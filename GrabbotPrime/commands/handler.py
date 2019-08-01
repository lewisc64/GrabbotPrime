from threading import Thread
import logging
import time

from .plugins import *
from .plugins.base import *

log = logging.getLogger(__name__)

class MessageTunnel:

    def __init__(self, expected_clients=2):

        self.expected_clients = expected_clients
        self.clients = []

        self.registering = False
        self.connected = False

    def register(self):

        while self.registering:
            pass
        self.registering = True

        log.debug("Registering tunnel connection...")

        self.clients.append({
            "messages": [],
            "last_messages_length": 0
        })

        if len(self.clients) >= self.expected_clients:
            self.open_connection()

        self.registering = False
        return len(self.clients) - 1

    def open_connection(self):
        self.connected = True

    def close_connection(self):
        self.connected = False

    def wait_for_connection(self):
        t = time.time()
        while not self.connected and time.time() - t < 10:
            pass

        if time.time() - t >= 10:
            raise Exception("Waiting for connection took too long.")

    def wait_for_message(self, client_number):
        other_client = self.clients[client_number - 1]
        while other_client["last_messages_length"] == len(other_client["messages"]):
            pass
        other_client["last_messages_length"] = len(other_client["messages"])
        return other_client["messages"][-1]

    def send_message(self, client_number, message):
        self.clients[client_number]["messages"].append(message)

class CommandContext:

    def __init__(self, command):
        self.tunnel = MessageTunnel()
        self.command_thread = Thread(target=command.handle, args=(self,), name=str(command), daemon=True)
        self.initial_message = None

    def run_command(self):
        Thread(target=self.manage_command, daemon=True).start()

    def manage_command(self):
        log.debug("Starting command thread...")
        self.command_thread.start()
        while self.command_thread.isAlive():
            pass
        log.debug("Closing tunnel connection, thread finished.")
        self.tunnel.close_connection()
        

def recognise_command(content):
    
    recognitions = []
    
    for command in commands:
        if command.recognise(content):
            recognitions.append(command)
            
    return recognitions

def create_context(command):

    log.debug(f"Creating connection to command object: {command}")
    
    context = CommandContext(command)
    
    return context

if __name__ == "__main__":
    context = connect(commands[0])
    import time
    time.sleep(5)
    context.send_message("hello")

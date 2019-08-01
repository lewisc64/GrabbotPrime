from .base import *
import logging

log = logging.getLogger(__name__)

@command
class ConnectToBridge(Command):

    def recognise(self, content):
        return content == "test"

    def handle(self, context, *args, **kwargs):
        super().handle(context, *args, **kwargs)
        
        self.send_message(context, "What is your name?")
        name = self.wait_for_message(context)
        
        self.send_message(context, f"You think that's a cool name? Huh? {name}?!")
        confirmed = "y" in self.wait_for_message(context)
        
        if confirmed:
            self.send_message(context, "You are wrong! Get lost.")
        else:
            self.send_message(context, "That's right. Don't you ever talk to me again.")
        

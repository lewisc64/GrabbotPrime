import logging

log = logging.getLogger(__name__)

commands = []

def command(class_reference):
    global commands
    commands.append(class_reference())
    log.info(f"Registered command plugin: {class_reference}")
    return class_reference

class Command:

    def __init__(self):
        pass

    def recognise(self, content):
        pass

    def handle(self, context, *args, **kwargs):
        context.tunnel.wait_for_connection()

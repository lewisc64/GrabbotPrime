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
        context.tunnel_id = context.tunnel.register()
        context.tunnel.wait_for_connection()

    def wait_for_message(self, context):
        return context.tunnel.wait_for_message(context.tunnel_id)

    def send_message(self, context, content):
        return context.tunnel.send_message(context.tunnel_id, content)

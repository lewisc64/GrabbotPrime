from ..component import *
from .discrod import *
import logging

@component
class DiscordBot(Component):

    name = "DiscordBot"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = kwargs["token"]

        self.writeable_values.extend(["token"])

        self.core = kwargs["core"]
        self.tunnels = {}
        
        self.bot = Bot(self.token)
        self.bot.on_message(self._message)

    def _message(self, data):
        if data["author"]["id"] == self.bot.user["id"]:
            return
        
        channel_id = data["channel_id"]
        
        if channel_id not in self.tunnels:
            
            tunnel = self.core.open_command_tunnel(data["content"])
            if tunnel is None:
                return
            
            self.tunnels[channel_id] = {"tunnel": tunnel}

            client_id = tunnel.register()
            self.tunnels[channel_id]["client_id"] = client_id
            tunnel.wait_for_connection()
            
            while tunnel.connected:
                message = tunnel.wait_for_message(client_id)
                self.bot.send_message(channel_id, str(message))

            log.debug("Removing tunnel from discord, connection closed.")
            del self.tunnels[channel_id]
            
        else:
            tunnel = self.tunnels[channel_id]["tunnel"]
            client_id = self.tunnels[channel_id]["client_id"]
            tunnel.send_message(client_id, data["content"])

    def cleanup(self):
        self.bot.logout()

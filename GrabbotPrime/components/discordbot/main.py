from ..component import *
from .discrod import *
import logging

log = logging.getLogger(__name__)

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

    def remove_tunnel(self, channel_id):
        log.debug("Removing tunnel from discord...")
        if channel_id in self.tunnels:
            del self.tunnels[channel_id]

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
                try:
                    message = tunnel.wait_for_message(client_id)
                except:
                    break
                self.bot.send_message(channel_id, str(message))
            self.remove_tunnel(channel_id)
            
        else:
            tunnel = self.tunnels[channel_id]["tunnel"]

            if tunnel.connected:
                client_id = self.tunnels[channel_id]["client_id"]
                tunnel.send_message(client_id, data["content"])
            else:
                log.warning("Dead tunnel found in storage.")
                self.remove_tunnel(channel_id)
                self._message(data)

    def cleanup(self):
        self.bot.logout()

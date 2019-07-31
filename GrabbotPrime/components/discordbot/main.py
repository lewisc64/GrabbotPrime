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
        
        self.bot = Bot(self.token)
        self.bot.on_message(self._message)

    def _message(self, data):
        print(data["content"])

    def cleanup(self):
        self.bot.logout()

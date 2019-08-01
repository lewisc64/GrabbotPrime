from ..component import *
import logging
import requests

log = logging.getLogger(__name__)

@component
class PhilipsHueBridge(Component):

    name = "PhilipsHueBridge"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ip = kwargs["ip"]
        self.api_endpoint = f"{self.ip}/api"

        if "username" not in kwargs:
            self._register

        self.writeable_values.extend(["ip"])

    def _register(self):
        body = {"devicetype": "grabbot_prime#python grabbot"}
        r = requests.post(self.api_endpoint, data=body)
        

    def _message(self, data):
        print(data["content"])

    def cleanup(self):
        self.bot.logout()

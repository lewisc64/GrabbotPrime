from ..component import *
import logging
import requests
import json

log = logging.getLogger(__name__)

@component
class PhilipsHueBridge(Component):

    name = "PhilipsHueBridge"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ip = kwargs["ip"]

        self.core = kwargs["core"]

        self.bridge_id = kwargs["bridge_id"]

        if "username" not in kwargs:
            self.username = None
        else:
            self.username = kwargs["username"]

        self.writeable_values.extend(["ip", "bridge_id", "username"])

    def get_api_address(self):
        return f"http://{self.ip}/api/{self.username}"

    def api_get(self, call):
        r = requests.get(self.get_api_address() + call)

        if r.status_code != 200:
            raise Exception(r"Response returned status code: {r.status_code}")
        
        return r.json()

    def get_light_groups(self):
        r = requests.get(self.get_api_address() + "/groups")
        return r.json()

    def get_lights(self):
        r = requests.get(self.get_api_address() + "/lights")
        return r.json()

    def set_light(self, light_id, state):
        r = requests.put(self.get_api_address() + f"/lights/{light_id}/state", data=json.dumps(state))

        if r.status_code != 200:
            raise Exception(r"Response returned status code: {r.status_code}")

        return r

    def verify_ip(self):
        try:
            r = requests.get("http://" + self.ip)
            return
        except:
            pass

        log.info("Can't connect to bridge, discovering new ip...")
        
        r = requests.get("https://discovery.meethue.com/")
        for bridge in r.json():
            if bridge["id"] == self.bridge_id:
                self.ip = bridge["internalipaddress"]
                log.info(f"Found new IP: {self.ip}")
                self.save(self.core.database)
                return

        log.error(f"Bridge {self.bridge_id} no longer exists! Was expecting it at {self.ip}")

    def is_registered(self):
        return self.username is not None
    
    def register(self):
        body = { "devicetype": "grabbot_prime#python grabbot" }
        r = requests.post(f"http://{self.ip}/api", data=json.dumps(body))

        data = r.json()

        if "success" in data[0]:
            self.username = data[0]["success"]["username"]
            self.save(self.core.database)
        
        return data[0]

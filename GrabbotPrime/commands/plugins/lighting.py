from .base import *
import logging
import requests
import re
import time

log = logging.getLogger(__name__)

def discover_bridges():
    r = requests.get("https://discovery.meethue.com/")
    return r.json()

def register_bridge(context, bridge):
    response = bridge.register()
    if "success" not in response:
        context.send_message("Bridge is not registered. Please press the link button on the Philips Hue bridge.")
        while "success" not in response:
            time.sleep(1)
            response = bridge.register()
            print(response)
        context.send_message("Bridge registered.")
            

def recognise_light(context, name):
    bridges = context.core.find_components_by_filter({ "type_name": "PhilipsHueBridge" })

    matched_group_lights = []
    matches = []
    
    for bridge in bridges:

        bridge.verify_ip()

        if not bridge.is_registered():
            register_bridge(context, bridge)

        for group_id, group in bridge.get_light_groups().items():
            if name == group["name"]:
                matched_group_lights.extend(group["lights"])

        for light_id, light in bridge.get_lights().items():
            if light_id in matched_group_lights or name == light["name"]:
                matches.append({"component": bridge, "light_id": light_id, "data": light})

    return matches

@command
class DiscoverBridges(Command):

    def recognise(self, content):
        return "discover" in content and "bridge" in content

    def handle(self, context, *args, **kwargs):
        super().handle(context, *args, **kwargs)

        core = context.core
        database = core.database

        found = 0

        for bridge in discover_bridges():
            
            component_data = database.find("components", { "type_name": "PhilipsHueBridge", "bridge_id": bridge["id"] })
            
            if component_data is None:
                component_data = {
                    "type_name": "PhilipsHueBridge",
                    "bridge_id": bridge["id"],
                    "ip": bridge["internalipaddress"],
                }
                core.create_component(component_data)
                found += 1

        context.send_message(f"Found {found} new bridge{'' if found == 1 else 's'}.")

@command   
class TurnLight(Command):

    formats = [
        re.compile(r"(?:turn|set) (?:the )?lights? in (?P<name>.+?) (?:to )?(?P<action>.+)", re.IGNORECASE),
        re.compile(r"(?:turn|set) (?:the )?(?P<name>.+?) lights? (?:to )?(?P<action>.+)", re.IGNORECASE),
    ]

    def recognise(self, content):
        for regex in TurnLight.formats:
            if regex.match(content):
                return True
        return False

    def handle(self, context, *args, **kwargs):
        super().handle(context, *args, **kwargs)

        for regex in TurnLight.formats:
            if regex.match(context.initial_message):
                match = regex.search(context.initial_message)
                break
        
        name = match.group("name")
        action = match.group("action")

        lights = recognise_light(context, name)

        for data in lights:
            data["component"].set_light(data["light_id"], {"on": action == "on"})

        if len(lights) > 0:
            context.send_message("Done.")
        else:
            context.send_message("Couldn't find any lights using that identifier.")


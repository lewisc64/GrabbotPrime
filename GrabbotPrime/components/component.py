import logging
import uuid

log = logging.getLogger(__name__)

component_classes = {}

def component(class_reference):
    global component_classes
    log.debug(f"Loaded component definition '{class_reference}'.")
    component_classes[class_reference.name] = class_reference
    return class_reference

def create_component(data, **kwargs):
    log.debug(f"Creating component from: {data}")

    if data["type_name"] not in component_classes:
        log.error(f"Cannot find component class with type name '{data['type_name']}'")
        log.debug(f"    Data: {data}")
        raise ValueError
    
    return component_classes[data["type_name"]](**data, **kwargs)

class Component:

    name = None

    def __init__(self, **kwargs):
        self.writeable_values = ["type_name", "uuid"]
        self.type_name = kwargs["type_name"]

        if "uuid" not in kwargs:
            self.uuid = str(uuid.uuid4())
        else:
            self.uuid = kwargs["uuid"]

    def cleanup(self):
        pass

    def save(self, database):
        record = {}

        for field_name in self.writeable_values:
            record[field_name] = getattr(self, field_name)

        print(record)
        
        database.insert("components", { "uuid": self.uuid }, record, upsert=True)

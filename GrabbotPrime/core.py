import logging
from database import MongoDatabase
import commands
import components

log = logging.getLogger(__name__)

class Core:

    def __init__(self):

        self.components = []
        self.database = MongoDatabase("localhost")

        self.load_components()

    def load_components(self):

        log.info("Loading components...")

        for record in self.database.get_all_records("components"):
            try:
                self.create_component(record, save=False)
            except ValueError:
                pass

    def open_command_tunnel(self, content):
        matches = commands.recognise_command(content)
        if len(matches) == 0:
            return None
        
        context = commands.create_context(matches[0])
        context.initial_message = content
        context.run_command()
        return context.tunnel
    
    def create_component(self, data, save=True):
        component = components.create_component(data, core=self)
        if save:
            component.save(self.database)
        self.components.append(component)

    def save_all(self):

        log.info("Saving everything...")
        
        for component in self.components:
            component.save(self.database)

    def cleanup_all(self):

        log.info("Cleaning everything...")
        
        for component in self.components:
            component.cleanup()

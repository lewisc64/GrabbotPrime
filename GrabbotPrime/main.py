import logging

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.DEBUG)

from core import Core

if __name__ == "__main__":
    
    core = Core()

from os.path import dirname, basename, isfile
import glob
import logging

log = logging.getLogger(__name__)

def find_all():
    modules = glob.glob(dirname(__file__)+"/*.py")
    plugins = [basename(f)[:-3] for f in modules if isfile(f)]
    plugins.remove("__init__")

    for plugin in plugins:
        log.debug(f"Found command plugin '{plugin}'")

    return plugins

__all__ = find_all()


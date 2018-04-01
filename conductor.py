import yaml
import importlib
from properties import PROVIDERS_DIR


def play_notes(filename):
    stream = open(filename, 'r')
    notes = yaml.load(stream)
    print(notes["project"])
    for space in notes["project"]:
        space = list(space.values())[0]  # looks like the most elegant way to get value
        provider = space.pop("provider")
        provider_module_path = PROVIDERS_DIR + '.' + provider
        provider_module = importlib.import_module(provider_module_path)  # import provider as module
        provider_module.run(space)


play_notes("notes.yml")
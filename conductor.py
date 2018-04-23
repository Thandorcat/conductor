import requests
import socket
import json

import yaml
import importlib
from properties import PROVIDERS_DIR

class Conductor_CLI:

    def __init__(self, address='localhost', port=5999):
        self.address = socket.gethostbyname(address)
        self.port = str(port)
        self.core_url = "http://" + self.address + ":" + self.port


    def play_notes(self, filename):
        stream = open(filename, 'r')
        notes = yaml.load(stream)
        json_data = json.dumps(notes)
        print(json_data)
        request = requests.post(self.core_url, json=json_data)
        print(request.text)

        # for space in notes["project"]:
        #     space = list(space.values())[0]  # looks like the most elegant way to get value
        #     provider = space.pop("provider")
        #     provider_module_path = PROVIDERS_DIR + '.' + provider
        #     provider_module = importlib.import_module(provider_module_path)  # import provider as module
        #     provider_module.run(space)

cli = Conductor_CLI()
cli.play_notes("notes.yml")
import requests
import socket
import json

import yaml


class Conductor_CLI:

    def __init__(self, address='localhost', port=5999):
        self.address = socket.gethostbyname(address)
        self.port = str(port)
        self.core_url = "http://" + self.address + ":" + self.port


    def play_notes(self, filename):
        stream = open(filename, 'r')
        notes = yaml.load(stream)
        message = {'play': notes}
        json_data = json.dumps(message)
        print(json_data)
        request = requests.post(self.core_url, json=json_data)
        print(request.text)

if __name__ == '__main__':
    cli = Conductor_CLI()
    cli.play_notes("notes.yml")
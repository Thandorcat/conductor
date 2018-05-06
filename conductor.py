import requests
import socket
import json
import sys
import yaml


class Conductor_CLI:

    def __init__(self, address='localhost', port=5999):
        self.address = socket.gethostbyname(address)
        self.port = str(port)
        self.core_url = "http://" + self.address + ":" + self.port

    def handle_command(self, arguments):
        methods = {'play': self.play,
                   'stop': self.stop,
                   'list': self.list}
        action = arguments[0]
        methods[action](arguments[1:])

    def send_request(self, action, data):
        message = {action: data}
        json_data = json.dumps(message)
        print(json_data)
        request = requests.post(self.core_url, json=json_data)
        if self.code_ok(request.status_code):
            print('Success!')
        else:
            print('Failed!')
        print(request.text)

    def code_ok(self, code):
        if int(code/100) == 2:
            return True
        else:
            return False

    def list(self, arguments):
        if arguments:
            providers_list = ' '.join(arguments)
            self.send_request('list', arguments)
        else:
            self.send_request('list', 'all')

    def stop(self, arguments):
        provider = arguments.pop(0)
        instances = " ".join(arguments)
        data = {}
        data['provider'] = provider
        data['instances'] = instances
        self.send_request('stop', data)

    def play(self, arguments):
        filename = arguments[0] #it recieves name as list
        stream = open(filename, 'r')
        notes = yaml.load(stream)
        self.send_request('play', notes)


if __name__ == '__main__':
    cli = Conductor_CLI()
    arguments = sys.argv[1:]
    cli.handle_command(arguments)
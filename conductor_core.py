from flask import Flask, request, Response
import json
import importlib

import properties
from providers.provider import Provider

class Core:


    def __init__(self, address=properties.ADDRESS, port=properties.PORT):
        self.address = address
        self.port = port

    def start(self):
        app = Flask(__name__)

        @app.route('/', methods=['POST'])
        def result():
            json_data = request.json
            request_data = json.loads(json_data)
            print(request_data)
            response = self.handle_request(request_data)
            return Response(status=response)

        app.debug = True
        app.run(host=self.address, port=self.port)

    def handle_request(self, request):
        methods = {'play': self.play, 'stop': self.stop}
        for action in request:
            response = methods[action](request[action])
            if response != 200:
                return 500
        return 200

    def play(self, notes):
        for space in notes["project"]:
            space = list(space.values())[0]  # looks like the most elegant way to get value
            provider_name = space.pop("provider")
            provider = Provider(provider_name).get_provider()
            provider.run(space)

    def stop(self, instanses):
        pass

if __name__ == '__main__':
   core = Core()
   core.start()
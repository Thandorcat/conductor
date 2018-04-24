from flask import Flask, request, Response
import json
import importlib
from properties import PROVIDERS_DIR

class Core:


    def __init__(self, address='0.0.0.0', port=5999):
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

        return True

    def play(self, notes):
        for space in notes["project"]:
            space = list(space.values())[0]  # looks like the most elegant way to get value
            provider = space.pop("provider")
            provider_module_path = PROVIDERS_DIR + '.' + provider
            provider_module = importlib.import_module(provider_module_path)  # import provider as module
            provider_module.run(space)

    def stop(self, instanses):
        pass

if __name__ == '__main__':
   core = Core()
   core.start()
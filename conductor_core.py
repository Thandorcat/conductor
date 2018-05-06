from flask import Flask, request, Response
import json
import importlib

import properties
from providers.provider import Provider

class Core:
    ok_code=200

    def __init__(self, address=properties.ADDRESS, port=properties.PORT):
        self.address = address
        self.port = port
        self.providers = {}

    def start(self):
        app = Flask(__name__)

        @app.route('/', methods=['POST'])
        def result():
            json_data = request.json
            request_data = json.loads(json_data)
            print(request_data)                 # DEBUG!!!!!!!!!!
            response, code = self.handle_request(request_data)
            return Response(response ,status=code)

        app.debug = True
        app.run(host=self.address, port=self.port)

    def get_provider(self, provider_name):
        if provider_name in self.providers:
            return self.providers[provider_name]
        else:
            provider_module = Provider(provider_name)
            provider = provider_module.get_provider()
            self.providers[provider_name] = provider  # collects all providers in dictionary
            return provider

    def handle_request(self, request):
        methods = {'play': self.play,
                   'stop': self.stop,
                   'list': self.list}
        message = ''
        for action in request:
            response, code = methods[action](request[action])
            message += response
            if not self.code_ok(code):
                return message, code
        return response, self.ok_code

    def play(self, notes):
        message = ''
        for space in notes["project"]:
            space = list(space.values())[0]  # looks like the most elegant way to get value
            provider_name = space.pop("provider")
            provider = self.get_provider(provider_name)
            response, code = provider.run(space)
            message += response
            if not self.code_ok(code):
                return message, code
        return message, self.ok_code


    def code_ok(self, code):
        if int(code/100) == 2:
            return True
        else:
            return False

    def stop(self, arguments):
        provider = self.get_provider(arguments['provider'])
        return provider.stop(arguments['instances'])

    def list(self, providers):
        message = ''
        if providers == 'all':
            providers_list = list(self.providers.values()) # get all later
        else:
            providers_list = [self.get_provider(provider_name) for provider_name in providers]
        for provider in providers_list:
            response, code = provider.list()
            message += response
            if not self.code_ok(code):
                return message, code
        return message, self.ok_code



if __name__ == '__main__':
   core = Core()
   core.start()
from flask import Flask, request, Response
import json
from monitor import Monitor
from orcestrator import Orcestrator
from multiprocessing import Process, Queue
import uuid

import properties
from providers.provider import Provider


class Core:

    ok_code = 200
    error_code = 500

    def __init__(self, address=properties.ADDRESS, port=properties.PORT):
        self.address = address
        self.port = port
        self.providers = {}
        self.metric_queue_in = Queue()
        self.metric_queue_out = Queue()
        self.orcestrator_queue_in = Queue()
        self.orcestrator_queue_out = Queue()
        self.monitor_process = self.create_monitor()
        self.orcestrator_process = self.create_orcestrator()

    def start(self):
        app = Flask(__name__)

        @app.route('/', methods=['POST'])
        def result():
            json_data = request.json
            request_data = json.loads(json_data)
            response, code = self.handle_request(request_data)
            return Response(response, status=code)

        #app.debug = True
        app.run(host=self.address, port=self.port)

    def get_provider(self, provider_name):
        if provider_name in self.providers:
            return self.providers[provider_name]
        else:
            provider_module = Provider(provider_name)
            provider = provider_module.get_provider()
            self.providers[provider_name] = provider  # collects all providers in dictionary
            return provider


    def create_monitor(self):
        monitor = Monitor(self.metric_queue_in, self.metric_queue_out, self.orcestrator_queue_in)
        self.monitor_process = Process(target=monitor.run_monitor)
        self.monitor_process.start()
        return self.monitor_process

    def create_orcestrator(self):
        orcestrator = Orcestrator(self.orcestrator_queue_in, self.orcestrator_queue_out)
        self.orcestrator_process = Process(target=orcestrator.run_orcestrator)
        self.orcestrator_process.start()
        return self.orcestrator_process

    def start_monitor(self):
        if self.monitor_process.is_alive():
            return 'Monitor is already running', self.ok_code
        else:
            self.create_monitor()
            return 'Monitor started', self.ok_code

    def stop_monitor(self):
        if self.monitor_process.is_alive():
            self.monitor_process.terminate()
            return 'Monitor stopped', self.ok_code
        else:
            return 'Monitor is already stopped', self.ok_code

    def monitor_status(self):
        if self.monitor_process.is_alive():
            self.monitor_send_command('status')
            status = self.monitor_recieve_message()
            return status
        else:
            return 'Monitor is stopped', self.error_code

    def monitor_recieve_message(self):
        status = self.metric_queue_out.get()
        return status

    def monitor_send_command(self, command):
        self.metric_queue_in.put(command)

    def monitor_add_metrics(self, metrics, uuid):
        message = ''
        for metric in metrics:
            self.metric_queue_in.put((metric, uuid))
            result, code = self.monitor_recieve_message()
            if self.code_ok(code):
                message += result + '\n'
            else:
                message += "Error" + result + '\n'
        return message, self.ok_code


    def handle_request(self, request):
        methods = {'play': self.play,
                   'stop': self.stop,
                   'list': self.list,
                   'monitor': self.monitor}
        message = ''
        for action in request:
            response, code = methods[action](request[action])
            message += response
            if not self.code_ok(code):
                return message, code
        return message, self.ok_code

    def play(self, notes):
        message = ''
        for space in notes["project"]:
            space = list(space.values())[0]  # looks like the most elegant way to get value
            provider_name = space.pop("provider")
            provider = self.get_provider(provider_name)
            space['uuid'] = uuid.uuid4()
            response, code = provider.run(space)
            message += response
            if not self.code_ok(code):
                return message, code

            if 'monitor' in space:
                self.monitor_add_metrics((space['monitor'], space['uuid']))
                self.orcestrator_queue_in.put(space['uuid'], {provider: space})

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

    def monitor(self, new_metric):
        commands = ['start', 'stop', 'status']
        if new_metric in commands:
            commands_methods = {'start': self.start_monitor,
                                'stop': self.stop_monitor,
                                'status': self.monitor_status}
            return commands_methods[new_metric]()
        else:
            if self.monitor_process.is_alive():
                message = self.monitor_add_metrics(new_metric, "manual")
                return message
            else:
                return 'Monitor is not running', self.error_code

if __name__ == '__main__':
   core = Core()
   core.start()
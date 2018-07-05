import time
from monitor import Monitor
from multiprocessing import Process, Queue

class Orcestrator:

    def __init__(self, orcestrator_queue_in, orcestrator_queue_out):
        self.instances = {}
        self.orcestrator_queue_in = orcestrator_queue_in
        self.orcestrator_queue_out = orcestrator_queue_out
        self.logs = ''

    def add_instance(self, instance):
        uuid = instance[0]
        self.instances[uuid] = instance[1]

    def send_status(self):
        if self.logs:
            self.orcestrator_queue_out.put(self.logs)
            self.clear_logs()
            return False
        else:
            message = "Everything was good."
            self.orcestrator_queue_out.put(message)
            return True

    def clear_logs(self):
        self.logs = ''

    def save_to_logs(self, message):
        self.logs += message

    def restart_instance(self, uuid):
        instance = self.instances[uuid]
        for provider in instance:
            provider.restart(instance[provider])
        self.save_to_logs("Space " + str(instance[provider].type) + " was restarted!")

    def check_status(self, status):
        for uuid in status:
            if not status[uuid]:
                self.restart_instance(uuid)

    def run_orcestrator(self):
        print("Orcestrator started!")
        while True:
            request = self.orcestrator_queue_in.get()
            if request == 'status':
                self.send_status()
            elif request[0] == 'monitor_status':
                self.check_status(request[1])
            else:
                self.add_instance(request)
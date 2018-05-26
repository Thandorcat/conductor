import psutil as psutil


class Metric:
    def __init__(self, load):
        self.load = load
        self.name = 'cpu_max'
        self.display_name = 'CPU usage'

    def check(self):
        if psutil.cpu_percent() < self.load:
            return True
        else:
            return False

    def value(self):
        return psutil.cpu_percent()
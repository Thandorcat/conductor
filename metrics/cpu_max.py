import psutil as psutil


class Metric:
    def __init__(self, load):
        self.load = load
        self.name = 'cpu_max'
        self.display_name = 'CPU usage'

    def check(self):
        if self.value() < self.load:
            return True
        else:
            return False

    def value(self):
        return psutil.cpu_percent()
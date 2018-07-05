import psutil as psutil


class Metric:
    def __init__(self, usage):
        self.usage = usage
        self.name = 'mem_max'
        self.display_name = 'Memory usage'

    def check(self):
        if self.value() < self.usage:
            return True
        else:
            return False

    def value(self):
        return psutil.virtual_memory()
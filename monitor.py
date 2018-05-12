import importlib
import properties
import time


class Monitor:

    ok_code = 200
    error_code = 500

    def __init__(self, metric_queue_in,metric_queue_out):
        self.metric_queue_in = metric_queue_in
        self.metric_queue_out = metric_queue_out
        self.metrics = []

    def add_metric(self, new_metric):
        try:
            for metric_name in new_metric:
                value = new_metric[metric_name]
                metric_name = properties.METRICS_DIR + '.' + metric_name
                module = importlib.import_module(metric_name)  # import provider as module
                metric = module.Metric(value)
                self.metrics.append(metric)
                message = "Added metric" + metric_name + ' value is: ' + value
                response = message, self.ok_code
                self.metric_queue_out.put(response)
        except Exception as e:
            message = str(e)
            response = message, self.ok_code
            self.metric_queue_out.put(response)

    def get_metrics(self):
        self.metric_queue_out(self.metrics)

    def send_status(self):
        # если есть value, то его, если нет, то чек
        message = ""
        try:
            for metric in self.metrics:
                if metric.check():
                    message += metric.name + ': [OK]\n'
                else:
                    message += metric.name + ': [FAIL]\n'
            response = message, self.ok_code
            self.metric_queue_out.put(response)
        except Exception as e:
            message = str(e)
            response = message, self.ok_code
            self.metric_queue_out.put(response)

    def run_monitor(self):
        print("Monitor started!")
        while True:
            request = self.metric_queue_in.get()
            if request == 'status':
                self.send_status()
            else:
                self.add_metric(request)



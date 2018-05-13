import importlib
import properties
import time


class Monitor:

    ok_code = 200
    error_code = 500

    def __init__(self, metric_queue_in,metric_queue_out,orcestrator_queue_in):
        self.metric_queue_in = metric_queue_in
        self.metric_queue_out = metric_queue_out
        self.orcestrator_queue_in = orcestrator_queue_in
        self.metrics = {}

    def add_metric(self, new_metric):
        try:
            uuid = new_metric[1]
            new_metric = new_metric[0]
            for metric_name in new_metric:
                value = new_metric[metric_name]
                metric_name = properties.METRICS_DIR + '.' + metric_name
                module = importlib.import_module(metric_name)  # import provider as module
                metric = module.Metric(value)
                uuid_metrics = self.metrics.get(uuid, [])
                uuid_metrics.append(metric)
                self.metrics[uuid] = uuid_metrics
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
            for uuid in self.metrics:
                for metric in self.metrics[uuid]:
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

    def check_metrics(self):
        result = {}
        for uuid in self.metrics:
            status = True
            for metric in self.metrics[uuid]:
                if not metric.check():
                    status = False
                    break
            result[uuid] = status
        self.orcestrator_queue_in.put(('monitor_status', result))

    def run_monitor(self):
        print("Monitor started!")
        while True:
            try:
                request = self.metric_queue_in.get(timeout=properties.MONITOR_FREQ)
                if request == 'status':
                    self.send_status()
                else:
                    self.add_metric(request)
            except Exception as e:
                self.check_metrics()




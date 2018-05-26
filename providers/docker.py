import docker
from docker.utils import ports


class Provider:

    ok_code = 200
    resource_created_code=201

    def __init__(self):
        self.client = docker.from_env()
        self.message = ''
        self.type = 'docker'

    def handle_exception(fn):
        def wrapped(self, *args):
            try:
                return fn(self, *args)
            except Exception as e:
                self.message += str(e)
                return self.message, 500

        return wrapped

    @handle_exception
    def run(self, options):
        self.message = ''
        location = options.pop("location")
        for service in options.values():
            image = service.get("image", None)
            port = (service.get("ports", None))[0]
            container = self.client.containers.run(image, detach=True, ports=port)
            self.message += 'Container ' + container.short_id + ' started\n'
            return self.message, self.resource_created_code

    @handle_exception
    def restart(self, ):
        pass

    @handle_exception
    def list(self):
        self.message = ''
        containers = self.client.containers.list()
        if not containers:
            return 'No containers running', self.ok_code
        self.message += 'Docker containers:\n'
        for container in self.client.containers.list():
            self.message += 'ID: ' + str(container.short_id)
            self.message += ' Image: ' + str(container.image.short_id)
            self.message += ' Status: ' + str(container.status) + '\n'
            return self.message, 200

    @handle_exception
    def restart(self):
        pass

    @handle_exception
    def stop(self, container_ids):
        self.message = ''
        for container_id in container_ids.split(' '):
            container = self.client.containers.get(container_id)
            container.stop()
            self.message += 'Container ' + container_id + ' stopped.'
        return self.message, 200
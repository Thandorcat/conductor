import docker
from docker.utils import ports


def run(options):
    client = docker.from_env()
    print(client.containers.list())
    location = options.pop("location")
    for service in options.values():
        print(service)
        image = service.get("image", None)
        port = (service.get("ports", None))[0]
        print(image)
        print(type(port))
        client.containers.run(image, detach=True, ports=port)
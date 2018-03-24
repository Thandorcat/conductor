import docker
import yaml

client = docker.from_env()
print(client.containers.list()[0].image)

stream = open('notes.yml', 'r')
notes = yaml.load(stream)
print(type(notes))
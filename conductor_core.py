from flask import Flask, request
import json
import importlib
from properties import PROVIDERS_DIR

app = Flask(__name__)
#app.config['SERVER_NAME'] = "0.0.0.0:5900"
@app.route('/', methods=['POST'])
def result():
    json_data = request.json
    notes = json.loads(json_data)
    print(notes)
    for space in notes["project"]:
        space = list(space.values())[0]  # looks like the most elegant way to get value
        provider = space.pop("provider")
        provider_module_path = PROVIDERS_DIR + '.' + provider
        provider_module = importlib.import_module(provider_module_path)  # import provider as module
        provider_module.run(space)
    return 'Performed!'

app.debug = True
app.run(host='0.0.0.0', port=5999)
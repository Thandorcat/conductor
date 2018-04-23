from flask import Flask, request
import json

app = Flask(__name__)
#app.config['SERVER_NAME'] = "0.0.0.0:5900"
@app.route('/', methods=['POST'])
def result():
    json_data = request.json
    notes = json.loads(json_data)
    print(notes)
    return 'Performed!'

app.debug = True
app.run(host='0.0.0.0', port=5999)
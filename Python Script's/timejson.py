import json
import datetime
from flask import Flask


t = {'name': 'JSON time'}

t['date'] = datetime.datetime.now()

def strconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

app = Flask(__name__)


@app.route("/get-server-time", methods=['GET'])
def index():
    return json.dumps(t, default=strconverter)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567)

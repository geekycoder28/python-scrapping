from flask import Flask, request
from main import process_link
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def hello_world():
    print("Running", request, request.method)
    request_json = request.get_json(silent=True)
    print(request_json)
    return process_link(request)

if __name__ == '__main__':
    app.run()

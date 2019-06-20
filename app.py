from flask import Flask, json
from flask import request

from client import send_request_to_server, create_login_request, create_message_request, module_var, start

app = Flask(__name__)
start()


@app.route('/login', methods=['POST'])
def login():
    body = request.data
    data = json.loads(body)

    send_request_to_server(create_login_request(data['login']))

    if module_var.isLogged:
        response = {'login': data['login'], 'access': 'grated'}
    else:
        response = {'login': data['login'], 'access': 'denied'}

    return app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )

@app.route('/sendmessage', methods=['POST'])
def send_message():

    data = json.loads(request.data)
    send_request_to_server(create_message_request(data['login'],data['message']))

    return app.response_class(
        response=json.dumps({'code': 'ok'}),
        status=200,
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run()

from flask import Flask, json
from flask import request
from flask_cors import CORS

from client import send_request_to_server, create_login_request, create_message_request, module_var, start, create_logout_request

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
start()


@app.route('/api/sendmessage', methods=['POST'])
def send_message():
    data = json.loads(request.data)
    send_request_to_server(create_message_request(data['user'], data['messageText']))

    return app.response_class(
        response=json.dumps({'code': 'ok'}),
        status=200,
        mimetype='application/json'
    )


@app.route('/api/login', methods=['POST'])
def login():
    body = request.data
    data = json.loads(body)

    send_request_to_server(create_login_request(data['username']))

    if module_var.isLogged:
        response = {'username': data['username'], 'access': 'granted'}
    else:
        response = {'username': data['username'], 'access': 'denied'}

    return app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json',
    )


@app.route('/api/messages', methods=['GET'])
def get_all_available_message():
    all_messages_response = []

    if module_var.all_messages:
        all_messages_response = json.dumps(module_var.all_messages)
        module_var.all_messages.clear()

    return app.response_class(
        response=all_messages_response,
        status=200,
        mimetype='application/json'
    )


@app.route('/api/onlineusers', methods=['GET'])
def get_online_users():
    return json.dumps({"online": module_var.online_list})


@app.route('/api/logout', methods=['POST'])
def logout_user():
    body = request.data
    data = json.loads(body)

    send_request_to_server(create_logout_request(data['username'], data['logout']))

    return app.response_class(
        response=body,
        status=200,
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(debug=True, use_evalex=False)

import socket
import ssl
import sys
import threading
import time
import logging
import event_parser
import event_types

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


logging.basicConfig(level=logging.DEBUG)

host = "192.168.0.73"
port = 8889

module_var = sys.modules[__name__]

module_var.isLogged = False
module_var.online_list = []
module_var.all_messages = []


def get_data_from_server():
    read_size = 1024
    while True:
        data = server_socket.recv(1024)
        full_length = event_parser.get_full_length(data.decode())

        while read_size < full_length:
            data += server_socket.recv(1024)
            read_size += 1024

        received_response = data.decode()
        logging.info("Received: " + received_response)

        if received_response:
            create_event_from_string(received_response)


def create_event_from_string(response_from_server):
    pr = event_parser.EventParser()
    event_from_server = pr.parse_string_to_event(response_from_server)

    if event_from_server.event_type == event_types.LOGIN_RESPONSE:

        if event_from_server.code == event_types.CODE_ACCEPT:
            logging.info("LOGIN ACCEPTED")
            module_var.isLogged = True

        # When username exists
        elif event_from_server.code == event_types.CODE_REJECT:
            logging.info("LOGIN REJECT")

    elif event_from_server.event_type == event_types.MESSAGE_REQUEST:
        event_from_server_object = {'user': event_from_server.login,
                                    'messageText': event_from_server.message,
                                    'created': event_from_server.timestamp}
        module_var.all_messages.append(event_from_server_object)

    elif event_from_server.event_type == event_types.ONLINE_REQUEST:
        module_var.online_list.clear()
        module_var.online_list = eval(event_from_server.online_users)


def create_login_request(username):
    login_request = event_types.LoginRequest(username)
    login_request_string = login_request.convert_to_string()
    return login_request_string


def create_logout_request(username, is_logged_out):
    logout_request = event_types.LogoutRequest(username, is_logged_out)
    logout_request_string = logout_request.convert_to_string()
    module_var.isLogged = False
    return logout_request_string


def send_request_to_server(request_string):
    logging.info('Sent to server: %r' % request_string)
    server_socket.send(request_string.encode())
    time.sleep(0.1)


def create_message_request(username, message):
    message_request = event_types.MessageRequest(username, message)
    message_request_string = message_request.convert_to_string()
    return message_request_string


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
context = ssl.create_default_context(cafile="server.crt")
server_socket = context.wrap_socket(socket, server_side=False, server_hostname='server')


def start():
    try:
        server_socket.connect((host, port))

        threading.Thread(target=get_data_from_server).start()

    # for now :)))))
    except Exception as e:
        print(e)

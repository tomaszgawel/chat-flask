import socket
import threading
import event_parser
import event_types

host = "localhost"
port = 8889

all_message = []
isLogged = False


def get_data_from_server(server_socket):
    read_size = 1024
    while True:
        print("Waiting for a data...")
        data = server_socket.recv(1024)
        full_length = event_parser.get_full_length(data.decode())

        while read_size < full_length:
            data += socket.recv(1024)
            read_size += 1024

        received_response = data.decode()
        print("RECEIVED: " + received_response)

        if received_response:
            print("Starting making events: ")
            event_creator = threading.Thread(target=create_event_from_string,args=(received_response,))
            event_creator.start()


def create_event_from_string(response_from_server):
    pr = event_parser.EventParser()
    event_from_server = pr.parse_string_to_event(response_from_server)

    print("Create_event_from_string_start")

    if event_from_server.event_type == event_types.LOGIN_RESPONSE:
        print("\nLogin response: ")

        if event_from_server.code == event_types.CODE_ACCEPT:
            print("ACCEPTED")
            isLogged = True

        # When username exists
        elif event_from_server.code == event_types.CODE_REJECT:
            print("REJECT")

    if event_from_server.event_type == event_types.MESSAGE_REQUEST:
        print("\nMessage\n{}: {}".format(event_from_server.login, event_from_server.message))
        all_message.append(event_from_server)


def create_login_request(username):
    login_request = event_types.LoginRequest(username)
    login_request_string = login_request.convert_to_string()
    return login_request_string


def send_request_to_server(server_socket, request_string):
    print('Send: %r' % request_string)
    server_socket.send(request_string.encode())


def create_message_request(username, message):
    message_request = event_types.MessageRequest(username, message)
    message_request_string = message_request.convert_to_string()
    return message_request_string


# Start
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.connect((host, port))

    # Listening without join !
    listen = threading.Thread(target=get_data_from_server, args=(server_socket,))
    listen.start()

    # Login request example usage.
    login_request1 = threading.Thread(target=send_request_to_server(server_socket, create_login_request("Hej")))
    login_request1.start()
    login_request1.join()

    # Message request example usage.
    message_request1 = threading.Thread(target=send_request_to_server(server_socket, create_message_request("Hej", "To ja")))
    message_request1.start()
    message_request1.join()

    # server_socket.close()


except socket.error as e:
    print(e)

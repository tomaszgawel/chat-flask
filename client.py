import asyncio
import event_types
import event_parser
import logging

host = "localhost"
port = 8889


async def get_data_from_client(reader):
    read_size = 1024
    data = await reader.read(1024)
    full_length = event_parser.get_full_length(data.decode())

    while read_size < full_length:
        data += await reader.read(1024)
        read_size += 1024

    return data.decode()


async def send_request_to_server_and_receive_data(writer, reader, request_string):
    print('Send: %r' % request_string)
    writer.write(request_string.encode())

    data = await get_data_from_client(reader)
    print('Recived: %r' % data)

    return data


async def imitate_login(username):
    login_request = event_types.LoginRequest(username)
    login_request_string = login_request.convert_to_string()
    return login_request_string


async def imitate_message(username, message):
    message_request = event_types.MessageRequest(username, message)
    message_request_string = message_request.convert_to_string()
    return message_request_string


async def handle_connection(loop):
    reader, writer = await asyncio.open_connection(host, port, loop=loop)
    login_request_string = await imitate_login("Test User")

    # Send login to server and receive data.
    data_from_server = await send_request_to_server_and_receive_data(writer, reader, login_request_string)

    # Replace case if protocol will be finished
    if data_from_server == login_request_string:
        print("Established connection with server\n")

        while True:
            # do something
            print("You can start typing now!\n")
            message_request_string = await imitate_message("Test User", "TestTestTestTestTestTestTestTestTestTestTestTest")
            data_from_server = await send_request_to_server_and_receive_data(writer, reader, message_request_string)
            break

    print('Close the socket')
    writer.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(handle_connection(loop))
loop.close()


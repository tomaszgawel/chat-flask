import asyncio
import event_types
import event_parser
import logging

host = "localhost"
port = 8889


# Replace test_login !!!
async def imitate_login(username):
    logging.info('Login initial!')
    login_request = event_types.LoginRequest(username)
    login_request_string = login_request.convert_to_string()
    return login_request_string


async def handle_connection(loop):
    reader, writer = await asyncio.open_connection(host, port, loop=loop)

    login_request_string = await imitate_login("Test User")

    print('Send: %r' % login_request_string)
    writer.write(login_request_string.encode())

    data = await reader.read(100)
    print('Recived: %r' % data.decode())

    print('Close the socket')
    writer.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(handle_connection(loop))
loop.close()


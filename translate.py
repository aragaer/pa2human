import json
import socket


def perform_request(query, server_address):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(server_address)
    message = json.dumps(query, ensure_ascii=False)
    sock.sendall("{}\n".format(message).encode())
    data = b'' 
    while True:
        data_byte = sock.recv(1)
        if not data_byte or data_byte == b'\n':
            break
        data += data_byte
    sock.close()
    return json.loads(data.decode())


def main(user, bot, phrase, server_address):
    event = {'user': user, 'bot': bot, 'text': phrase}
    result = perform_request(event, server_address)
    print(result['reply'])

import json

PACKET_LENGTH_SIZE = 2


def encode_packet(data):
    payload = json.dumps(data).encode()
    packet_len = len(payload)
    packet_len_bytes = packet_len.to_bytes(PACKET_LENGTH_SIZE, 'big')
    packet = packet_len_bytes + payload
    return packet


# when client connects to server, hello packet gets sent to associate connection with nick
def build_hello_packet(nick_name):
    data = {'type': 'hello', 'nick': nick_name}
    return encode_packet(data)


# this function handles socket buffers packet by packet and only returns complete packets
def process_socket_buffer(buffer_source, socket=None, is_dict=False):
    if is_dict:
        if socket is None:
            raise ValueError(
                'socket must be provided when processing multi-buffer')
        buf = buffer_source[socket]
    else:
        buf = buffer_source

    packets = []

    while len(buf) >= PACKET_LENGTH_SIZE:
        packet_length = int.from_bytes(buf[:2], 'big')
        if len(buf) < packet_length + 2:
            break
        packet = buf[2:packet_length + 2]
        buf = buf[packet_length + 2:]
        packets.append(packet)

    if is_dict:
        buffer_source[socket] = buf
        return packets
    else:
        return packets, buf


# this function decodes the payload and loads it into dict
def handle_packet(packet):
    return json.loads(packet.decode())


def broadcast_connect(nick_name, all_connected_sockets, client_nicknames):
    data = {'type': 'join', 'nick': nick_name}
    packet = encode_packet(data)
    for sock in all_connected_sockets:
        if sock in client_nicknames:
            sock.sendall(packet)


def broadcast_disconnect(nick_name, all_connected_sockets, client_nicknames):
    data = {'type': 'leave', 'nick': nick_name}
    packet = encode_packet(data)
    for sock in all_connected_sockets:
        if sock in client_nicknames:
            sock.sendall(packet)


def send_message(client_socket, payload):
    data = {'type': 'chat', 'message': payload}
    client_socket.sendall(encode_packet(data))


def broadcast_message(nick_name, payload, all_connected_sockets, client_nicknames):
    data = {'type': 'chat', 'nick': nick_name, 'message': payload}
    packet = encode_packet(data)
    for sock in all_connected_sockets:
        if sock in client_nicknames:
            sock.sendall(packet)

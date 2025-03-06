import sys
import socket
import select
import utils

socket_bufs = {}
client_nicknames = {}


def run(port):
    global socket_bufs
    global client_nicknames

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen()
    print(f"listening on port {port}")
    potential_readers = {server_socket}

    while True:
        ready_to_read, _, _ = select.select(
            potential_readers, [], []
        )

        for sock in ready_to_read:

            if sock == server_socket:
                client_socket, addrinfo = server_socket.accept()
                # add client socket to select set
                potential_readers.add(client_socket)
                # assign a buffer to the client socket
                socket_bufs[client_socket] = b''
            else:
                data = sock.recv(4096)
                if data == b'':
                    potential_readers.remove(sock)
                    utils.broadcast_disconnect(
                        client_nicknames[sock], potential_readers, client_nicknames)
                    continue

                socket_bufs[sock] = socket_bufs.get(sock, b'') + data

                # process the current client buffer to look for complete packets to handle
                packets = utils.process_socket_buffer(
                    socket_bufs, sock, is_dict=True)

                for packet in packets:
                    # handle complete packets according to type
                    payload = utils.handle_packet(packet)
                    if payload['type'] == 'hello':
                        # associate nick_name with current socket
                        client_nicknames[sock] = payload['nick']
                        # broadcast connection to all connected clients
                        utils.broadcast_connect(
                            client_nicknames[sock], potential_readers, client_nicknames)
                    elif payload['type'] == 'chat':
                        utils.broadcast_message(
                            client_nicknames[sock], payload['message'], potential_readers, client_nicknames)


def usage():
    print("Usage: python3 chatserver.py [port]")


def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run(port)


if __name__ == "__main__":
    sys.exit(main(sys.argv))

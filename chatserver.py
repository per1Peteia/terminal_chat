import sys
import socket
import select

packet_bufs = dict()


def run(port):
    global packet_bufs

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen()
    potential_readers = {server_socket}
    potential_writers = set()
    potential_errs = set()

    ready_to_read, _, _ = select.select(
        potential_readers, potential_writers, potential_errs
    )

    while True:
        for skt in ready_to_read:
            if skt is server_socket:
                client_socket, addrinfo = server_socket.accept()
                # add client socket to selectable set
                potential_readers.add(client_socket)
                # assign a fresh buffer to the client socket
                packet_bufs[addrinfo[1]] = b''
            else:
                # TODO if client socket is readable, recv data
                pass


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

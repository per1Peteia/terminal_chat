from chatui import init_windows, read_command, print_message, end_windows
import sys
import socket


def usage():
    print('Usage: python3 chatlient.py [nickname] [host] [port]')


def main(argv):
    try:
        nick = argv[1]
        host = argv[2]
        port = int(argv[3])

    except:
        usage()
        return 1

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))


if __name__ == "__main__":
    sys.exit(main(sys.argv))

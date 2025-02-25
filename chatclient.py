from chatui import init_windows, read_command, print_message, end_windows
import sys


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

    run(nick, host, port)


if __name__ == "__main__":
    sys.exit(main(sys.argv))

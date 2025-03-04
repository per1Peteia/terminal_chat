from chat_ui import init_windows, read_command, print_message, end_windows
import threading
import sys
import socket
import utils


def usage():
    print('Usage: python3 chatlient.py [nickname] [host] [port]')


def recv_runner(sock):
    buf = b''

    while True:
        data = sock.recv(4096)
        buf = buf + data
        packets, buf = utils.process_socket_buffer(buf)

        for packet in packets:
            # handle complete packets according to type
            payload = utils.handle_packet(packet)
            if payload['type'] == 'join':
                print_message(f'*** {payload['nick']} has joined the chat')
            else:
                print_message(f"{payload['nick']}: {payload['message']}")

        buf = buf


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

    # before entering the threaded logic, send hello packet
    client_socket.sendall(utils.build_hello_packet(nick))

    init_windows()

    # worker thread (receiving)
    recv_thread = threading.Thread(
        target=recv_runner, args=(client_socket,), daemon=True)
    recv_thread.start()

    # main thread (sending)
    while True:
        cmd = read_command(f'{nick}> ')
        if cmd == '/q' or cmd == '/quit':
            print('closing connection')
            client_socket.close()
            break

    end_windows()


if __name__ == "__main__":
    sys.exit(main(sys.argv))

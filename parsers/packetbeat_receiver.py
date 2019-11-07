import socket
import threading
import json
# import signal

bind_ip = '0.0.0.0'
bind_port = 5129

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

def keyboardInterruptHandler(signal, frame):
    server.close()

def handle_client_connection(client_socket):
    while True:
        request = client_socket.recv(2048)
        try:
            beat = json.dumps(request)
            print(beat)
        except Exception as e:
            pass

def start():
    # --- Set signal handlers
    # signal.signal(signal.SIGINT, keyboardInterruptHandler)

    while True:
        client_sock, address = server.accept()
        print('Accepted connection from {}:{}'.format(address[0], address[1]))
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()

def run():
    print('[Packetbeat_Receiver] Listening on {}:{}'.format(bind_ip, bind_port))
    start()
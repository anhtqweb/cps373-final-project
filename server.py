import socket
import threading, wave, pyaudio ,pickle,struct
import youtube_dl, json
import os

# init
host_name = socket.gethostname()
host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
port = 3000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_ip, port))
server_socket.listen(5)
CHUNK = 1024

# TODO simulate lossy network

def main():
    while True:
        print("waiting for client...")
        client_socket,addr = server_socket.accept()
        print('server listening at',(host_ip, port))

        path = client_socket.recv(CHUNK)
        while not path:
            path = client_socket.recv(CHUNK)

        wf = wave.open(path.decode(), 'rb')

        print("Start streaming")
        data = wf.readframes(CHUNK)
        # if client_socket:
        while data != b"":
            client_socket.send(data)
            data = wf.readframes(CHUNK)
        
        print("End streaming")
        path = None
        client_socket.close()

main()    
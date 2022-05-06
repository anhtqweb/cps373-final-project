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
CHUNK_SIZE = 1024
CMD_PLAY = "0"
CMD_DOWNLOAD = "1"

# TODO simulate lossy network

def main():
    while True:
        print("Waiting for client...")
        client_socket,addr = server_socket.accept()
        print('SERVER listening at',(host_ip, port))

        cmd = client_socket.recv(CHUNK_SIZE)
        data = None
        while not data and not cmd:
            data = client_socket.recv(CHUNK_SIZE)
            cmd += data

        cmd = cmd.decode()
        if cmd[0] == CMD_PLAY:
            wf = wave.open(cmd[1:], 'rb')

            print("Start streaming")
            data = wf.readframes(CHUNK_SIZE)
            # if client_socket:
            while data != b"":
                client_socket.send(data)
                data = wf.readframes(CHUNK_SIZE)
        
            print("End streaming")
            wf.close()    
        elif cmd[0] == CMD_DOWNLOAD:
            url = cmd[1:]
            print(url)
            ydl_opts = {
			'outtmpl': 'songs/%(id)s.%(ext)s',
			'default_search': "ytsearch5",
			'format': 'bestaudio/best',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'wav',
				'preferredquality': '192',
				}],
			}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                client_socket.send(b"DONE")
        cmd = None
        client_socket.close()

main()    
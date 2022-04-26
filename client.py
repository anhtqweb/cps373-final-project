import socket,os
import threading, wave, pyaudio, pickle,struct
host_name = socket.gethostname()
host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
port = 3000
	
p = pyaudio.PyAudio()
CHUNK = 1024
stream = p.open(format=p.get_format_from_width(2),
				channels=2,
				rate=44100,
				output=True,
				frames_per_buffer=CHUNK)
				
# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_address = (host_ip,port)
print('server listening at',socket_address)
client_socket.connect(socket_address) 
print("CLIENT CONNECTED TO",socket_address)

data = client_socket.recv(4096)
while data != b"":
	try:
		stream.write(data)
		data = client_socket.recv(4096)
	except:
		
		break

stream.stop_stream()
stream.close()
p.terminate()
client_socket.close()
print('Audio closed')
os._exit(1)
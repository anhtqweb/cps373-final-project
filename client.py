import json
import socket
import threading, pyaudio
import youtube_dl
import queue

# declare constants
host_name = socket.gethostname()
host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
port = 3000
CHUNK_SIZE = 1024
CHANNELS = 2
RATE = 44100
SONG_LIST_FILE = "allsongs.json"
BUFFER_SIZE = 128
CMD_PLAY = "0"
CMD_DOWNLOAD = "1"

# buffer to store ahead chunks, simulate delays in network
def audio_download(url):
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	socket_address = (host_ip,port)
	print('SERVER listening at',socket_address)
	client_socket.connect(socket_address)
	print("CLIENT CONNECTED TO",socket_address)

	url = CMD_DOWNLOAD + url
	client_socket.send(url.encode())

	data = client_socket.recv(CHUNK_SIZE)
	while data != b"":
		data = client_socket.recv(CHUNK_SIZE)
	

def audio_stream(client_socket):
	# get rate from server before playing
	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(2),
					channels=CHANNELS,
					rate=RATE,
					output=True,
					frames_per_buffer=CHUNK_SIZE)
					

	print("Streaming audio...")
	# t1 = threading.Thread(target=getCmd, args=(stream,))
	# t1.start()
	buffer = queue.Queue()
	for i in range(BUFFER_SIZE):
		data = client_socket.recv(CHUNK_SIZE)
		if data != b"":
			buffer.put(data)

	i = 0
	while not buffer.empty():
		data = buffer.get()
		
	# while data != b"":
		stream.write(data)
		rec_data = client_socket.recv(CHUNK_SIZE)
		if rec_data != b"":
			buffer.put(rec_data)
	
	# t1.join()

	print("End streaming")
	stream.stop_stream()
	stream.close()
	print('Audio closed')
	p.terminate()
	# client_socket.close()
	print("Socket closed")

def main():
	


	while True:
		
		# create socket
		client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		socket_address = (host_ip,port)
		print('SERVER listening at',socket_address)
		client_socket.connect(socket_address)
		print("CLIENT CONNECTED TO",socket_address)

		print('Pick one option:')
		print('1. Show ALL songs')
		print('2. Play a song')
		print('3. Search and download')
		print('4. Exit')

		choice = int(input('>>> '))

		if choice == 3:

			client_socket.sendall('3'.encode())

			name = input('Enter the name of a song you want to search: ')

			client_socket.sendall(name.encode())

			options = client_socket.recv(CHUNK_SIZE)
			s = None
			while not s and not options:
				s = client_socket.recv(CHUNK_SIZE)
				options += s
			options = options.decode()
			print(options)

			download = input('Choose the song you want to download and play: ')
			client_socket.send(download.encode())

			cf_server = client_socket.recv(CHUNK_SIZE)
			cf = None
			while not cf and not cf_server:
				cf = client_socket.recv(CHUNK_SIZE)
				cf_server += cf
			cf_server = cf_server.decode()
			print(cf_server)

				
		elif choice == 1:
			'''songs_num = len(song_list)
			if songs_num == 0:
				print('Song list is empty')
			else:
				for i in range(songs_num):
					print(i+1, '.', song_list[i]["name"])'''
			client_socket.sendall('1'.encode())
			item_server = client_socket.recv(CHUNK_SIZE)
			
			item = None
			while not item and not item_server:
				item = client_socket.recv(CHUNK_SIZE)
				item_server += item
			item_server = item_server.decode()
			print(item_server)

		elif choice == 2:
			client_socket.sendall('2'.encode())

			item_server = client_socket.recv(CHUNK_SIZE)
			
			item = None
			while not item and not item_server:
				item = client_socket.recv(CHUNK_SIZE)
				item_server += item
			item_server = item_server.decode()
			print(item_server)

			play_choice = input('You want to play song number: ')

			client_socket.sendall(play_choice.encode())

			path = client_socket.recv(CHUNK_SIZE)
			p = None
			while not p and not path:
				p = client_socket.recv(CHUNK_SIZE)
				path += p
			path = path.decode()

			# request server for songs using path, open connection for streaming
			audio_stream(client_socket)


		elif choice == 4:
			break


main()
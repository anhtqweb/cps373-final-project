import socket
import pyaudio
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
	
def audio_stream(client_socket):
	# get rate from server before playing
	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(2),
					channels=CHANNELS,
					rate=RATE,
					output=True,
					frames_per_buffer=CHUNK_SIZE)
					
	print("Streaming audio...")

	# store BUFFER_SIZE chunks of data ahead of playback
	buffer = queue.Queue()
	for i in range(BUFFER_SIZE):
		data = client_socket.recv(CHUNK_SIZE)
		if data != b"":
			buffer.put(data)

	i = 0
	while not buffer.empty():
		data = buffer.get()
		stream.write(data)
		rec_data = client_socket.recv(CHUNK_SIZE)
		if rec_data != b"":
			buffer.put(rec_data)
	
	print("End streaming")
	stream.stop_stream()
	stream.close()
	print('Audio closed')
	p.terminate()
	print("Socket closed")

def recv_from_server(client_socket):
    # receive arguments from client
    res = client_socket.recv(CHUNK_SIZE)
    data = None
    while not data and not res:
        data = client_socket.recv(CHUNK_SIZE)
        res += data
    return res.decode()

def main():
	socket_address = (host_ip,port)
	print('SERVER listening at',socket_address)

	while True:
		# create socket
		client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
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

			options = recv_from_server(client_socket)
			print(options)

			download = input('Choose the song you want to download and play: ')
			client_socket.send(download.encode())

			cf_server = recv_from_server(client_socket)
			print(cf_server)

		elif choice == 1:
			client_socket.sendall('1'.encode())
			item_server = recv_from_server(client_socket)
			print(item_server)

		elif choice == 2:
			client_socket.sendall('2'.encode())

			item_server = recv_from_server(client_socket)
			print(item_server)

			play_choice = input('You want to play song number: ')

			client_socket.sendall(play_choice.encode())

			audio_stream(client_socket)

		elif choice == 4:
			break

main()
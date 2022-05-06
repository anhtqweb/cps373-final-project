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
	

def audio_stream(path):
	# get rate from server before playing
	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(2),
					channels=CHANNELS,
					rate=RATE,
					output=True,
					frames_per_buffer=CHUNK_SIZE)
					
	# create socket
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	socket_address = (host_ip,port)
	print('SERVER listening at',socket_address)
	client_socket.connect(socket_address)
	print("CLIENT CONNECTED TO",socket_address)

	# request audio stream from server
	path = CMD_PLAY + path
	client_socket.send(path.encode())

	print("Streaming audio...")
	# t1 = threading.Thread(target=getCmd, args=(stream,))
	# t1.start()
	buffer = queue.Queue()
	# for i in range(BUFFER_SIZE):
	data = client_socket.recv(CHUNK_SIZE)
		# buffer.put(data)

	# while not buffer.empty():
		# data = buffer.get()
	while data != b"":
		stream.write(data)
		data = client_socket.recv(CHUNK_SIZE)
	
	# t1.join()

	print("End streaming")
	stream.stop_stream()
	stream.close()
	print('Audio closed')
	p.terminate()
	client_socket.close()
	print("Socket closed")

def main():
	while True:
		with open(SONG_LIST_FILE) as data_file:
			json_file_data = json.load(data_file)

		song_list = []
		song_list.extend(json_file_data)

		print('Pick one option:')
		print('1. Show ALL songs')
		print('2. Play a song')
		print('3. Search and download')
		print('4. Exit')

		choice = int(input('>>> '))

		if choice == 3:
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

			name = input('Enter the name of a song you want to search: ')

			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				info = ydl.extract_info(name, download=False)

			for i,k in enumerate(info['entries']):
				print(i+1, '.', info['entries'][i]['title'])

			download = int(input('Choose the song you want to download and play: '))
			song_download_url = info['entries'][download-1]['webpage_url']
			song_download_id = info['entries'][download-1]['id']
			song_download_name = info['entries'][download-1]['title']
			song_download_obj = {"name": song_download_name, "id":song_download_id}
			song_list.append(song_download_obj)
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				# print(info['entries'][download-1]['webpage_url'])
				
				# ydl.download([song_download_url])
				audio_download(song_download_url)
			
			with open(SONG_LIST_FILE, 'w') as outfile:
				json.dump( song_list, outfile)

			path = "songs/" + song_download_id + ".wav"
			audio_stream(path)
				
		elif choice == 1:
			songs_num = len(song_list)
			if songs_num == 0:
				print('Song list is empty')
			else:
				for i in range(songs_num):
					print(i+1, '.', song_list[i]["name"])
		elif choice == 2:
			songs_num = len(song_list)
			if songs_num == 0:
				print('Song list is empty')
			else:
				for i in range(songs_num):
					print(i+1, '.', song_list[i]["name"])

				play_choice = int(input('You want to play song number: '))
				path = 'songs/' + song_list[play_choice - 1]["id"] + '.wav'
				# request server for songs using path, open connection for streaming
				audio_stream(path)

		elif choice == 4:
			break


main()
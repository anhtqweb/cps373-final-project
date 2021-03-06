import socket
import wave
import youtube_dl, json

# init
host_name = socket.gethostname()
host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
port = 3000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_ip, port))
server_socket.listen(5)
CHUNK_SIZE = 1024
SONG_LIST_FILE = "allsongs.json"

def recv_from_client(client_socket):
    # receive arguments from client
    res = client_socket.recv(CHUNK_SIZE)
    data = None
    while not data and not res:
        data = client_socket.recv(CHUNK_SIZE)
        res += data
    return res.decode()

def audio_stream(path, client_socket):
    # stream audio files to client
    wf = wave.open(path, 'rb')
    print("Start streaming")

    data = wf.readframes(CHUNK_SIZE)
    while data != b"":
        client_socket.send(data)
        data = wf.readframes(CHUNK_SIZE)

    print("End streaming")
    wf.close()

def main():
    while True:
        print("Waiting for client...")
        client_socket,addr = server_socket.accept()
        print('SERVER listening at',(host_ip, port))

        with open(SONG_LIST_FILE) as data_file:
            json_file_data = json.load(data_file)
        song_list = []
        song_list.extend(json_file_data)

        # receive operation type from client
        cmd = recv_from_client(client_socket)
        
        if cmd == '3':
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
            
            name = recv_from_client(client_socket)
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(name, download=False)
                
            s = ""
            for i,k in enumerate(info['entries']):
                s += str(i+1) + "." + info['entries'][i]['title'] + "\n"
            client_socket.sendall(s.encode())

            # receive download information sent from client
            download = int(recv_from_client(client_socket))
			
            song_download_url = info['entries'][download-1]['webpage_url']
            song_download_id = info['entries'][download-1]['id']
            song_download_name = info['entries'][download-1]['title']
            song_download_obj = {"name": song_download_name, "id":song_download_id}
            song_list.append(song_download_obj)

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([song_download_url])
                client_socket.send(b"DONE")

			
            with open(SONG_LIST_FILE, 'w') as outfile:
                json.dump( song_list, outfile)


        elif cmd == '2':
            songs_num = len(song_list)
            if songs_num == 0:
                client_socket.sendall('Song list is empty'.encode())
            else:
                msg = ""
                for i in range(songs_num):
                    msg += str(i+1) + '.' + song_list[i]["name"] + "\n"
                client_socket.sendall(msg.encode())

                play_choice = recv_from_client(client_socket)
                
                play_choice = int(play_choice)
                path = 'songs/' + song_list[play_choice - 1]["id"] + '.wav'
                client_socket.sendall(path.encode())

                audio_stream(path, client_socket)

        elif cmd == '1':
            songs_num = len(song_list)
            if songs_num == 0:
                client_socket.sendall('Song list is empty'.encode())
            else:
                songs = ""
                for i in range(songs_num):
                    songs += str(i+1) + "." + song_list[i]["name"] + "\n"
                client_socket.sendall(songs.encode())
        
        client_socket.close()
        cmd = None


        
        

main()    
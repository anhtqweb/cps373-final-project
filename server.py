import socket
import wave
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
SONG_LIST_FILE = "allsongs.json"

# TODO simulate lossy network

def main():
    while True:
        print("Waiting for client...")
        client_socket,addr = server_socket.accept()
        print('SERVER listening at',(host_ip, port))


        with open(SONG_LIST_FILE) as data_file:
            json_file_data = json.load(data_file)
        song_list = []
        song_list.extend(json_file_data)


        cmd = client_socket.recv(CHUNK_SIZE)
        data = None
        while not data and not cmd:
            data = client_socket.recv(CHUNK_SIZE)
            cmd += data
        cmd = cmd.decode()
        
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
            
            name = client_socket.recv(CHUNK_SIZE)
            song_name = None
            while not name and not song_name:
                song_name = client_socket.recv(CHUNK_SIZE)
                name += song_name
            name = name.decode()
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(name, download=False)
                
            s = ""
            for i,k in enumerate(info['entries']):
				
                s += str(i+1) + "." + info['entries'][i]['title'] + "\n"
            client_socket.sendall(s.encode())

			
            download = client_socket.recv(CHUNK_SIZE)
            dl_num = None
            while not download and not dl_num:
                dl_num = client_socket.recv(CHUNK_SIZE)
                download += dl_num
            download = int(download.decode())
                
			
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

                play_choice = client_socket.recv(CHUNK_SIZE)
                num = None
                while not num and not play_choice:
                    num = client_socket.recv(CHUNK_SIZE)
                    play_choice += num
                play_choice  = play_choice.decode()
                
                play_choice = int(play_choice)
                path = 'songs/' + song_list[play_choice - 1]["id"] + '.wav'
                client_socket.sendall(path.encode())

                wf = wave.open(path, 'rb')

                print("Start streaming")
                data = wf.readframes(CHUNK_SIZE)
                # if client_socket:
                while data != b"":
                    client_socket.send(data)
                    data = wf.readframes(CHUNK_SIZE)
            
                print("End streaming")
                wf.close()

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
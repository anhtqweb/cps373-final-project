import socket
import threading, wave, pyaudio ,pickle,struct

host_name = socket.gethostname()
host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
port = 3000

def audio_stream():
    server_socket = socket.socket()
    server_socket.bind((host_ip, port))

    server_socket.listen(5)
    CHUNK = 1024
    wf = wave.open("/home/trnqungnh/Downloads/audio.wav", 'rb')
    
    p = pyaudio.PyAudio()
    print('server listening at',(host_ip, port))
   
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

             

    client_socket,addr = server_socket.accept()
 
    data = None
    while True:
        if client_socket:
            while True:
              
                data = wf.readframes(CHUNK)
                a = pickle.dumps(data)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                
t1 = threading.Thread(target=audio_stream, args=())
t1.start()
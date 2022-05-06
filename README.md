# Server-Client Music Streaming Application
Final Project for Computer Networking

# Description
A music streaming application in Python using ```socket```, ```pyaudio```, ```youtube_dl```.

# Prerequisites
- ```python3```
- ```socket```
  - Should already come with ```python3```
- ```pyaudio``` (installation depends on operating system):
  - For Windows:
    
    ```
    pip install pipwin
    pipwin install pyaudio
    ```
  - For macOS:
    ```
    brew install portaudio
    pip install pyaudio
    ```
- ```youtube_dl```:
    ```
    pip install youtube_dl
    ```
- ```ffmpeg```:
  - For Windows: download executable of ```ffmpeg``` from https://www.gyan.dev/ffmpeg/builds/. Then, extract and put the executables to the ```Scripts``` folder of ```Python```.
  - For macOS:
# How to run
- First run the server.
```
python3 server.py
```
- Then run the client.
```
python3 client.py
```
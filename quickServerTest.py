import socket

PORT = 5000       # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((socket.gethostname(), PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
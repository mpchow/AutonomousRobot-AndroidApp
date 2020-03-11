import socket

PORT = 5003       # Port to listen on (non-privileged ports are > 1023)
HOST = ''


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((socket.gethostname(), PORT))
    print(socket.gethostname())
    s.listen()
    (conn, addr) = s.accept()
    print("Connected")
    with conn:
        print('Connected by', addr)
        input = s.recv(1024)
        print(input)
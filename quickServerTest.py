import socket

PORT = 5008       # Port to listen on (non-privileged ports are > 1023)
HOST = ''


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

    s.listen()
    (conn, addr) = s.accept()
    print("Connected")
    with conn:
        print('Connected by', addr)
        input = conn.recv(1024)
        print(input)
        input = conn.recv(1024)
        print(input)
        input = conn.recv(1024)
        print(input)
        s.close()
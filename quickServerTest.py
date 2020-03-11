import socket

PORT = 5008       # Port to listen on (non-privileged ports are > 1023)
HOST = ''

def parseJson(byteStream):
    # Decode UTF-8 bytes to unicode
    # To make valid JSON, replace single quotes with double quotes
    jsonStream = byteStream.decode('utf8').replace("'", '"')
    # Load JSON to Python list
    jsonList = json.load(jsonStream)
    parsedJson = json.dumps(jsonList, indent=4, sort_keys=True)
    print(parsedJson)

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
        parseJson(input)
        s.close()
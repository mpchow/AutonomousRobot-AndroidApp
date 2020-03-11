import socket
import json

PORT = 5016       # Port to listen on (non-privileged ports are > 1023)
HOST = ''

def parseJson(byteStream):
    # Decode UTF-8 bytes to unicode
    # To make valid JSON, replace single quotes with double quotes
    jsonStream = byteStream.decode('utf8').replace("'", '"')
    # Load JSON to Python list
    #jsonList = json.load(jsonStream)
    #parsedJson = json.dumps(jsonStream, indent=4, sort_keys=True)
    jsonObject = json.loads(jsonStream)
    print(jsonObject)
    print(jsonObject.get("Type"))
    #first_elem = jsonObject[0]
    #print(first_elem)
    #Type = first_elem['Type']
    #print(Type)
    #print(jsonObject['Type'])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

    s.listen()
    (conn, addr) = s.accept()
    print("Connected")
    with conn:
        print('Connected by', addr)
        input = conn.recv(1024)
        noValue = input

        while True:
            input = conn.recv(1024)
            if (input != noValue):
                parseJson(input)

        s.close()
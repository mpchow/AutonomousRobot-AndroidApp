import json
my_str = b"HELLO' :)"
parseJson(my_str)

def parseJson(byteStream):
    # Decode UTF-8 bytes to unicode
    # To make valid JSON, replace single quotes with double quotes
    jsonStream = byteStream.decode('utf8').replace("'", '"')
    # Load JSON to Python list
    jsonList = json.load(jsonStream)
    parsedJson = json.dumps(jsonList, indent=4, sort_keys=True)
    print(parsedJson)
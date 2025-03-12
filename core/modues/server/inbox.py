import socket, json, hashlib
from core.modues.init import load_server, load_keys
from core.modues.crypto.decrypt import decrypt

def inbox(args, self):
    host, port = load_server()
    _, public_key = load_keys()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps({
            "op" : 3,
            "data" : {
                "username" : self.pw[1],
                "password" : self.pw[0],
                "public_key" : public_key
            }
        }).encode())
        data = s.recv(1024)

    data = json.loads(data.decode())

    if data["status"] == 0:
        for message in data["messages"]:
            raw_msg = decrypt(message["message"])
            print(f"From: {message['from']}")
            print(f"Message: {raw_msg}")
            print()
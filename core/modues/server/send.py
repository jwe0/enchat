import socket, json
from core.modues.crypto.encrypt import encrypt
from core.modues.init import load_server, load_keys

def get_pub_key(recipient, username, password, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps({
            "op" : 2,
            "data" : {
                "username" : username,
                "password" : password,
                "recipient" : recipient
            }
        }).encode())
        data = s.recv(1024)

    data = json.loads(data.decode())

    if data["status"] == 1:
        return None 
    return data["public_key"]

def send(args, self):
    host, port = load_server()
    _, public_key = load_keys()

    recipient = args[0]
    message = args[1]

    recipient_pub_key = get_pub_key(recipient, self.pw[1], self.pw[0], host, port)

    if recipient_pub_key == None:
        print("Invalid request")
        return
    
    encrypted_message = encrypt(recipient_pub_key, message)

    payload = {
        "op" : 1,
        "data" : {
            "from" : self.pw[1],
            "recipient" : recipient,
            "message" : encrypted_message
        }
    }

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps(payload).encode())
        data = s.recv(1024)

    data = json.loads(data.decode())

    if data["status"] == 0:
        print("Message sent")



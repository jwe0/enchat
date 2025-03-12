import socket, json, hashlib
from core.modues.init import load_server, load_keys

def register(args, self):
    host, port = load_server()
    _, public_key = load_keys()

    username = args[0]
    password = args[1]

    payload = {
        "op" : 0,
        "data" : {
            "username" : username,
            "password" : password,
            "public_key" : public_key
        }
    }

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps(payload).encode())
        data = s.recv(1024)

    data = json.loads(data.decode())

    if data["status"] == 0:
        print("Registration successful")
        with open("core/assets/user.json", "w") as f:
            json.dump({
                "username" : username,
                "password" : hashlib.sha256(password.encode()).hexdigest(),
            }, f)
    elif data["status"] == 1:
        print("Username already exists")

    return data
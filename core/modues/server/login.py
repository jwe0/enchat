import socket, json, hashlib
from core.modues.init import load_server

def login(args, self):
    host, port = load_server()

    username = args[0]
    password = args[1]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps({
            "op" : 4,
            "data" : {
                "username" : username,
                "password" : password
            }
        }).encode())
        data = s.recv(1024)

    data = json.loads(data.decode())

    if data["status"] == 0:
        print("Login successful")
        with open("core/assets/user.json", "w") as f:
            json.dump({
                "username" : username,
                "password" : hashlib.sha256(password.encode()).hexdigest(),
            }, f)
        return {
            "status" : 0
        }
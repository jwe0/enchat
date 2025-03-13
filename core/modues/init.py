import os, json, hashlib, os, socket
from core.modues.crypto.keygen import key_gen

def verify_server(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((host, port))
            s.sendall(json.dumps({
                "op" : 10,
                "data" : {}
            }).encode())
            data = s.recv(1024)

        data = json.loads(data.decode())

        if data["status"] == 0:
            return True
    except:
        return False

def load_user():
    if os.path.exists("core/assets/user.json") == False:
        return None
    with open("core/assets/user.json", "r") as f:
        data = json.load(f)
    pw = input("Password: ")
    if hashlib.sha256(pw.encode()).hexdigest() != data["password"]:
        return None
    return pw, data["username"]

def load_server():
    if not os.path.exists("core/assets/server.json"):
        print("Server not set")
        return None, None
    with open("core/assets/server.json", "r") as f:
        data = json.load(f)
    if verify_server(data["host"], data["port"]) == False:
        print("Invalid server")
        return None, None
    return data["host"], data["port"]

def load_keys():
    with open("core/assets/keys.json", "r") as f:
        data = json.load(f)
    return data["private"], data["public"]

def init_files():
    files = [
        [
            "keys.json",
            key_gen
        ]
    ]

    for file in files:
        if not os.path.exists("core/assets/" + file[0]):
            with open("core/assets/" + file[0], "w") as f:
                f.write(json.dumps(file[1]()))

def init_dirs():
    dirs = ["assets"]
    for dir in dirs:
        if not os.path.exists("core/" + dir):
            os.mkdir("core/" + dir)

def init():
    init_dirs()
    init_files()
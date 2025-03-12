import os, json, hashlib, os
from core.modues.crypto.keygen import key_gen

def load_user():
    if os.path.exists("core/assets/user.json") == False:
        return None
    with open("core/assets/user.json", "r") as f:
        data = json.load(f)
    pw = input("Password: ")
    if hashlib.sha256(pw.encode()).hexdigest() != data["password"]:
        return None
    print(pw)
    return pw, data["username"]

def load_server():
    with open("core/assets/server.json", "r") as f:
        data = json.load(f)
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
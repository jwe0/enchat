import socket, threading, json, os, hashlib, sqlite3
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
class Functions:
    def __init__(self):
        ""

    def check(self, username):
        conn = sqlite3.connect("files/users.db")
        cursor = conn.cursor()
        response = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

        if len(response) > 0:
            conn.close()
            return True
        conn.close()
        return False
    
    def get_user_pub(self, args):
        
        username = args["username"]
        password = args["password"]
        recipient = args["recipient"]

        conn = sqlite3.connect("files/users.db")
        cursor = conn.cursor()

        verify = cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashlib.sha256(password.encode()).hexdigest())).fetchall()

        if len(verify) == 0:
            return {
                "status" : 1
            }

        response = cursor.execute("SELECT * FROM users WHERE username = ?", (recipient,)).fetchall()

        if len(response) == 0:
            return {
                "status" : 1
            }

        return {
            "status" : 0,
            "public_key" : response[0][3]
        }
    
    def send(self, args):
        from_user = args["from"]
        to_user = args["recipient"]
        message = args["message"]

        conn = sqlite3.connect("files/users.db")
        cursor = conn.cursor()

        verify = cursor.execute("SELECT * FROM users WHERE username = ?", (to_user,)).fetchall()

        if len(verify) == 0:
            return {
                "status" : 1
            }


        cursor.execute("INSERT INTO messages (from_user, to_user, message) VALUES (?, ?, ?)", (from_user, to_user, message))

        conn.commit()
        conn.close()

        return {
            "status" : 0
        }
    
    def get_inbox(self, args):
        username = args["username"]
        password = args["password"]

        conn = sqlite3.connect("files/users.db")
        cursor = conn.cursor()

        verify = cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashlib.sha256(password.encode()).hexdigest())).fetchall()

        if len(verify) == 0:
            return {
                "status" : 1
            }

        response = cursor.execute("SELECT * FROM messages WHERE to_user = ?", (username,)).fetchall()

        if len(response) == 0:
            return {
                "status" : 1
            }
        
        res = []

        for i in response:
            id    = i[0]
            from_ = i[1]
            to    = i[2]
            msg   = i[3]

            res.append({
                "id" : id,
                "from" : from_,
                "to" : to,
                "message" : msg
            })

        conn.close()

        return {
            "status" : 0,
            "messages" : res
        }


    def register(self, args):

        username = args["username"]
        password = args["password"]
        public_key = args["public_key"]

        if self.check(username):
            return {
                "status" : 1
            }
        
        conn = sqlite3.connect("files/users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, public_key) VALUES (?, ?, ?)", (username, hashlib.sha256(password.encode()).hexdigest(), public_key))
        conn.commit()
        conn.close()

        return {
            "status" : 0
        }
    
    def login(self, args):
        username = args["username"]
        password = args["password"]

        conn = sqlite3.connect("files/users.db")
        cursor = conn.cursor()

        response = cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashlib.sha256(password.encode()).hexdigest())).fetchall()

        if len(response) > 0:
            conn.close()
            return {
                "status" : 0
            }

        conn.close()
        return {
            "status" : 1
        }

class Server:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 1234
        self.funcs = Functions()
        self.start_server()

    def evaluate(self, data, sock):
        data = json.loads(data)
        commands = {
            0 : self.funcs.register,
            1 : self.funcs.send,
            2 : self.funcs.get_user_pub,
            3 : self.funcs.get_inbox,
            4 : self.funcs.login
        }
        if data["op"] in commands:
            response = commands[data["op"]](data["data"])
            sock.sendall(json.dumps(response).encode())

        
            

    def handle_client(self, conn, addr):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            self.evaluate(data, conn)
    
    def start_server(self):
        print(f"Server started on {self.host}:{self.port}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    Server()
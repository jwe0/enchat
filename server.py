import socket, threading, json, os, hashlib
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class Functions:
    def __init__(self):
        pass

    def check(self, username):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_API")
        supabse = Client(url, key)

        response = (
            supabse.table("users")
            .select("*")
            .eq("username", username)
            .execute()
        )

        if len(response.data) > 0:
            return True

        return False
    
    def get_user_pub(self, args):
        
        username = args["username"]
        password = args["password"]
        recipient = args["recipient"]

        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_API")
        supabse = Client(url, key)

        verify = (
            supabse.table("users")
            .select("*")
            .eq("username", username)
            .eq("password", hashlib.sha256(password.encode()).hexdigest())
            .execute()
        )

        if len(verify.data) == 0:
            return {
                "status" : 1
            }

        response = (
            supabse.table("users")
            .select("publickey")
            .eq("username", recipient)
            .execute()
        )

        if len(response.data) == 0:
            return {
                "status" : 1
            }

        return {
            "status" : 0,
            "public_key" : response.data[0]["publickey"]
        }
    
    def send(self, args):
        from_user = args["from"]
        to_user = args["recipient"]
        message = args["message"]

        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_API")
        supabse = Client(url, key)

        response = (
            supabse.table("messages")
            .insert({
                "from" : from_user,
                "to" : to_user,
                "message" : message
            })
            .execute()
        )

        return {
            "status" : 0
        }
    
    def get_inbox(self, args):
        username = args["username"]
        password = args["password"]

        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_API")
        supabse = Client(url, key)

        verify = (
            supabse.table("users")
            .select("*")
            .eq("username", username)
            .eq("password", hashlib.sha256(password.encode()).hexdigest())
            .execute()
        )

        if len(verify.data) == 0:
            return {
                "status" : 1
            }

        response = (
            supabse.table("messages")
            .select("*")
            .eq("to", username)
            .execute()
        )

        return {
            "status" : 0,
            "messages" : response.data
        }


    def register(self, args):

        username = args["username"]
        password = args["password"]
        public_key = args["public_key"]

        if self.check(username):
            return {
                "status" : 1
            }
        
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_API")
        supabse = Client(url, key)

        response = (
            supabse.table("users")
            .insert({
                "username" : username,
                "password" : hashlib.sha256(password.encode()).hexdigest(),
                "publickey" : public_key
            })
            .execute()
        )

        return {
            "status" : 0
        }
    
    def login(self, args):
        username = args["username"]
        password = args["password"]

        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_API")
        supabse = Client(url, key)

        response = (
            supabse.table("users")
            .select("*")
            .eq("username", username)
            .eq("password", hashlib.sha256(password.encode()).hexdigest())
            .execute()
        )

        if len(response.data) > 0:
            return {
                "status" : 0
            }

        return {
            "status" : 1
        }

class Server:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 12345
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
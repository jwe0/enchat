import json
from core.modues.init import init, load_user

from core.modues.server.register import register
from core.modues.server.send import send
from core.modues.server.inbox import inbox


class Main:
    def __init__(self):
        init()
        self.pw = load_user()

    def set_host(self, args, self_):
        with open("core/assets/server.json", "w") as f:
            f.write(json.dumps({"host" : args[0], "port" : int(args[1])}))

    def evaluate(self, args):
        self.commands = {
            "register" : {
                "args" : ["<username>", "<password>"],
                "func" : register
            },
            "set" : {
                "args" : ["<host>", "<port>"],
                "func" : self.set_host
            },
            "send" : {
                "args" : ["<recipient>", "<message>"],
                "func" : send
            },
            "inbox" : {
                "args" : ["(from)"],
                "func" : inbox
            }
        }
        if args[0] in self.commands:
            if len(args) - 1 != len(self.commands[args[0]]["args"]):
                print("Invalid arguments")
                print(self.commands[args[0]]["args"])
                return
            self.commands[args[0]]["func"](args[1:], self)

    def main(self):
        while True:
            command = input("> ")

            args = command.split(" ")
            if len(args) > 0:
                self.evaluate(args)

if __name__ == "__main__":
    main = Main()
    main.main()
import socket
import json

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8000

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP, TARGET_PORT)
        self.sock.connect(self.server_address)
        self.token_id = ""
        self.realm_id = ""

    def proses(self, cmdline):
        j = cmdline.split(" ")
        try:
            command = j[0].strip()
            if (command == 'register'):
                username = j[1].strip()
                password = j[2].strip()
                return self.register(username, password)
            elif (command == 'creategroup'):
                groupname = j[1].strip()
                return self.create_group(groupname)
            elif (command == 'auth'):
                username = j[1].strip()
                password = j[2].strip()
                return self.login(username, password)
            elif (command == 'sendprivate'):
                usernameto = j[1].strip()
                message = ""
                for w in j[2:]:
                    message = "{} {}" . format(message, w)
                return self.sendmessage(usernameto, message)
            elif (command == 'sendgroup'):
                groupto = j[1].strip()
                message = ""
                for w in j[2:]:
                    message = "{} {}" . format(message, w)
                return self.sendmessage_group(groupto, message)
            elif (command == 'inbox'):
                return self.inbox()
            elif (command == 'inboxgroup'):
                groupname = j[1].strip()
                return self.inbox_group(groupname)
            else:
                return "*Maaf, command tidak benar"
        except IndexError:
            return "-Maaf, command tidak benar"

    def sendstring(self, string):
        try:
            self.sock.sendall(string.encode())
            receivemsg = ""
            while True:
                data = self.sock.recv(4096)
                print("diterima dari server", data)
                if (data):
                    # data harus didecode agar dapat di operasikan dalam bentuk string
                    receivemsg = "{}{}" . format(receivemsg, data.decode())
                    if receivemsg[-4:] == '\r\n\r\n':
                        print("end of string")
                        return json.loads(receivemsg)
        except:
            self.sock.close()
            return {'status': 'ERROR', 'message': 'Gagal'}

    def register(self, username, password):
        string = "register {} {} \r\n" . format(username, password)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "username {} successfully registered " .format(username)
        else:
            return "Error, {}" . format(result['message'])
        
    def create_group(self, groupname):
        string = "creategroup {} \r\n" . format(groupname)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "groupname {} successfully created " .format(groupname)
        else:
            return "Error, {}" . format(result['message'])
        
    def login(self, username, password):
        string = "auth {} {} \r\n" . format(username, password)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            self.token_id = result['token_id']
            self.realm_id = result['realm_id']
            return "username {} logged in, token {} " .format(username, self.token_id)
        else:
            return "Error, {}" . format(result['message'])

    def sendmessage(self, usernameto="xxx", message="xxx"):
        if (self.token_id == ""):
            return "Error, not authorized"
        string = "sendprivate {} {} {} \r\n" . format(
            self.token_id, usernameto, message)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "message sent to {}" . format(usernameto)
        else:
            return "Error, {}" . format(result['message'])

    def sendmessage_group(self, groupto="xxx", message="xxx"):
        if (self.token_id == ""):
            return "Error, not authorized"
        string = "sendgroup {} {} {} \r\n" . format(
            self.token_id, groupto, message)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "message sent to {}" . format(groupto)
        else:
            return "Error, {}" . format(result['message'])

    def inbox(self):
        if (self.token_id == ""):
            return "Error, not authorized"
        string = "inbox {} \r\n" . format(self.token_id)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}" . format(json.dumps(result['messages']))
        else:
            return "Error, {}" . format(result['message'])

    def inbox_group(self, groupname):
        if (self.token_id == ""):
            return "Error, not authorized"
        string = "inboxgroup {} {}\r\n" . format(self.token_id, groupname)
        result = self.sendstring(string)
        if result['status'] != 'OK':
            # return "{}" . format(json.dumps(result['messages'])):
            return "Error, {}" . format(result['message'])


if __name__ == "__main__":
    cc = ChatClient()
    while True:
        cmdline = input("Command {}:" . format(cc.token_id))
        print(cc.proses(cmdline))

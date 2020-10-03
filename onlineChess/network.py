import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "73.157.134.80"
        self.port = 5000
        self.addr = (self.server, self.port)
        self.player_number = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, message):
        try:
            self.client.send(str.encode(message))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

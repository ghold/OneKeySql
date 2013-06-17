import socket

class OkClient(object):
    def __init__(self):
        HOST, PORT = "localhost", 8089
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        
    def sendMessage(self, message):
        try:
            self.sock.sendall(bytes(message, 'ascii'))
            response = str(self.sock.recv(1024), 'ascii')
            print("Received: {}".format(response))
        finally:
            self.sock.close()
            
if __name__ == "__main__":
    myClient = OkClient()
    myClient.sendMessage("hello world")

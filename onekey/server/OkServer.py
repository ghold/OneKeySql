import socketserver
import threading

class OkBaseRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{%s}:{%s}"%(cur_thread.name, data), 'ascii')
        self.request.sendall(response)
        
    def requestConfig(self):
        

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 8089
    
    server = ThreadedTCPServer((HOST, PORT), OkBaseRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)

    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    server.serve_forever()

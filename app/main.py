import os
import socket  
from threading import Thread
import sys
from pathlib import Path


class server_side():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.running = True
        # self.data = data
        self.start_server()
    
    def start_server(self):
        with socket.create_server((self.host, self.port), reuse_port=True) as server:
            print(f"Server is open on port {self.port}")
            while self.running:
                connection, address = server.accept()
                # To make it concurrent, we spawn a thread for each client
                thread = Thread(target=self.handle_client, args=(connection,))
                thread.start()     
    
    def handle_client(self, connection):
        with connection :
            try:
                self.data = {
                        "Status_Line" : "HTTP/1.1 200 OK",
                        "Content-Type" : None,
                        "Content-Length" : None,
                        "Content" : None,
                        "body" : None,
                    }
                recv = connection.recv(1024)
                if not recv:
                    return
                self.user_request(recv)
                if self.data["Content"] is not None:
                    respond = f"{self.data["Status_Line"]}\r\nContent-Type: {self.data["Content-Type"]}\r\nContent-Length: {self.data["Content-Length"]}\r\n\r\n{self.data["Content"]}".encode()
                else:
                    respond = f"{self.data["Status_Line"]}\r\n\r\n".encode()
                connection.sendall(respond)
                connection.settimeout(10.0)
          
            except Exception as e:
                print(e)
             
        
    def user_request(self, recv):
        header, body = recv.decode().split("\r\n\r\n", 1)
        header = header.split("\r\n")
        # parsing safety
        if not header: return b"HTTP/1.1 400 Bad Request\r\n\r\n"
        method = header[0].split(" ")[0]
        print(method)
        if method == "GET":
            self.get_method_requests(header, body)
        elif method == "POST":
            self.post_method_requests(header, body)
        else:
            self.data["Status_Line"] = "HTTP/1.1 404 Not Found"
            return self.data
     
        
    def get_method_requests(self, header, body):
        path = header[0].split(' ')[1]
        paths = path.split("/")
        
        for line in header:
            if line.startswith("User-Agent: "):
                user_agent = line.split("User-Agent: ")[1]
        
        if paths[1] == "echo":
            echo = paths[2]
            self.data["Content-Length"] = len(echo)
            self.data["Content"] = echo
            self.data["Content-Type"] = "text/plain"
            return 
        
        elif paths[1] == "user-agent":
            self.data["Content-Length"] = len(user_agent)
            self.data["Content"] = user_agent
            self.data["Content-Type"] = "text/plain"
            return 
        
        elif path == "/":
            return
        
        elif paths[1] == "quit":
            self.running =  False
            return 
        
        elif paths[1] == "files" and Path(f"/{sys.argv[2]}/{paths[2]}").exists():
            with open(f"/{sys.argv[2]}/{paths[2]}", 'r') as file:
                content = file.read()
                self.data["Content-Length"] = len(content)
                self.data["Content"] = content
                self.data["Content-Type"] = "application/octet-stream"
                return
        
        else: 
            self.data["Status_Line"] = "HTTP/1.1 404 Not Found"
            return 
        
    def post_method_requests(self, header, body):
        path = header[0].split(' ')[1]
        filename = path.split("/")[-1]
        base_dir = sys.argv[2] if len(sys.argv) > 2 else "."
        full_path = os.path.join(base_dir, filename)
        try:
            with open(full_path, "w") as file:
                file.write(body)
                self.data["Content-Type"] = "text/plain"
                self.data["Status_Line"] = "HTTP/1.1 201 Created"
            return
        except Exception as e:
            print(e)
            
        
        
        
               

def main():
    server_side("localhost", 4221)
     

if __name__ == "__main__":
    main()

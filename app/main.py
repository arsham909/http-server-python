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
                self.header_data = {
                        "Status_Line" : "HTTP/1.1 200 OK",
                        "Content-Type" : None,
                        "Content-Length" : None,
                    }
                self.body_data = {"Content" : "",}
                
                recv = connection.recv(1024)
                if not recv:
                    return
                self.user_request(recv)
                if self.body_data["Content"] is not None:
                    respond = ""
                    for i in self.header_data.keys():
                        if self.header_data[i] is not None:
                            respond += f"{i} {self.header_data[i]}\r\n"
                        # respond = f"{self.header_data["Status_Line"]}\r\nContent-Type: {self.header_data["Content-Type"]}\r\nContent-Length: {self.header_data["Content-Length"]}\r\n\r\n{self.header_data["Content"]}".encode()
                    respond += f"\r\n{self.body_data["Content"]}"
                else:
                    respond = f"{self.header_data["Status_Line"]}\r\n\r\n"
                connection.sendall(respond.encode())
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
            self.header_data["Status_Line"] = "HTTP/1.1 404 Not Found"
            return self.header_data
     
        
    def get_method_requests(self, header, body):
        print(header)
        path = header[0].split(' ')[1]
        paths = path.split("/")
        
        for line in header:
            if line.startswith("User-Agent: "):
                user_agent = line.split("User-Agent: ")[1]
        
        if paths[1] == "echo":
            echo = paths[2]
            self.content_encoding(header)
            self.header_data["Content-Length"] = len(echo)
            self.header_data["Content"] = echo
            self.header_data["Content-Type"] = "text/plain"
            return 
        
        elif paths[1] == "user-agent":
            self.header_data["Content-Length"] = len(user_agent)
            self.body_data["Content"] = user_agent
            self.header_data["Content-Type"] = "text/plain"
            return 
        
        elif path == "/":
            return
        
        elif paths[1] == "quit":
            self.running =  False
            return 
        
        elif paths[1] == "files" and Path(f"/{sys.argv[2]}/{paths[2]}").exists():
            with open(f"/{sys.argv[2]}/{paths[2]}", 'r') as file:
                content = file.read()
                self.header_data["Content-Length"] = len(content)
                self.body_data["Content"] = content
                self.header_data["Content-Type"] = "application/octet-stream"
                return
        
        else: 
            self.header_data["Status_Line"] = "HTTP/1.1 404 Not Found"
            return 
        
    def post_method_requests(self, header, body):
        path = header[0].split(' ')[1]
        filename = path.split("/")[-1]
        base_dir = sys.argv[2] if len(sys.argv) > 2 else "."
        full_path = os.path.join(base_dir, filename)
        try:
            with open(full_path, "w") as file:
                file.write(body)
                self.header_data["Content-Type"] = "text/plain"
                self.header_data["Status_Line"] = "HTTP/1.1 201 Created"
            return
        except Exception as e:
            print(e)
    
    def content_encoding(self, header):
        for line in header:
            if "Accept-Encoding" in line:
                encoding = line.splt("Accept-Encoding", 1)[1]
            if encoding == "gzip":
                self.header_data["Content-Encoding"] = "gzip"
            
                
            
        
        
        
               

def main():
    server_side("localhost", 4221)
     

if __name__ == "__main__":
    main()

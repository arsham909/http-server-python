import socket  
from threading import Thread
import sys
from pathlib import Path

data= {
    "Status_Line" : "HTTP/1.1 200 OK",
    "Content-Type" : None,
    "Content-Length" : None,
    "Content" : None,
    "body" : None,
}

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
        request = recv.decode().split('\r\n')
        # print(request)
        # parsing safety
        if not request: return b"HTTP/1.1 400 Bad Request\r\n\r\n"
        method = request[0].split(" ")[0]
        print(request)
        if method == "GET":
            self.get_method_requests(request)
        elif method == "POST":
            self.post_method_requests(request)
        else:
            self.data["Status_Line"] = "HTTP/1.1 404 Not Found"
            return self.data
     
        
    def get_method_requests(self, request):
        path = request[0].split(' ')[1]
        paths = path.split("/")
        print(request)
        for line in request:
            if line.startswith("User-Agent: "):
                user_agent = line.split("User-Agent: ")[1]
        
        if paths[1] == "echo":
            echo = paths[2]
            self.data["Content-Length"] = len(echo)
            self.data["Content"] = echo
            return 
        
        elif paths[1] == "user-agent":
            self.data["Content-Length"] = len(user_agent)
            self.data["Content"] = user_agent
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
        
    def post_method_requests(self, request):
        path = request[0].split(' ')[1]
        paths = path.split("/")
        filename= paths[-1]
        body = request[7]   
        if paths[1] == "files" and Path(f"/{sys.argv[2]}").exists():
            with open(filename, "w") as file:
                file.write(body)
                self.data["Status_Line"] = "HTTP/1.1 201 Created"
            return
            
        #     with open(f"/{sys.argv[2]}/{paths[2]}", 'r') as file:
        #         content = file.read()
        #         self.data["Status_Line"] = "HTTP/1.1 201 Created"
        #         self.data["Content-Length"] = len(content)
        #         self.data["Content"] = content
        #         self.data["Content-Type"] = "application/octet-stream"
        #         return
    
        
        
        
               

def main():
    server_side("localhost", 4221)
     

if __name__ == "__main__":
    main()

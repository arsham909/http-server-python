import os
import socket  
from threading import Thread
import sys
from pathlib import Path
import gzip  


class server_side():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.running = True
        self.base_dir = sys.argv[2] if len(sys.argv) > 2 else "."
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
        connection.settimeout(10.0)
        with connection :
            try:
                raw_request = connection.recv(1024)
                if not raw_request:
                    return
                respond_bytes = self.process_request(raw_request.decode())
                connection.sendall(respond_bytes)
                
            except Exception as e:
                print(e)
    
    def process_request(self, raw_request):
        try:
            header_section, body_section = raw_request.split("\r\n\r\n",1)
        except ValueError:
            return b"HTTP/1.1 400 Bad Request\r\n\r\n"
        
        header_lines = header_section.split("\r\n")
        if not header_lines: 
            return b"HTTP/1.1 400 Bad Request\r\n\r\n"
        
        request_line = header_lines[0].split(" ")
        method = request_line[0]
        path = request_line[1]
        headers = {"Status_Line" : "HTTP/1.1 200 OK",}
        headers = self.content_encoding(header_lines, headers)
        body = b""
        if method == "GET":
            headers, body = self.get_method_requests(path, header_lines, headers, body)
        elif method == "POST":
            headers, body = self.post_method_requests(path, body_section, headers, body)
        else:
            headers["Status_Line"] = "HTTP/1.1 405 Method Not Allowed"
            return headers
        
        #build the final respond
        return self.build_respond(headers, body)
    
    def content_encoding(self, header_lines, headers,):
        for line in header_lines:
            if "Accept-Encoding: " in line:
                encoding = line.split(" ")
                print(encoding)
                if "gzip" in encoding:
                    headers["Content-Encoding"] = "gzip"
        return headers

     
        
    def get_method_requests(self, path, header_lines, headers, body):
        paths = path.split("/")

        if path == "/":
            pass # Keep 200 OK default
            
        elif len(paths) > 1 and paths[1] == "echo":
            echo_str = paths[2] if len(paths) > 2 else ""
            headers["Content-Type"] = "text/plain"
            body = echo_str.encode() # Convert string to bytes
            
        elif len(paths) > 1 and paths[1] == "user-agent":
            user_agent = ""
            for line in header_lines:
                if line.startswith("User-Agent: "):
                    user_agent = line.replace("User-Agent: ", "")
            headers["Content-Type"] = "text/plain"
            body = user_agent.encode()

        elif len(paths) > 1 and paths[1] == "quit":
            self.running = False
            
        elif len(paths) > 2 and paths[1] == "files":
            filename = paths[2]
            # Safely join the paths
            full_path = os.path.join(self.base_dir, filename)
            
            if os.path.exists(full_path):
                # Read as binary (rb) to support any file type
                with open(full_path, 'rb') as file:
                    body = file.read() 
                headers["Content-Type"] = "application/octet-stream"
            else:
                headers["Status_Line"] = "HTTP/1.1 404 Not Found"
        else:
            headers["Status_Line"] = "HTTP/1.1 404 Not Found"

        return headers, body
    
        
    def post_method_requests(self, path, body_section, headers, body):
        paths = path.split("/")
        if len(paths) > 2 and paths[1] == "files":
            filename = paths[-1]
            full_path = os.path.join(self.base_dir, filename)
            
            try:
                # Write as text for now, assuming the test is sending text
                with open(full_path, "w") as file:
                    file.write(body_section)
                headers["Status_Line"] = "HTTP/1.1 201 Created"
            except Exception as e:
                print(f"File write error: {e}")
                headers["Status_Line"] = "HTTP/1.1 500 Internal Server Error"
        else:
            headers["Status_Line"] = "HTTP/1.1 404 Not Found"
            
        return headers, body
            
                
    def build_respond(self, headers, body_bytes):
        if body_bytes:
            headers["Content-Length"] = len(body_bytes)
        
        respond_str = headers.pop("Status_Line") + "\r\n"
        
        for key, value in headers.items():
            respond_str += f"{key}: {value}\r\n"
        
        respond_str += "\r\n"
        return respond_str.encode() + body_bytes
    
    
def main():
    server_side("localhost", 4221)
     

if __name__ == "__main__":
    main()

import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    with socket.create_server(("localhost",4221), reuse_port=True) as server:
        while True:
            server.listen()
            conncetion, address = server.accept()
            recv = conncetion.recv(1024)
            
            request = recv.decode().split('\r\n')
            path = request[0].split(' ')[1]
            paths = path.split("/")            
            if path == "/":
                conncetion.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
                break
            elif paths[1] == "echo":
                echo = paths[2]
                data = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo)}\r\n\r\n{echo}"
                conncetion.sendall(data.encode())
            else:
                conncetion.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
                break
                
        
        


if __name__ == "__main__":
    main()

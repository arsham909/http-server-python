import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    with socket.create_server(("localhost",4221), reuse_port=True) as server:
        server.listen()
        conncetion, address = server.accept()
        recv = conncetion.recv(1024)
        
        request = recv.decode().split('\r\n')
        path = request[0].split(' ')
        if path[1] == "/":
            conncetion.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        elif "/echo/" in path[1]:
            conncetion.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 4\r\n\r\nabcd")
        else:
            conncetion.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
            
        
        


if __name__ == "__main__":
    main()

import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # TODO: Uncomment the code below to pass the first stage
    #
    # server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client
    with socket.create_server(("localhost",8000), reuse_port=True) as server:
        conncetion, address = server.accept()
        # print(f"conncetion is working {conncetion}")
        
        conncetion.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        
        


if __name__ == "__main__":
    main()

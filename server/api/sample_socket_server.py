import socket


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(1)  # Listen for incoming connections

    print("Waiting for incoming connections...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print("Connected to", client_address)

            # Handle communication with the client
            handle_client(client_socket)

    except KeyboardInterrupt:
        print("Server terminated by user.")

    finally:
        server_socket.close()


def handle_client(client_socket):
    try:
        # Example communication with the client
        data_to_send = "Hello, client!"
        client_socket.send(data_to_send.encode())

        received_data = client_socket.recv(1024).decode()
        print("Received data:", received_data)

    except Exception as e:
        print("Error handling client:", str(e))

    finally:
        client_socket.close()


if __name__ == "__main__":
    run_server()

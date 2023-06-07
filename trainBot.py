import socket

def send_command(command):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = ('localhost', 4445)
    client_socket.connect(server_address)

    try:
        while True:
            # Send the command to the server
            client_socket.sendall(command.encode())

            # Receive the response from the server
            response = client_socket.recv(1024).decode().strip()

            if response != "No response.":
                # Print the response
                print("{}".format(response))

            # Check if exit command received
            if command == "exit":
                break

            # Read input for the next command
            command = input("$ ")

    except KeyboardInterrupt:
        print("Client interrupted.")

    # Close the connection
    client_socket.close()

if __name__ == '__main__':
    # Read input for the first command
    command = input("$ ")

    send_command(command)

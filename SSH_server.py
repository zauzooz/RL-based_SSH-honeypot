import socket
import os
import json
from learner.environment import LearningEnvironment
from learner.RL_instance import ReinforcementAlgorithm
from learner.RL_log import write_log


def start_server():
    def load_json(dir_path: str):
        file_names = []

        # Iterate over all the files and folders within the given directory
        for root, dirs, files in os.walk(dir_path):
            # Append the file names to the list
            for file in files:
                file_names.append(os.path.join(root, file))
        if file_names:
            last_file_path = file_names[-1]
            dir_path = os.path.dirname(last_file_path)
            file_name = os.path.basename(last_file_path)
            return json.load(open(os.path.join(dir_path, file_name), "r"))
        else:
            return {}
    
    write_log("[terminal] Start stupidPot.")

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 4445)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print("Server listening on {}:{}".format(*server_address))

    try:
        while True:
            # Wait for a client to connect
            print("Waiting for a connection...")
            client_socket, client_address = server_socket.accept()
            print("Accepted connection from {}:{}".format(*client_address))

            # Initialize RL algorithm
            alg = ReinforcementAlgorithm(
                alg='Q-Learning',
                q_table=load_json("learner/var/rl/q-table/")
            )

            # Initialize RL environment
            env = LearningEnvironment(
                rlalg=alg, 
                learning=True,
                explore_states=load_json("learner/var/rl/explore_states/")
            )

            try:
                while True:
                    # Receive data from the client
                    command = client_socket.recv(2048).decode().strip()

                    # Check if exit command received
                    if command == "exit":
                        output = env.command_receive(command)
                        env.connection_close()
                        write_log("[terminal] End session.")
                        break

                    # Process the command
                    response = env.command_receive(command)

                    if response == "":
                        response = "No response."

                    # Send the response back to the client
                    client_socket.sendall(response.encode())

            except (ConnectionResetError, BrokenPipeError):
                print("Client disconnected unexpectedly.")
                env.connection_close()

            # Close the connection
            client_socket.close()

    except KeyboardInterrupt:
        print("Server interrupted. Closing the server socket.")
        server_socket.close()
        write_log("[terminal] End session.")


if __name__ == '__main__':
    start_server()

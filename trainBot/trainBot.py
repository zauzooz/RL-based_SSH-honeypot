import os
import json
import socket
import pandas
from trainBotlog import write_log
from trainset_gen import COMMANDS
from trainBotaccuracylog import accuracy_log
from datetime import datetime

THRESHOLD = 0.7 # percent match
PORT = 4445

def load_dataset_path(dir_path: str) -> dict:
    file_names = []

    # Iterate over all the files and folders within the given directory
    for root, dirs, files in os.walk(dir_path):
        # Append the file names to the list
        for file in files:
            file_names.append(os.path.join(root, file))
    return file_names

def get_file_paths(dir_path):
    files_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            files_list.append(dir_path + "/" + file)
    return files_list

def percent_match(str1: str, str2: str) -> float:

    def format_string(input_str):
        # Split the input string by whitespace into a list of words
        words = input_str.split()

        # Join the words with a single space in between
        formatted_str = " ".join(words)

        return formatted_str

    if str1 == str2:
        return 1

    # format string to 1 space between 2 words.
    str1 = format_string(str1)
    str2 = format_string(str2)

    # help 2 string that match
    while len(str1) > len(str2):
        str2 += " "
    while len(str2) > len(str1):
        str1 += " "
    
    match_count = sum(c1 == c2 for c1, c2 in zip(str1, str2))
    percentage = match_count / len(str1)
    return percentage

def start_server():

    PREDICT = {}

    """
        - PREDICT is a dictionary with key is dataset name and value is 0 or 1,
        with 0 mean the RL honeypot responses a non-desired output. Otherwise, 1
        means is RL honeypot like a real SSH.
    """

    # Get the current datetime
    now = datetime.now()

    # Format the datetime as "d-m-y_h-m-s-ms"
    formatted_datetime = now.strftime("%d-%m-%y_%H-%M-%S-%f")

    def send_command_recieve_output(client_socket, command:str) -> str:
        response = ""
        # Send the command to the server
        client_socket.sendall(command.encode())

        # Receive the response from the server
        response = client_socket.recv(1024).decode().strip()
        return response
    
    write_log(formatted_datetime,"TRAINING SESSION START.")
    paths_list = load_dataset_path("trainBot/trainset")
    for path, ith in list(zip(paths_list, [i+1 for i in range(len(paths_list))])):

        PREDICT[path] = 0

        FULL_COMMAND = True
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        server_address = ('localhost', PORT)
        client_socket.connect(server_address)
        write_log(formatted_datetime,f"Access to localhost at {PORT}.")

        write_log(formatted_datetime,f"Train set {ith}, path: {paths_list}")
        cmd_seq = json.load(
            open(path, "r")
        )
        seqs = list(cmd_seq.keys())
        write_log(formatted_datetime,f"Numbers of sequence command: {len(seqs)}")

        for seq in seqs:
            command = cmd_seq[seq]["cmd"]
            write_log(formatted_datetime,f"Command: {command}")

            output_true = cmd_seq[seq]["output"]
            write_log(formatted_datetime,f"Desired ouput: {output_true}")

            # send and recieved command from RL.
            output_pred = send_command_recieve_output(client_socket, command)
            if output_pred == 'No response.':
                 output_pred = ""
            write_log(formatted_datetime,f"Received output: {output_pred}")

            threshold = percent_match(output_true, output_pred)
            write_log(formatted_datetime,f"Percent match between desired ouput received output: {threshold}")
            if threshold > THRESHOLD:
                write_log(formatted_datetime,f"Because threshold is larger than THRESHOLD ({threshold} > {THRESHOLD}), trainBot continues to send the next command.")
                # match output, continue the next cmd in seq
                continue
            else:
                # unmatch output, send exit.
                command = "exit"
                output_pred = send_command_recieve_output(client_socket, command)
                client_socket.close()
                FULL_COMMAND = False
                write_log(formatted_datetime,f"Because threshold is smaller than THRESHOLD ({threshold} < {THRESHOLD}), , trainBot continues to send {command} command.")
                break
        
        if FULL_COMMAND is True:
            # because all response is correct, PREDICT will be 1.
            PREDICT[path] = 1
            command = "exit"
            output_pred = send_command_recieve_output(client_socket, command)
            client_socket.close()
        
        client_socket.close()
    


    accuracy_log(formatted_datetime, PREDICT)

    write_log(formatted_datetime,"TRAINING SESSION END.")
        

if __name__ == '__main__':
    # Read input for the first command
    N = 10
    for i in range(N):
        start_server()
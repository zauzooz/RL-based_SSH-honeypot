#/usr/bin/python3
import docker
import pickle

"""
    return outputs each of command from a list of file
    return list of file proccessed
"""

class Explorer:
    def __init__(self, file_names: dict):
        self.process_file_names = file_names

    def docker_rm(self, container):
        container.remove()

    def docker_stop(self, container):
        container.stop()

    def process_file(self, file_path):

        unknown_command_list = pickle.load(open(file_path, "rb"))
        
        def standardize_commands(unknown_command_list: list):
            pass

        unknown_command_list = standardize_commands(unknown_command_list)

        return unknown_command_list
    
    def save_outputs(self, command_dict: dict):
        pickle.dump(
            command_dict,
            open("explorer/var/output.plk", "wb")
        )

    def start(self):
        client = docker.from_env()
        for file in self.process_file_names:
            container = client.containers.run('myubuntu', tty=True, stdin_open=True, detach=True)
            command_list = self.process_file(file)
            command_dict = {}
            
            for cmd in command_list:
                output = container.exec_run(cmd)
                command_dict[cmd] = output.output.decode('utf-8')
            
            # stop container
            self.docker_stop(container)

            # remove container
            self.docker_rm(container)

            # save output to file
            self.save_outputs(command_dict)


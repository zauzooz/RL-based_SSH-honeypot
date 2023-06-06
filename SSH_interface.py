import os
import json
from learner.environment import LearningEnvironment
from learner.RL_instance import ReinforcementAlgorithm
from learner.RL_log import write_log

DATE_TIME = ""

def Login():
    username = input("Username: ")
    password = input("Password: ")
    if (username == "nnt") and (password == "dtd"):
        write_log("[terminal] Login successfull.")
        return True

def get_q_table(dir_path: str):
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

def TerminalEmulator():
    # khởi tạo thuật toán RL
    alg = ReinforcementAlgorithm(q_table=get_q_table("learner/var/rl/q-table/"))

    # khởi tạo môi trường RL
    env = LearningEnvironment(rlalg=alg, learning=True)

    # đợi nhận input đầu tiên khi đăng nhập thành công.
    cmd = input("$ ")
    while cmd != "exit":
        write_log(f"[terminal] recieved command {cmd}.")
        output = env.command_receive(cmd)
        print(output, end="")
        cmd = ""
        cmd = input("$ ")
    env.connection_close()


if __name__ == "__main__":
    write_log("[terminal] Start stupidPot.")
    i = 0
    while i < 3:
        if Login():
            TerminalEmulator()
            break
        else:
            print("Wrong Username or Password.")
            write_log("[terminal] Loggin fails.")
            i += 1
    else:
        write_log("[terminal] Login attemps failed.")
    write_log("[terminal] End session.")

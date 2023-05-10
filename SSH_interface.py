from environment import LearningEnvironment
from RL_instance import ReinforcementAlgorithm
from RL_log import writelog


def Login():
    username = input("Username: ")
    password = input("Password: ")
    if (username == "nnt") and (password == "dtd"):
        return True


def TerminalEmulator():
    # khởi tạo thuật toán RL
    alg = ReinforcementAlgorithm()

    # khởi tạo môi trường RL
    env = LearningEnvironment(rlalg=alg, learning=True)

    # đợi nhận input đầu tiên khi đăng nhập thành công.
    cmd = input("nnt@nnt:~$ ")
    while cmd != "exit":
        output = env.command_receive(cmd)
        print(output, end="")
        cmd = ""
        cmd = input()
    env.connection_close()


if __name__ == "__main__":
    i = 0
    while i < 3:
        if Login():
            TerminalEmulator()
            break
        else:
            print("Wrong Username or Password.")
            i += 1

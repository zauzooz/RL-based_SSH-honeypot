import numpy as np
from learner.RL_instance import ReinforcementAlgorithm
from learner.RL_log import write_log
import pickle
from learner.RL_database import CommandKnowledgeBase

db = CommandKnowledgeBase()


class LearningEnvironment:
    def __init__(self, rlalg: ReinforcementAlgorithm, learning: bool = True) -> None:
        self.rlalg = rlalg  # agent
        self.LEARNING = learning
        self.previous_output = ""
        self.explore_states = []
        self.unknown_commands = []

    def command_receive(self, command):
        def produce_next_state(command: str, output: str):
            state = str({"current_input": command, "previous_output": self.previous_output})
            return state

        # 2, 3 kiểm tra command có trong database không.
        if db.is_command_in_db(command):
            write_log(f"[environment] {command} is in the database.")
            self.unknown_commands.append(command)
            
            # nếu option LEARNING là True thì thực thi RL
            if self.LEARNING:
                write_log(f"[environment] LEARNING is True")
                # 4.2 Có output của command trong db.
                output = db.get_output_by_cmd(command)
                write_log(f"[environment] Get list of output from the database. There are {len(output)} output.")
                i = np.random.randint(0, len(output))
                next_state = produce_next_state(command=command, output=output[i])
                write_log(f"[environment] Choosen action is {i}. Therefore next_state will be {next_state}.")
                if next_state not in self.explore_states:
                    self.explore_states.append(next_state)

                # nếu state mới không nằm trong q_table của thuật toán
                if next_state not in self.rlalg.q_table:
                    # hiện tại đang thực hiện trong trường hợp có 1 output,
                    # với trưởng hợp có nhiều output cần lấy toàn bột danh sách output có thể có của command.
                    self.rlalg.q_table[next_state] = np.zeros(1).tolist()

                # thuật toán RL sẽ tính toán và trả về index output phù hợp với command.
                action = self.rlalg.produce_output(next_state)
                write_log(f"[environment] The output will be {output[action]}.")
                # output trả về sẽ tương ứng với action.
                # output = "nnt@nnt:~$ "
                self.previous_output = output[action]
                return output[action]
            # nếu option LEARNING là False thì trả về tĩnh mà không học.
            else:
                # output sẽ là mặc định trong database.
                output = db.get_output_by_cmd(command)[0]
                return output

        else:
            write_log(f"[environment] {command} is not in the database.")
            # 4.1 Không có output của commandd trong db.
            self.unknown_commands.append(command)
            return ""

    def connection_close(self):
        import datetime

        now = datetime.datetime.now()
        formatted_date = now.strftime("%d-%m-%Y_%H-%M-%S-%f")

        # lưu state lại để tiện load sau này.

        # lưu danh sách unknown_commands dùng trong việc update sau này.
        if self.unknown_commands != []:
            pickle.dump(
                self.unknown_commands,
                open(f"learner/var/explorer/unknown_commands_{formatted_date}.log", "wb"),
            )

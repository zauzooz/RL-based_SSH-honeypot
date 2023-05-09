import numpy as np
from RL_instance import ReinforcementAlgorithm
from database import COMMAND_DATABASE, get_output_in_database


class LearningEnvironment:
    def __init__(self, rlalg: ReinforcementAlgorithm, learning: bool = True) -> None:
        self.rlalg = rlalg  # agent
        self.LEARNING = learning
        self.explore_states = []
        self.unknown_commands = []

    def send_output(output: str):
        return output

    def command_receive(self, command):
        def is_in_database(command: str):
            if command in COMMAND_DATABASE.keys():
                return True
            else:
                return False

        def produce_next_state(command: str, output: str):
            state = str({"input": command, "output": output})
            return state

        # 2 và 3
        if is_in_database(command):
            # nếu option LEARNING là True thì thực thi RL
            if self.LEARNING:
                # 4.2 Có output của command trong db.
                next_state = produce_next_state(command)
                self.explore_states.append(next_state)

                # nếu state mới không nằm trong q_table của thuật toán
                if next_state not in self.rlalg.q_table:
                    # hiện tại đang thực hiện trong trường hợp có 1 output,
                    # với trưởng hợp có nhiều output cần lấy toàn bột danh sách output có thể có của command.
                    self.rlalg.q_table[next_state] = np.zeros(1).tolist()

                # thuật toán RL sẽ tính toán và trả về index output phù hợp với command.
                action = self.rlalg.produce_output(next_state)
                # output trả về sẽ tương ứng với action.
                output = ""
            # nếu option LEARNING là False thì trả về tĩnh mà không học.
            else:
                # output sẽ là mặc định trong database.
                ouput = get_output_in_database(command)

        else:
            # 4.1 Không có output của commandd trong db.
            self.unknown_commands.append(command)
            self.send_output("")

    def connection_close():
        pass

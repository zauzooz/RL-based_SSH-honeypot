import numpy as np
from copy import deepcopy
import random
import pickle
from learner.RL_log import write_log
from learner.RL_central import ReinforcementLearningCentral

class ReinforcementAlgorithm:
    def __init__(
        self,
        rl_central: ReinforcementLearningCentral,
        alg="Q-Learning",
        q_table: dict = {},
        command_dict: dict = {}
    ):
        self.alg = (
            alg  # tên thuật toán algorithm, ví dụ Q-Learning, Deep Q-Learning,...
        )
        # Tham số cho Q-Learning
        self.rl_central = deepcopy(rl_central)
        self.learning_rate: float = self.rl_central.learning_rate
        self.discount: float =  self.rl_central.discount
        self.epsilon: float = self.rl_central.epsilon
        self.q_table: dict = q_table  # q_table là một dictionary với cặp key-value là state-aciton (action là một danh sách các giá trị q_value)
        self.exploration = self.rl_central.exploration
    
        self.epsilon_factor = self.rl_central.epsilon_factor #
        self.max_cmds = 0

        self.previous_state: str = None
        self.previous_action: int = None
        self.current_state: str = None

        self.step: int = 0  # tăng thêm 1 mỗi lần nhận một input khác 'exit'.
        self.learning_point: float = 0  # số điểm tích lũy trong suốt quá trình học.

    def get_next_state(self, current_state, action, epsilon):
        state_list = list(self.q_table.keys())
        next_state = random.choice(state_list)
        return next_state

    def get_reward(self, current_state, action):
        """
        Trả về +1 nếu nhận command khác 'exit', trả về -1 nếu nhận command là 'exit'.
        """
        if "exit" in current_state:
            write_log(f"[reinforcement learning, get_reward] Because the \"exit\" command is recieved, the REWARD will be -1.")
            return -1
        else:
            write_log(f"[reinforcement learning, get_reward] Because the \"exit\" command  is not recieved, the REWARD will be 1.")
            return 1

    def update(self, current_state, action, next_state, reward):
        """

        next_state: được tạo ra bởi produce_next_state ở Environment
        """
        if self.alg == "Q-Learning":
            # Cách thức update Q-Learning
            write_log(f"[reinforcement learning, update, q-learning] Q-Learning is selected.")
            if current_state is not None:
                # reward = self.get_reward(current_state, action)
                if next_state is None:
                    next_state = self.get_next_state(
                        current_state, action, self.epsilon
                    )
                max_future_q = np.max(self.q_table[next_state])
                current_q = self.q_table[current_state][self.previous_action]

                new_q = current_q + self.learning_rate * (
                    reward + self.discount * max_future_q - current_q
                )
                write_log(f"[reinforcement learning, update, q-learning] Q-value of {self.current_state} with action {action} is {new_q}.")
                self.q_table[current_state][self.previous_action] = new_q

                write_log(f"[reinforcement learning, update, q-learning] Update current state {self.current_state} to {next_state}.")
                self.current_state = next_state

            else:
                write_log(f"[reinforcement learning, get_reward] The CURRENT STATE is None.")
                
        elif self.alg == "Deep-Q-Learning":
            pass

    def produce_output(self, state):
        # cập nhật lại bước hiện tại
        self.previous_state = self.current_state
        self.current_state = state
        write_log(f"[reinforcement learning, produce_output] PREVIOUS STATE is {self.previous_state}, while CURRENT STATE is {self.current_state}.")

        # áp dụng chiến lược greedy-epsilon ở đây
        e = np.random.uniform(0, 1)

        if self.max_cmds == self.rl_central.epsilon_update_stage:
            self.rl_central.epsilon *= self.epsilon_factor
            self.epsilon = self.rl_central.epsilon
            self.max_cmds = 0
        else:
            self.max_cmds += 1

        if e < self.epsilon:
            # chọn một action ngẫu nhiên
            action = int(np.random.randint(len(self.q_table[self.current_state])))
            write_log(f"[reinforcement learning, produce_output] Since {e} is smaller than {self.epsilon}, the action will be taken randomly. The selected action is action {action}.")
        else:
            # chọn action có q_value cao nhất
            action = int(np.argmax(self.q_table[self.current_state]))
            write_log(f"[reinforcement learning, produce_output] Becase {e} is larger than {self.epsilon}, the action having maximum q-value will be taken. The selected action is action {action}.")

        # lấy reware tương ứng với state và action.
        reward = self.get_reward(self.current_state, action)

        # tăng điểm học tập
        self.learning_point += reward

        # Thực hiện cập nhật giá trị q_value trong q_table
        self.update(self.previous_state, action, self.current_state, reward)

        # tăng điểm số lệnh nhận được
        self.step += 1

        # sau khi thực hiện hàm này xong, hành động này trở thành hành động của quá khư
        # cho nên cần phải gán cho nó là hành động của quá khứ.
        self.previous_action = int(action)

        return int(action)

    def connection_closed(self):
        # lưu state tại var/rl để có dịp xài cho lần sau.
        # lưu unknown_command_dict tại var/explore để cập nhật db sau này.
        pass

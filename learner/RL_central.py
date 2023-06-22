

class ReinforcementLearningCentral:
    """
        Manage the configuration values for Reinforcement Learning Algorithms.
    """
    def __init__(self,
                 mode: str,
                 learning: bool = True,
                 learning_rate: float = 0.095,
                 discount: float = 0.95,
                 epsilon: float = 0.4,
                 exploration: bool = True,
                 epsilon_factor:float = 0.9995,
                 epsilon_update_stage: int = 5
                ):
        
        if mode not in ["train", "test"]:
            raise "mode must be 'train' or 'test'."

        self.learning = learning
        self.learning_rate = learning_rate
        self.discount = discount
        self.epsilon = epsilon
        self.exploration = exploration
        self.epsilon_factor = 0
        if 0 < epsilon_factor < 1:
            self.epsilon_factor = epsilon_factor
        else:
            raise "epsilon_factor must be greater than 0 and smaller than 1."
        
        self.epsilon_update_stage = epsilon_update_stage

        self.number_of_cmds = 0

    
    def inc(self):
        self.number_of_cmds += 1
import torch

class DeepKirby:

    BUTTONS = ['A', 'B', 'X', 'Y', 'L']
    
    def __init__(self, state_dim, action_dim, save_dir):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.save_dir = save_dir

        self.device = "cuda" if torch.cuda.is_available() else "cpu"



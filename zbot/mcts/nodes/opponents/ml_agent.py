from mcts.nodes.old_files.opponent_node import Opponent
from mcts.nodes.node import Node


class ml_agent(Opponent):

    def __init__(self, parent: Node, state):
        super().__init__(parent, state)

    def generate_children(self):
        raise NotImplemented


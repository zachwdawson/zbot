
from mcts.nodes.node import Node

class Leaf(Node):

    def __init__(self, state, prev_action=None, parent=None):
        super().__init__(state, prev_action, parent)

    def generate_children(self):
        return []

    def is_terminal(self):
        return True

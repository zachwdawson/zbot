
from mcts.nodes.node import Node
from mcts.nodes.chance_node import Chance
from mcts.nodes.leaf_node import Leaf
from mcts.nodes.decision_node import Decision
from copy import deepcopy

class Opponent(Node):

    def __init__(self, state, prev_action=None, parent=None):
        super().__init__(parent, prev_action, state)


    def generate_children(self):
        new_state = deepcopy(self.state)
        for action in self.state['legal_actions']:
            if action == 'raise':
                self.children.append(Decision(new_state, parent=self, prev_action='raise'))
            elif action == 'call':
                if len(new_state['public_cards']) == 5:
                    self.children.append(Leaf(new_state, parent=self, prev_action='call'))
                else:
                    self.children.append(Chance(new_state, parent=self, prev_action='call'))
            elif action == 'check':
                if len(new_state['public_cards']) == 5:
                    self.children.append(Leaf(new_state, parent=self, prev_action='call'))
                else:
                    self.children.append(Decision(new_state, parent=self, prev_action='call'))
            elif action == 'fold':
                self.children.append(Leaf(new_state, parent=self, prev_action='fold'))

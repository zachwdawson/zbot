
from mcts.nodes.node import Node
from mcts.nodes.old_files.opponent_node import Opponent
from mcts.nodes.old_files.chance_node import Chance
from mcts.nodes.old_files.leaf_node import Leaf
from copy import deepcopy

class Decision(Node):

    def __init__(self, state, prev_action=None, parent=None):

        super().__init__(state, prev_action, parent)

    def generate_children(self):
        new_state = deepcopy(self.state)
        for action in self.state['legal_actions']:
            if action == 'raise':
                new_state['legal_actions'] = ['raise', 'call', 'fold']
                self.children.append(Opponent(new_state, parent=self, prev_action='raise'))
            elif action == 'call':
                if len(new_state['public_cards']) == 5:
                    self.children.append(Leaf(new_state, parent=self, prev_action='call'))
                else:
                    self.children.append(Chance(new_state, parent=self, prev_action='call'))
            elif action == 'check':
                if len(new_state['public_cards']) == 5:
                    self.children.append(Leaf(new_state, parent=self, prev_action='check'))
                else:
                    new_state['legal_actions'] = ['raise', 'check', 'fold']
                    self.children.append(Opponent(new_state, parent=self, prev_action='check'))
            elif action == 'fold':
                self.children.append(Leaf(new_state, parent=self, prev_action='fold'))

# class Decision(Node):
#
#     def __init__(self, state, prev_action=None, parent=None):
#
#         super().__init__(parent, prev_action, state)
#
#     def generate_children(self):
#         new_state = deepcopy(self.state)
#         for action in self.state['legal_actions']:
#             if action == 'raise':
#                 self.children.append(Opponent(new_state, parent=self, prev_action='raise'))
#             elif action == 'call':
#                 if len(new_state['public_cards']) == 5:
#                     self.children.append(Leaf(new_state, parent=self, prev_action='call'))
#                 else:
#                     self.children.append(Chance(new_state, parent=self, prev_action='call'))
#             elif action == 'check':
#                 if len(new_state['public_cards']) == 5:
#                     self.children.append(Leaf(new_state, parent=self, prev_action='call'))
#                 else:
#                     self.children.append(Opponent(new_state, parent=self, prev_action='call'))
#             elif action == 'fold':
#                 self.children.append(Leaf(new_state, parent=self, prev_action='fold'))

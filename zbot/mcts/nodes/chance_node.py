from mcts.nodes.node import Node
from mcts.nodes.opponent_node import Opponent
from mcts.nodes.decision_node import Decision
from mcts.nodes.leaf_node import Leaf
from copy import deepcopy
from util import eval7torlcard


class Chance(Node):

    def __init__(self, state, prev_action=None, parent=None):
        super().__init__(parent, prev_action, state)

    def generate_children(self):
        new_state = deepcopy(self.state)
        if len(self.state['public_cards']) == 0:
            new_state['public_cards'] = map(eval7torlcard, self.deck.deal(3))
            if self.state['dealer']:
                self.children.append(Opponent(new_state, parent=self))
            else:
                self.children.append(Decision(new_state, parent=self))
        elif len(self.state['public_cards']) == 3:
            new_state['public_cards'] = map(eval7torlcard, self.deck.deal())
            if self.state['dealer']:
                self.children.append(Opponent(new_state, parent=self))
            else:
                self.children.append(Decision(new_state, parent=self))
        elif len(self.state['public_cards']) == 4:
            new_state['public_cards'] = map(eval7torlcard, self.deck.deal())
            if self.state['dealer']:
                self.children.append(Opponent(new_state, parent=self))
            else:
                self.children.append(Decision(new_state, parent=self))
        elif len(self.state['public_cards']) == 5:
            self.children.append(Leaf(new_state, parent=self))


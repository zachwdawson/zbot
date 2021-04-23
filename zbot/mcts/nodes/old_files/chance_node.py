from mcts.nodes.node import Node
from mcts.nodes.node import Opponent
from mcts.nodes.node import Decision
from mcts.nodes.node import Leaf
from copy import deepcopy
from util import eval7torlcard, rlcardtoeval7
from eval7 import Deck


class Chance(Node):

    def __init__(self, state, prev_action=None, parent=None):
        super().__init__(state, prev_action, parent)

    def generate_children(self):
        new_state = deepcopy(self.state)
        new_state['legal_actions'] = ['raise', 'check', 'fold']
        opp_hand = list(map(rlcardtoeval7, self.state['opp_hand']))
        hand = list(map(rlcardtoeval7, self.state['hand']))
        public_cards = list(map(rlcardtoeval7, self.state['public_cards']))
        used_cards = hand + public_cards + opp_hand
        if len(self.state['public_cards']) == 0:
            new_state['public_cards'] = new_state['public_cards'] + self.generate_cards(3, used_cards)
            if self.state['im_dealer']:
                self.children.append(Opponent(new_state, parent=self, prev_action='cards'))
            else:
                self.children.append(Decision(new_state, parent=self, prev_action='cards'))
        elif len(self.state['public_cards']) == 3:
            new_state['public_cards'] = new_state['public_cards'] + self.generate_cards(1, used_cards)
            if self.state['im_dealer']:
                self.children.append(Opponent(new_state, parent=self, prev_action='cards'))
            else:
                self.children.append(Decision(new_state, parent=self, prev_action='cards'))
        elif len(self.state['public_cards']) == 4:
            new_state['public_cards'] = new_state['public_cards'] + self.generate_cards(1, used_cards)
            if self.state['im_dealer']:
                self.children.append(Opponent(new_state, parent=self, prev_action='cards'))
            else:
                self.children.append(Decision(new_state, parent=self, prev_action='cards'))
        elif len(self.state['public_cards']) == 5:
            self.children.append(Leaf(new_state, parent=self, prev_action='cards'))

    def generate_cards(self, num, hand):
        deck = Deck()
        while True:
            new_cards = deck.sample(num)
            if hand[0] not in new_cards and hand[1] not in new_cards:
                break
        return list(map(eval7torlcard, new_cards))

# class Chance(Node):
#
#     def __init__(self, state, prev_action=None, parent=None):
#         super().__init__(parent, prev_action, state)
#
#     def generate_children(self):
#         new_state = deepcopy(self.state)
#         if len(self.state['public_cards']) == 0:
#             new_state['public_cards'] = map(eval7torlcard, self.deck.deal(3))
#             if self.state['dealer']:
#                 self.children.append(Opponent(new_state, parent=self))
#             else:
#                 self.children.append(Decision(new_state, parent=self))
#         elif len(self.state['public_cards']) == 3:
#             new_state['public_cards'] = map(eval7torlcard, self.deck.deal())
#             if self.state['dealer']:
#                 self.children.append(Opponent(new_state, parent=self))
#             else:
#                 self.children.append(Decision(new_state, parent=self))
#         elif len(self.state['public_cards']) == 4:
#             new_state['public_cards'] = map(eval7torlcard, self.deck.deal())
#             if self.state['dealer']:
#                 self.children.append(Opponent(new_state, parent=self))
#             else:
#                 self.children.append(Decision(new_state, parent=self))
#         elif len(self.state['public_cards']) == 5:
#             self.children.append(Leaf(new_state, parent=self))


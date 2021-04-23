from eval7 import Deck
from copy import deepcopy
from util import eval7torlcard, rlcardtoeval7


class Node(object):

    def __init__(self, state, prev_action=None, parent=None):
        self.state = state
        self.prev_action = prev_action
        self.parent = parent
        self.children = []
        self.num_visits = 0
        self.ev = 0

    def update(self, ev: float):
        self.num_visits += 1
        self.ev = ev

    def generate_children(self):
        raise NotImplemented

    def is_terminal(self):
        return False # override for leaf node


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


class Opponent(Node):

    def __init__(self, state, prev_action=None, parent=None):
        super().__init__(state, prev_action, parent)


    def generate_children(self):
        new_state = deepcopy(self.state)
        for action in self.state['legal_actions']:
            if action == 'raise':
                new_state['legal_actions'] = ['raise', 'call', 'fold']
                self.children.append(Decision(new_state, parent=self, prev_action='raise'))
            elif action == 'call':
                if len(new_state['public_cards']) == 5:
                    self.children.append(Leaf(new_state, parent=self, prev_action='call'))
                else:
                    self.children.append(Chance(new_state, parent=self, prev_action='call'))
            elif action == 'check':
                if len(new_state['public_cards']) == 5:
                    self.children.append(Leaf(new_state, parent=self, prev_action='check'))
                else:
                    if self.prev_action == 'check':
                        self.children.append(Chance(new_state, parent=self, prev_action='check'))
                    else:
                        new_state['legal_actions'] = ['raise', 'check', 'fold']
                        self.children.append(Decision(new_state, parent=self, prev_action='check'))
            elif action == 'fold':
                self.children.append(Leaf(new_state, parent=self, prev_action='fold'))


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


class Leaf(Node):

    def __init__(self, state, prev_action=None, parent=None):
        super().__init__(state, prev_action, parent)

    def generate_children(self):
        return []

    def is_terminal(self):
        return True

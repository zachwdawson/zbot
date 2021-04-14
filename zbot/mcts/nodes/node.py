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
        self.num_wins = 0
        self.deck = Deck()
        self.deck.cards = list(set(self.deck.cards) - set(map(rlcardtoeval7, state['public_cards'])))
        # self.deck = Deck() if parent is None else deepcopy(parent.deck)

    def update(self, win: bool):
        self.num_visits += 1
        self.num_wins += 1 if win else 0

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
                    self.children.append(Decision(new_state, parent=self, prev_action='check'))
            elif action == 'fold':
                self.children.append(Leaf(new_state, parent=self, prev_action='fold'))


class Chance(Node):

    def __init__(self, state, prev_action=None, parent=None):
        super().__init__(state, prev_action, parent)

    def generate_children(self):
        new_state = deepcopy(self.state)
        if len(self.state['public_cards']) == 0:
            new_state['public_cards'] = list(map(eval7torlcard, self.deck.deal(3)))
            if self.state['dealer']:
                self.children.append(Opponent(new_state, parent=self))
            else:
                self.children.append(Decision(new_state, parent=self))
        elif len(self.state['public_cards']) == 3:
            new_state['public_cards'] = list(map(eval7torlcard, self.deck.deal(1)))
            if self.state['dealer']:
                self.children.append(Opponent(new_state, parent=self))
            else:
                self.children.append(Decision(new_state, parent=self))
        elif len(self.state['public_cards']) == 4:
            new_state['public_cards'] = list(map(eval7torlcard, self.deck.deal(1)))
            if self.state['dealer']:
                self.children.append(Opponent(new_state, parent=self))
            else:
                self.children.append(Decision(new_state, parent=self))
        elif len(self.state['public_cards']) == 5:
            self.children.append(Leaf(new_state, parent=self))


class Leaf(Node):

    def __init__(self, state, prev_action=None, parent=None):
        super().__init__(state, prev_action, parent)

    def generate_children(self):
        return []

    def is_terminal(self):
        return True

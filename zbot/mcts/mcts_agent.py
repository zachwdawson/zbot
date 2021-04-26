
from mcts.mcts import explore
from mcts.nodes.old_files.decision_node import Decision
from util import rlcardtoeval7, action_to_num
import numpy as np


class MCTS_Agent(object):
    ''' A random agent. Random agents is for running toy examples on the card games
    '''

    def __init__(self, action_num):
        ''' Initilize the random agent

        Args:
            action_num (int): The size of the ouput action space
        '''
        self.use_raw = True
        self.action_num = action_num
        self.prev_state = None
        self.hand = None
        self.dealer = False

        ### Hand Rank Model- maintained all from opponents point of view
        self.stage = 0
        self.opp_num_raises_total = 0
        self.my_num_raises_total = 0
        self.prev_opp_num_raises_total = 0
        self.prev_my_num_raises_total = 0
        self.action = None
        self.prev_action = None
        self.opp_last_action = None
        self.prev_opp_last_action = None
        self.highest_card = None
        self.prev_highest_card = None
        self.num_queens = None
        self.num_kings = None
        self.num_aces = None

    def step(self, state):
        ''' Predict the action given the curent state in gerenerating training data.

        Args:
            state (dict): An dictionary that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        '''
        state = state['raw_obs']
        self.update(state)
        state['im_dealer'] = self.dealer
        state['opp_hand'] = None
        # [stage, opp_last_action, my_last_action, my_num_raises_total, opp_num_raises_total, num_aces, num_kings,
        # num_queens, prev_action, prev_opp_last_action, prev_my_last_action, prev_my_num_raises_total,
        # prev_opp_num_raises_total, prev_num_queens]
        print([self.stage, self.action, self.opp_last_action,
                                                             self.opp_num_raises_total, self.my_num_raises_total,
                                                             self.num_aces, self.num_kings, self.num_queens,
                                                             self.prev_action, self.prev_action,
                                                             self.prev_opp_last_action, self.prev_opp_num_raises_total,
                                                             self.prev_my_num_raises_total])
        hand_rank_model = np.reshape(np.nan_to_num(np.array([self.stage, action_to_num(self.action), action_to_num(self.opp_last_action),
                                                             self.opp_num_raises_total, self.my_num_raises_total,
                                                             self.num_aces, self.num_kings, self.num_queens,
                                                             action_to_num(self.prev_action), action_to_num(self.prev_action),
                                                             action_to_num(self.prev_opp_last_action), self.prev_opp_num_raises_total,
                                                             self.prev_my_num_raises_total], dtype=np.float)), (1, -1))
        print(hand_rank_model)
        action, probs = explore(Decision(state), hand_rank_model)
        self.prev_state = state
        self.action = action
        return action

    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation.
            Since the random agents are not trained. This function is equivalent to step function

        Args:
            state (dict): An dictionary that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        state = state['raw_obs']
        self.update(state)

        state['im_dealer'] = self.dealer
        state['opp_hand'] = None
        # [stage, opp_last_action, my_last_action, my_num_raises_total, opp_num_raises_total, num_aces, num_kings,
        # num_queens, prev_action, prev_opp_last_action, prev_my_last_action, prev_my_num_raises_total,
        # prev_opp_num_raises_total, prev_num_queens]
        hand_rank_model = np.reshape(np.nan_to_num([self.stage, self.action, self.opp_last_action, self.opp_num_raises_total, self.my_num_raises_total,
                           self.num_aces, self.num_kings, self.num_queens, self.prev_action, self.prev_action,
                           self.prev_opp_last_action, self.prev_opp_num_raises_total, self.prev_my_num_raises_total]), (1,-1))
        action, probs = explore(Decision(state), hand_rank_model)
        self.prev_state = state
        self.action = action
        return action, probs

    def update(self, state):
        curr_public_cards = state['public_cards']
        prev_public_cards = [] if self.prev_state is None else self.prev_state['public_cards']
        curr_hand = state['hand']
        prev_hand = [] if self.prev_state is None else self.prev_state['hand']

        # new hand
        if len(curr_public_cards) < len(prev_public_cards) or curr_hand != prev_hand:
            self.hand = state['hand']
            if 'check' in state['legal_actions'] and sum(state['raise_nums']) == 0:
                self.dealer = True
            elif 'call' in state['legal_actions'] and sum(state['raise_nums']) == 1:
                self.dealer = True
            else:
                self.dealer = False

        # stage
        if len(curr_public_cards) == 0:
            self.stage = 0
        elif len(curr_public_cards) == 3:
            self.stage = 1
        elif len(curr_public_cards) == 4:
            self.stage = 2
        else:
            self.stage = 4

        # raises
        new_raises = np.subtract(state['raise_nums'], [0,0,0,0]) if self.prev_state is None else np.subtract(state['raise_nums'], self.prev_state['raise_nums'])
        new_raises = np.sum(new_raises)
        if self.prev_action == 'raise':
            opp_raises = new_raises - 1
        else:
            opp_raises = new_raises
        if self.opp_last_action == 'raise':
            my_raises = new_raises - 1
        else:
            my_raises = new_raises

        self.prev_opp_num_raises_total = self.opp_num_raises_total
        self.prev_my_num_raises_total = self.my_num_raises_total
        self.opp_num_raises_total = self.opp_num_raises_total + opp_raises
        self.my_num_raises_total = self.my_num_raises_total + my_raises

        # Action
        self.prev_action = self.action
        self.prev_opp_last_action = self.opp_last_action
        self.opp_last_action = 2 if opp_raises > 0 else 1

        # Board Info
        num_aces, num_kings, num_queens = 0, 0, 0
        eval7_cards = list(map(rlcardtoeval7, curr_public_cards))
        highest_card = eval7_cards[0] if len(curr_public_cards) > 0 else None
        for card in eval7_cards:

            if card > highest_card:
                highest_card = card

            if 'A' in str(card):
                num_aces += 1
            elif 'K' in str(card):
                num_kings += 1
            elif 'Q' in str(card):
                num_queens += 1
        self.prev_highest_card = self.highest_card
        self.highest_card = highest_card
        self.num_queens = num_queens
        self.num_kings = num_kings
        self.num_aces = num_aces


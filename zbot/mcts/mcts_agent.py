
from mcts.mcts import explore
from mcts.nodes.old_files.decision_node import Decision
from util import rlcardtoeval7, action_to_num, hand_rank_to_num, calc_num_outs, calc_win_prob
import numpy as np
import pandas as pd
from joblib import load
import eval7

MAX_EVAL_HS = 135004160 # royal flush of any suit

class MCTS_Agent(object):
    ''' A random agent. Random agents is for running toy examples on the card games
    '''

    def __init__(self, action_num, duration, exploration, model_hand_rank, model_action):
        ''' Initilize the random agent

        Args:
            action_num (int): The size of the ouput action space
        '''
        self.use_raw = True
        self.action_num = action_num
        self.prev_state = None
        self.hand = None
        self.dealer = False
        self.duration = duration
        self.exploration = exploration
        self.model_hand_rank = load(model_hand_rank)
        self.model_action = load(model_action)
        self.action_df = pd.DataFrame(columns=['model_raise', 'model_check', 'model_fold', 'mcts_raise', 'model_check', 'mcts_fold'])

        ### Stored For models
        self.stage = 0
        self.prev_stage = 0
        self.opp_num_raises_total = 0
        self.my_num_raises_total = 0
        self.prev_opp_num_raises_total = 0
        self.prev_my_num_raises_total = 0
        self.opp_num_raises_curr_phase = 0
        self.my_num_raises_curr_phase = 0
        self.opp_stack_committed_curr_phase = 0
        self.my_stack_committed_curr_phase = 0
        self.action = None
        self.prev_action = None
        self.my_last_action = None
        self.prev_my_last_action = None
        self.opp_last_action = None
        self.prev_opp_last_action = None
        self.highest_card = None
        self.prev_highest_card = None
        self.num_queens = None
        self.num_kings = None
        self.num_aces = None
        self.hand_rank = None
        self.hand_strength = None
        self.prev_hand_strength = None
        self.winning_prob = None
        self.prev_winning_prob = None
        self.num_outs = None
        self.prev_num_outs = None

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
        hand_rank_inst = np.reshape(np.nan_to_num(np.array([self.stage, action_to_num(self.action), action_to_num(self.opp_last_action),
                                                             self.opp_num_raises_total, self.my_num_raises_total,
                                                             self.num_aces, self.num_kings, self.num_queens,
                                                             action_to_num(self.prev_action), action_to_num(self.prev_action),
                                                             action_to_num(self.prev_opp_last_action), self.prev_opp_num_raises_total,
                                                             self.prev_my_num_raises_total], dtype=np.float)), (1, -1))
        opp_hand_rank_probs = self.model_hand_rank.predict_proba(hand_rank_inst)
        action, probs = explore(Decision(state), opp_hand_rank_probs, duration=self.duration, exploration=self.exploration)
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
        # [stage, opp_last_action, my_num_raises_total, opp_num_raises_total, num_aces,
        # num_kings	num_queens, prev_opp_last_action, prev_my_last_action,
        # prev_my_num_raises_total, prev_opp_num_raises_total]
        hand_rank_inst = np.reshape(np.nan_to_num(np.array([self.stage, action_to_num(self.action),
                                                            self.opp_num_raises_total, self.my_num_raises_total,
                                                            self.num_aces, self.num_kings, self.num_queens,
                                                            action_to_num(self.prev_my_last_action), action_to_num(self.prev_opp_last_action),
                                                            self.prev_opp_num_raises_total, self.prev_my_num_raises_total], dtype=np.float)), (1, -1))
        opp_hand_rank_probs = self.model_hand_rank.predict_proba(hand_rank_inst)
        action, mcts_probs = explore(Decision(state), opp_hand_rank_probs, duration=self.duration, exploration=self.exploration)
        eval_probs = [prob[1] for prob in mcts_probs]
        self.prev_state = state
        self.action = action
        # [dealer, hand_strength, hand_rank, opp_last_action, my_last_action, my_stack_committed_curr_phase,
        # opp_stack_committed_curr_phase, opp_num_raises_curr_phase, num_outs, winning_prob, highest_card, prev_action,
        # prev_hand_strength, prev_opp_last_action, prev_my_last_action, prev_my_num_raises_total,
        # prev_opp_num_raises_total, prev_num_outs, prev_winning_prob, prev_highest_card]
        action_model_probs = self.model_action.predict_proba(np.reshape(np.nan_to_num(np.array([self.dealer * 1, self.hand_strength,
                                                                                              hand_rank_to_num(self.hand_rank), action_to_num(self.opp_last_action),
                                                                                              action_to_num(self.my_last_action), self.my_stack_committed_curr_phase,
                                                                                              self.opp_stack_committed_curr_phase,
                                                                                              self.opp_num_raises_curr_phase, self.num_outs, self.winning_prob,
                                                                                              self.highest_card, action_to_num(self.prev_action),
                                                                                              self.prev_hand_strength, action_to_num(self.prev_opp_last_action),
                                                                                              action_to_num(self.prev_my_last_action), self.prev_my_num_raises_total,
                                                                                              self.prev_opp_num_raises_total, self.prev_num_outs,
                                                                                              self.prev_winning_prob, self.prev_highest_card], dtype=np.float)), (1,-1)))

        mcts_probs = sorted(mcts_probs, key=lambda x: x[0])
        print(self.action_df)
        print(action_model_probs)
        print(mcts_probs)
        self.action_df.loc[len(self.action_df.index)] = [action_model_probs[2],
                                                         action_model_probs[1],
                                                         action_model_probs[0],
                                                         mcts_probs[2],
                                                         mcts_probs[1],
                                                         mcts_probs[0]]
        return action, eval_probs

    def update(self, state):
        curr_public_cards = state['public_cards']
        prev_public_cards = [] if self.prev_state is None else self.prev_state['public_cards']
        curr_hand = state['hand']
        prev_hand = [] if self.prev_state is None else self.prev_state['hand']
        self.prev_stage = self.stage

        # new hand
        if len(curr_public_cards) < len(prev_public_cards) or curr_hand != prev_hand:
            self.stage = 0
            self.prev_stage = 0
            self.opp_num_raises_total = 0
            self.my_num_raises_total = 0
            self.prev_opp_num_raises_total = 0
            self.prev_my_num_raises_total = 0
            self.opp_num_raises_curr_phase = 0
            self.opp_stack_committed_curr_phase = 0
            self.action = None
            self.prev_action = None
            self.my_last_action = None
            self.prev_my_last_action = None
            self.opp_last_action = None
            self.prev_opp_last_action = None
            self.highest_card = None
            self.prev_highest_card = None
            self.num_queens = None
            self.num_kings = None
            self.num_aces = None
            self.hand_rank = None
            self.hand_strength = None
            self.prev_hand_strength = None
            self.winning_prob = None
            self.prev_winning_prob = None
            self.num_outs = None
            self.prev_num_outs = None
            self.hand = state['hand']

            self.prev_dealer = self.dealer
            if 'check' in state['legal_actions'] and sum(state['raise_nums']) == 0:
                self.dealer = True
            elif 'call' in state['legal_actions'] and sum(state['raise_nums']) == 1:
                self.dealer = True
            else:
                self.dealer = False

        # hand
        full_hand = list(map(rlcardtoeval7, curr_hand + curr_public_cards))
        eval7_strength = eval7.evaluate(full_hand)
        self.prev_hand_strength = self.hand_strength
        self.hand_strength = eval7_strength / MAX_EVAL_HS # scales to between 0 and 1. Needed for P(win)
        self.hand_rank = eval7.handtype(eval7_strength)
        self.prev_num_outs = self.num_outs
        self.num_outs = calc_num_outs(full_hand)
        self.prev_winning_prob = self.winning_prob
        self.winning_prob = calc_win_prob(list(map(rlcardtoeval7, curr_public_cards)), list(map(rlcardtoeval7, curr_hand)), self.num_outs)

        # stage
        if len(curr_public_cards) == 0:
            self.stage = 0
        elif len(curr_public_cards) == 3:
            self.stage = 1
        elif len(curr_public_cards) == 4:
            self.stage = 2
        else:
            self.stage = 3

        if self.stage > self.prev_stage:
            self.opp_num_raises_curr_phase = 0
            self.opp_stack_committed_curr_phase = 0
            self.my_num_raises_curr_phase = 0
            self.my_stack_committed_curr_phase = 0

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
        self.my_num_raises_curr_phase = self.my_num_raises_curr_phase + my_raises
        self.my_stack_committed_curr_phase = self.my_stack_committed_curr_phase ++ 1 \
            if (my_raises == 0 and action_to_num(self.action)) == 1 else 0
        self.opp_num_raises_curr_phase = self.opp_num_raises_curr_phase + opp_raises
        self.opp_stack_committed_curr_phase = self.opp_stack_committed_curr_phase + opp_raises
        self.opp_stack_committed_curr_phase = self.opp_stack_committed_curr_phase + 1 \
            if (opp_raises == 0 and self.dealer and self.my_last_action == 'raise') else 0

        # Action
        self.prev_opp_last_action = self.opp_last_action
        self.opp_last_action = 2 if opp_raises > 0 else 1
        self.prev_action = self.opp_last_action
        self.my_last_action = self.action

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


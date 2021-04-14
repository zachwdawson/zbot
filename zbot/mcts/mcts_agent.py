
from mcts.mcts import explore
from src.structures.stage import Stage
from mcts.nodes.node import Decision


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
        # self.stage = Stage.PRE_FLOP
        # self.dealer = False
        # self.opp_last_action = None
        # self.my_last_action = None
        # self.opp_stack_committed_curr_phase = None
        # self.my_stack_committed_curr_phase = None
        # self.opp_num_raises_curr_phase = None
        # self.my_num_raises_curr_phase = None
        # self.opp_num_raises_total = None
        # self.my_num_raises_total = None

    def step(self, state):
        ''' Predict the action given the curent state in gerenerating training data.

        Args:
            state (dict): An dictionary that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        '''
        # print('step')
        # print(state)
        # legal_actions = state['raw_legal_actions']
        # state = state['raw_obs']
        # hand = state['hand']
        # public_cards = state['public_cards']
        # self.stage = Stage.PRE_FLOP
        # self.dealer = False
        # self.opp_last_action = None
        # self.my_last_action = None
        # self.opp_stack_committed_curr_phase = 0
        # self.my_stack_committed_curr_phase = 0
        # self.opp_num_raises_curr_phase = 0
        # self.my_num_raises_curr_phase = 0
        # self.opp_num_raises_total = 0
        # self.my_num_raises_total = 0
        #
        # if len(public_cards) == 0:
        #     self.stage = Stage.PRE_FLOP
        #     if 'check' in state['legal_actions'] and sum(state['raise_nums']) == 0:
        #         self.dealer = True
        #     elif 'call' in state['legal_actions'] and sum(state['raise_nums']) == 1:
        #         self.dealer = True
        # elif len(public_cards) == 3:
        #     self.stage = Stage.POST_FLOP
        # elif len(public_cards) == 4:
        #     self.stage = Stage.RIVER
        # elif len(public_cards) == 5:
        #     self.stage = Stage.RIVER
        #
        #
        # action = 'fold'
        state = state['raw_obs']
        if len(state['public_cards']) == 0 and self.hand != state['hand']: # Terrible assumption that you can't be dealt the same two cards in consecutive hands
            self.hand = state['hand']
            if 'check' in state['legal_actions'] and sum(state['raise_nums']) == 0:
                self.dealer = True
            elif 'call' in state['legal_actions'] and sum(state['raise_nums']) == 1:
                self.dealer = True
            else:
                self.dealer = False

        state['dealer'] = self.dealer
        action, probs = explore(Decision(state))
        return action
        # return np.random.choice(state['legal_actions'])

    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation.
            Since the random agents are not trained. This function is equivalent to step function

        Args:
            state (dict): An dictionary that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        # print("eval_step")
        # print(state)
        # # print()
        # probs = [0 for _ in range(self.action_num)]
        # for i in state['legal_actions']:
        #     probs[i] = 1/len(state['legal_actions'])
        # return self.step(state), probs
        state = state['raw_obs']

        if len(state['public_cards']) == 0 and self.hand != state['hand']: # Terrible assumption that you can't be dealt the same two cards in consecutive hands
            self.hand = state['hand']
            if 'check' in state['legal_actions'] and sum(state['raise_nums']) == 0:
                self.dealer = True
            elif 'call' in state['legal_actions'] and sum(state['raise_nums']) == 1:
                self.dealer = True
            else:
                self.dealer = False

        state['dealer'] = self.dealer

        action, probs = explore(Decision(state))
        #
        # self.prev_state = deepcopy(state)
        # print()

        # return max(zip(actions, probs), key=lambda item: item[1])[0], probs
        # print(actions, probs)
        # best_action = max(zip(actions, probs), key=lambda item: item[1])
        # print(best_action)
        return action, probs


    # def search(self, time_budget: int) -> None:
    #     """
    #     Search and update the search tree for a
    #     specified amount of time in seconds.
    #     """
    #     start_time = datetime.now()
    #     num_rollouts = 0
    #
    #     # do until we exceed our time budget
    #     while (datetime.now() - start_time).total_seconds() < time_budget:
    #         node, state = self.select_node()
    #         turn = state.turn()
    #         outcome = self.roll_out(state)
    #         self.backup(node, turn, outcome)
    #         num_rollouts += 1

    # def select_node(self) -> tuple:
    #     """
    #     Select a node in the tree to preform a single simulation from.
    #     """
    #     node = self.root
    #     state = deepcopy(self.root_state)
    #
    #     # stop if we find reach a leaf node
    #     while len(node.children) != 0:
    #         # descend to the maximum value node, break ties at random
    #         children = node.children.values()
    #         max_value = max(children, key=lambda n: n.value).value
    #         max_nodes = [n for n in node.children.values()
    #                      if n.value == max_value]
    #         node = choice(max_nodes)
    #         state.play(node.move)
    #
    #         # if some child node has not been explored select it before expanding
    #         # other children
    #         if node.N == 0:
    #             return node, state
    #
    #     # if we reach a leaf node generate its children and return one of them
    #     # if the node is terminal, just return the terminal node
    #     if self.expand(node, state):
    #         node = choice(list(node.children.values()))
    #         state.play(node.move)
    #     return node, state

    # @staticmethod
    # def expand(parent: Node, state: Node) -> bool:
    #     """
    #     Generate the children of the passed "parent" node based on the available
    #     moves in the passed gamestate and add them to the tree.
    #     Returns:
    #         bool: returns false If node is leaf (the game has ended).
    #     """
    #     children = []
    #     if state.is_terminal():
    #         return False
    #
    #     if state.winner != GameMeta.PLAYERS['none']:
    #         # game is over at this node so nothing to expand
    #         return False
    #
    #     for move in state.moves():
    #         children.append(Node(move, parent))
    #
    #     parent.add_children(children)
    #     return True
    #
    # @staticmethod
    # def roll_out(state: GameState) -> int:
    #     """
    #     Simulate an entirely random game from the passed state and return the winning
    #     player.
    #     Args:
    #         state: game state
    #     Returns:
    #         int: winner of the game
    #     """
    #     moves = state.moves()  # Get a list of all possible moves in current state of the game
    #
    #     while state.winner == GameMeta.PLAYERS['none']:
    #         move = choice(moves)
    #         state.play(move)
    #         moves.remove(move)
    #
    #     return state.winner
    #
    # @staticmethod
    # def backup(node: Node, turn: int, outcome: int) -> None:
    #     """
    #     Update the node statistics on the path from the passed node to root to reflect
    #     the outcome of a randomly simulated playout.
    #     Args:
    #         node:
    #         turn: winner turn
    #         outcome: outcome of the rollout
    #     Returns:
    #         object:
    #     """
    #     # Careful: The reward is calculated for player who just played
    #     # at the node and not the next player to play
    #     reward = 0 if outcome == turn else 1
    #
    #     while node is not None:
    #         node.N += 1
    #         node.Q += reward
    #         node = node.parent
    #         reward = 0 if reward == 1 else 1
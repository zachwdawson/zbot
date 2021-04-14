from mcts.nodes.node import Node
from datetime import datetime
from random import choice
import math
from util import rlcardtoeval7, p_win_v_random
from math import inf


def explore(root: Node, duration: float = 0.5, exploration: float = 1):

    start_time = datetime.now()

    while (datetime.now() - start_time).total_seconds() < duration:
        curr_node = select(root, exploration)
        sim_start = expand(curr_node)
        result = simulate(sim_start)
        backpropogatge(sim_start, result)

    max_val = -inf
    action = None
    probs=[]
    for child in root.children:
        prob = 0 if child.num_visits == 0 else child.num_wins/child.num_visits
        probs.append(prob)
        if prob > max_val:
            action = child.prev_action
            max_val = child.num_wins/child.num_visits

    return action, probs


def select(root, exploration):

    if len(root.children) == 0:
        return root

    max_child = None
    max_val = -math.inf
    for child in root.children:
        if child.num_visits != 0:
            if child.parent is not None and child.parent.num_visits != 0:
                uct = (child.num_wins / child.num_visits) + exploration * math.sqrt(math.log(child.parent.num_visits) / child.num_visits)
            else:
                uct = (child.num_wins / child.num_visits) + exploration * math.sqrt(math.log(1) / child.num_visits)
        else:
            uct = exploration
        if uct > max_val:
            max_val = uct
            max_child = child

    return select(max_child, exploration)


def expand(node):
    if node.is_terminal():
        return node

    node.generate_children()
    if len(node.children) == 0:
        return node
    return choice(node.children)


def simulate(node):
    '''
    Simulate game to end by comparing hand strength to any two random cards
    :param node: start node for simulate
    :return: True if probability of winning is greater than 0.5
    '''
    state = node.state
    hand = state['hand']
    public_cards = state['public_cards']
    p_win = p_win_v_random(list(map(rlcardtoeval7, hand)), list(map(rlcardtoeval7, public_cards)))
    if p_win > 0.5:
        return True
    else:
        return False


def backpropogatge(node, result):
    while node.parent is not None:
        node.update(result)
        node = node.parent

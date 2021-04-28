from mcts.nodes.node import Node, Chance
from datetime import datetime
from random import choice
import math
from util import create_opp_hand_from_rank_distribution, rlcardtoeval7, eval7torlcard, action_to_num
from eval7 import HandRange, Card
from eval7.equity import py_hand_vs_range_monte_carlo
from math import inf

def explore(root: Node, opp_hand_rank_probs, duration: float = 1.0, exploration: float = 1):

    start_time = datetime.now()

    while (datetime.now() - start_time).total_seconds() < duration:

        opp_hand = create_opp_hand_from_rank_distribution(opp_hand_rank_probs,
                                                          list(map(rlcardtoeval7, root.state['public_cards'])),
                                                          list(map(rlcardtoeval7, root.state['hand'])))

        curr_node = select(root, exploration)
        curr_node.state['opp_hand'] = list(map(eval7torlcard, opp_hand))
        sim_start = expand(curr_node)
        result = simulate(sim_start, opp_hand)
        backpropogatge(sim_start, result)

    max_val = -inf
    action = None
    probs=[]
    for child in root.children:
        prob = 0 if child.num_visits == 0 else child.ev/child.num_visits
        probs.append((action_to_num(child.prev_action),prob))
        if prob > max_val:
            action = child.prev_action
            max_val = child.ev/child.num_visits

    prob_sum = sum([prob[1] for prob in probs])
    probs = [(prob[0], prob[1]/prob_sum) for prob in probs]

    return action, probs


def select(root, exploration):

    if len(root.children) == 0:
        return root

    children = []
    if type(root) is Chance:
        for child in root.children:
            opp_hand = child.state['opp_hand']
            used_cards = list(map(rlcardtoeval7, child.state['public_cards'])) + \
                         list(map(rlcardtoeval7, child.state['hand']))
            if opp_hand[0] in used_cards or opp_hand[1] in used_cards:
                pass
            else:
                children.append(child)
    else:
        children = root.children

    max_child = None
    max_val = -math.inf
    for child in children:
        if child.num_visits != 0:
            if child.parent is not None and child.parent.num_visits != 0:
                uct = (child.ev / child.num_visits) + exploration * math.sqrt(math.log(child.parent.num_visits) / child.num_visits)
            else:
                uct = (child.ev / child.num_visits) + exploration * math.sqrt(math.log(1) / child.num_visits)
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


def simulate(node, opp_hand):
    state = node.state
    hand = state['hand']
    public_cards = state['public_cards']
    # print(str(opp_hand[0]) + str(opp_hand[1]))
    # print(HandRange(str(opp_hand[0]) + str(opp_hand[1])))
    # print(list(map(rlcardtoeval7, hand)), str(opp_hand[0]) + str(opp_hand[1]), list(map(rlcardtoeval7, public_cards)))
    win_prob = py_hand_vs_range_monte_carlo(list(map(rlcardtoeval7, hand)), HandRange(str(opp_hand[0]) + str(opp_hand[1])), list(map(rlcardtoeval7, public_cards)), 1000)

    if len(public_cards) == 0:
        remaining_rounds = 3
    elif len(public_cards) == 3:
        remaining_rounds = 2
    elif len(public_cards) == 4:
        remaining_rounds = 1
    else:
        remaining_rounds = 0

    ev = win_prob * (sum(state['all_chips']) + remaining_rounds)
    return ev


def backpropogatge(node, profit):
    while node.parent is not None:
        numerator = 0.0
        denominator = 0.0
        for child in node.children:
            numerator += child.ev * child.num_visits
            denominator += child.num_visits
        profit = profit if denominator == 0 else numerator/denominator
        node.update(profit)
        node = node.parent

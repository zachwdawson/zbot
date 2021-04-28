import eval7
import itertools
from eval7 import Card, HandRange, Deck
import random
import pandas as pd

def eval7torlcard(card: Card):
    card_str = str(card)
    return card_str[1].upper() + card_str[0]

def rlcardtoeval7(card: str):
    return Card(card[1] + card[0].lower())

def action_to_num(action):
    if action is None:
        return 0
    if action in ['check', 'call']:
        return 1
    elif action in ['bet', 'raise']:
        return 2
    else:
        return 0

def hand_rank_to_num(rank):
        if rank is None:
            return 0
        elif rank == 'High Card':
            return 0
        elif rank == 'Pair':
            return 1
        elif rank == 'Two Pair':
            return 2
        elif rank == 'Trips':
            return 3
        elif rank == 'Straight':
            return 4
        elif rank == 'Flush':
            return 5
        else:
            return 6

def create_opp_hand_from_rank_distribution(opp_hand_rank_probas, public_cards, my_hand):
    deck = Deck()
    potential_hands = []

    remaining_cards = list(set(deck.cards) - set(public_cards + my_hand))
    selected_hand_rank = random.choices(['High Card', 'Pair', 'Two Pair', 'Trips', 'Straight', 'Flush', 'Nuts'], weights=opp_hand_rank_probas[0])
    for hand in itertools.combinations(remaining_cards, 2):
        hand_strength = eval7.evaluate(public_cards + list(hand))
        hand_rank = eval7.handtype(hand_strength)
        # print(selected_hand_rank)
        if hand_rank in selected_hand_rank:
            potential_hands.append(hand)
        elif selected_hand_rank == 'Nuts' and hand_rank in ['Quads', 'Full House', 'Straight Flush']:
            potential_hands.append(hand)

    return (remaining_cards[0], remaining_cards[1]) if len(potential_hands) == 0 else random.choice(potential_hands)

def calc_num_outs(curr_hand):
    # no outs pre flop
    deck = Deck()
    if len(curr_hand) == 2:
        return 0

    # calculate outs after flop and turn
    deck = eval7.Deck()
    remaining_cards = list(set(deck.cards) - set(curr_hand))
    num_outs = 0
    curr_strength = eval7.evaluate(curr_hand)
    curr_rank = eval7.handtype(curr_strength)
    for card in remaining_cards:
        hand = curr_hand + [card]
        hand_strength = eval7.evaluate(hand)
        hand_rank = eval7.handtype(hand_strength)
        if hand_strength > curr_strength and hand_rank != curr_rank:
            num_outs += 1

    return num_outs


def calc_win_prob(communal_cards, hole_cards, num_outs):
    if len(communal_cards) == 0:
        pre_flop_fn = '/home/dawson.z/zbot/data/pre_flop_hand_rank.csv'

        pre_flop_df = pd.read_csv(pre_flop_fn, delim_whitespace=True)
        pre_flop_df = pre_flop_df.set_index('Hole')

        card1 = str(hole_cards[0])[0]
        card2 = str(hole_cards[1])[0]
        hand = card1 + card2
        try:
            pre_flop_df.loc[hand, 'Wins'] + pre_flop_df.loc[hand, 'Ties'] * 0.5
        except:
            hand = card2 + card1

        if hole_cards[0].suit == hole_cards[1].suit:
            hand += 's'

        return pre_flop_df.loc[hand, 'Wins'] + pre_flop_df.loc[hand, 'Ties'] * 0.5
    else:
        return num_outs * 2.1  # value of one out as a percentage


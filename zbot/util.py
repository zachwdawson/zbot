import eval7
import itertools
from eval7 import Card, HandRange, Deck
import random

def eval7torlcard(card: Card):
    card_str = str(card)
    return card_str[1].upper() + card_str[0]

def rlcardtoeval7(card: str):
    return Card(card[1] + card[0].lower())

def action_to_num(action:str):
    if action in ['check', 'call']:
        return 1
    elif action in ['bet', 'raise']:
        return 2
    else:
        return 0

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


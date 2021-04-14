import eval7
from eval7 import Card, HandRange

FIFTY = HandRange("22+, A2s+, K2s+, Q4s+, J6s+, T6s+, 95s+, 84s+, 74s+, 63s+, 53s+, 43s, A2o+, K8o+, Q8o+, J8o+, T8o+, 98o")
FORTY = HandRange("22+, A2s+, K2s+, Q5s+, J7s+, T6s+, 96s+, 85s+, 75s+, 64s+, 53s+, 43s, A4o+, K9o+, Q9o+, J9o+, T9o, 98o")
TWENTY5 = HandRange("22+, A2s+, K5s+, Q8s+, J8s+, T8s+, 97s+, 86s+, 75s+, 65s, 54s, ATo+, KTo+, QTo+, JTo")
TEN = HandRange("77+, ATs+, KTs+, QTs+, J9s+, T9s, 98s, A5s, AQo+")

def eval7torlcard(card: Card):
    card_str = str(card)
    return card_str[1].upper() + card_str[0]

def rlcardtoeval7(card: str):
    return Card(card[1] + card[0].lower())

def p_win_v_random(hand, total_cards):
    if len(total_cards) == 0:
        range = FIFTY
    elif len(total_cards) == 3:
        range = FORTY
    elif len(total_cards) == 4:
        range = TWENTY5
    else:
        range = TEN
    win_prob = eval7.equity.py_hand_vs_range_exact(hand, range, total_cards)
    return win_prob


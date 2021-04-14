from eval7 import Card
from typing import Tuple, Dict
from action import Action
from stage import Stage



class Player(object):
    
    def __init__(self, name: str, stack:int, hand:Tuple[Card, Card], dealer: bool):
        self.name = name
        self.stack = stack
        self.hand = hand
        self.dealer = dealer
    
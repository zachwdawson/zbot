from eval7 import Card
from typing import Tuple, Dict, List
from action import Action
from player import Player


class Hand(object):
    
    def __init__(self, players: List[Player],
                 preflop_action: List[Action], postflop_action: List[Action],
                 turn_action: List[Action], river_action: List[Action], 
                 board: List[Card]):
        self.players = players
        self.board = board
        self.preflop_action = preflop_action
        self.postflop_action = postflop_action
        self.turn_action = turn_action
        self.river_action = river_action
        
        
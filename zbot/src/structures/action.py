# -*- coding: utf-8 -*-

from src.structures.action_type import ActionType

class Action(object):
    
    def __init__(self, description:str = "", action_type: ActionType = None, amount:int = 0, player_name: str = None):
        if action_type:
            self.amount = amount
            self.action_type = action_type
            self.description = description
            self.player_name = player_name
        else:
            self.description = description
            self.action_type, self.amount, self.player_name = self.process_raw(description)
            
    
    def get_amount(self):
        return self.amount
    
    def get_descr(self):
        return self.description
    
    def process_raw(self, description):
        components = description.split(' ')
        player = components[0]
        if components[1] == 'folds':
            return ActionType.F, 0, player
        elif components[1] == 'wins':
            return ActionType.W, float(components[2][1:]), player
        elif components[1] == 'calls':
            return ActionType.C, float(components[2][1:]), player
        elif components[1] == 'checks':
            return ActionType.K, 0, player
        elif components[1] == 'shows':
            return ActionType.S, 0, player
        
        amount = float(components[-1:][0][1:])
        if 'posts small blind' in description:
            return  ActionType.SB, amount, player
        elif 'posts big blind' in description:
            return  ActionType.BB, amount, player
        elif components[1] == 'bets':
            return ActionType.B, amount, player
        elif components[1] == 'raises':
            return ActionType.R, amount, player
        
        return ActionType.BROKE, 0, None
            
    
    
    
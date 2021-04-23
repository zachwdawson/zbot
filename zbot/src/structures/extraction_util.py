# -*- coding: utf-8 -*-
from src.structures.player import Player
from src.structures.hand import Hand
from src.structures.action_type import ActionType
from src.structures.action import Action
from src.structures.decision import Decision
from src.structures.stage import Stage
from typing import List, Dict
import pandas as pd
import eval7
import re

def process_hand_history_simple(file: str):
    hands = []
    hand = {}
    stage = Stage.PRE_FLOP
    players = []
    pre_flop = []
    post_flop = []
    turn = []
    river = []
    communal_cards = ""
    
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('******************************'):
                hand_stage = ''
                hand['players'] = players
                hand['pre_flop'] = pre_flop
                hand['post_flop'] = post_flop
                hand['turn'] = turn
                hand['river'] = river
                hand['communal_cards'] = [eval7.Card(s) for s in communal_cards]
                hands.append(hand)
                hand = {}
                stage = Stage.PRE_FLOP
                players = []
                pre_flop = []
                post_flop = []
                turn = []
                river = []
                communal_cards = ""
            else:
                if re.search('^\s*[0-9]\)', line.strip()) and 'sitting out' not in line:
                    components = line.strip().split(' ')
                    if '*' in components:
                        dealer = True
                    else:
                        dealer = False
                    components = list(filter(lambda a : a != '' and a != '*', components))
                    players.append({'name': components[1], 'starting_stack': components[-3:-2], 'hand': (components[-2:-1], components[-1:]), 'dealer': dealer})
                elif line.startswith('FLOP'):
                    stage = Stage.POST_FLOP
                    components = line.strip().split(' ')
                    components = list(filter(lambda a : a != '' and a != '*', components))
                    communal_cards = components[2:]
                elif line.startswith('TURN'):
                    stage = Stage.TURN
                    components = line.strip().split(' ')
                    components = list(filter(lambda a : a != '' and a != '*', components))
                    communal_cards = components[2:]
                elif line.startswith('RIVER'):
                    stage = Stage.RIVER
                    components = line.strip().split(' ')
                    components = list(filter(lambda a : a != '' and a != '*', components))
                    communal_cards = components[2:]
                elif 'posts small blind' in line:
                    pre_flop.append(line)
                elif 'posts big blind' in line:
                    pre_flop.append(line)
                elif 'calls' in line:
                    if stage == Stage.PRE_FLOP:
                        pre_flop.append(line)
                    elif stage == Stage.POST_FLOP:
                        post_flop.append(line)
                    elif stage == Stage.TURN:
                        turn.append(line)
                    elif stage == Stage.RIVER:
                        river.append(line)
                elif 'checks' in line:
                    if stage == Stage.PRE_FLOP:
                        pre_flop.append(line)
                    elif stage == Stage.POST_FLOP:
                        post_flop.append(line)
                    elif stage == Stage.TURN:
                        turn.append(line)
                    elif stage == Stage.RIVER:
                        river.append(line)
                elif 'bets' in line:
                    if stage == Stage.PRE_FLOP:
                        pre_flop.append(line)
                    elif stage == Stage.POST_FLOP:
                        post_flop.append(line)
                    elif stage == Stage.TURN:
                        turn.append(line)
                    elif stage == Stage.RIVER:
                        river.append(line)
                elif 'raises' in line:
                    if stage == Stage.PRE_FLOP:
                        pre_flop.append(line)
                    elif stage == Stage.POST_FLOP:
                        post_flop.append(line)
                    elif stage == Stage.TURN:
                        turn.append(line)
                    elif stage == Stage.RIVER:
                        river.append(line)
                elif 'folds' in line:
                    if stage == Stage.PRE_FLOP:
                        pre_flop.append(line)
                    elif stage == Stage.POST_FLOP:
                        post_flop.append(line)
                    elif stage == Stage.TURN:
                        turn.append(line)
                    elif stage == Stage.RIVER:
                        river.append(line)
                elif 'shows' in line:
                    if stage == Stage.PRE_FLOP:
                        pre_flop.append(line)
                    elif stage == Stage.POST_FLOP:
                        post_flop.append(line)
                    elif stage == Stage.TURN:
                        turn.append(line)
                    elif stage == Stage.RIVER:
                        river.append(line)
                elif 'wins' in line:
                    if stage == Stage.PRE_FLOP:
                        pre_flop.append(line)
                    elif stage == Stage.POST_FLOP:
                        post_flop.append(line)
                    elif stage == Stage.TURN:
                        turn.append(line)
                    elif stage == Stage.RIVER:
                        river.append(line)
        f.close()
        
    return hands

def process_hand_dicts_simple(hands: List[Dict]):
    hand_objs = []
    for hand in hands:
        players = []
        for player in hand['players']:
            players.append(Player(player['name'], player['starting_stack'], tuple(player['hand']), player['dealer']))
            
        # process preflop
        pre_flop = []
        for action in hand['pre_flop']:
            pre_flop.append(Action(action))
            
        # process postflop
        post_flop = []
        for action in hand['post_flop']:
            post_flop.append(Action(action))
            
        # process turn
        turn = []
        for action in hand['turn']:
            turn.append(Action(action))
            
        # process river
        river = []
        for action in hand['river']:
            river.append(Action(action))
        
        hand_objs.append(Hand(players, pre_flop, post_flop, turn, river, hand['communal_cards'])) 
    return hand_objs

def create_decisions_from_hand(hand: Hand):
    columns = ['target', 'stage', 'dealer', 'hand_strength', 'hand_rank', 'opp_last_action',
        'my_last_action', 'my_stack_committed_curr_phase', 'opp_stack_committed_curr_phase',
        'my_num_raises_curr_phase', 'opp_num_raises_curr_phase',
        'my_num_raises_total', 'opp_num_raises_total','num_outs', 
        'winning_prob','highest_card', 'num_aces', 'num_kings', 'num_queens']
    df_decision = pd.DataFrame(columns=columns)
    board = hand.board
    
    players = {}
    decisions = []
    
    for player in hand.players:
        player_hand = (eval7.Card(player.hand[0][0]), eval7.Card(player.hand[1][0]))
        players[player.name] = {'stack': player.stack,
                                'hand':player_hand,
                                'dealer': player.dealer,
                                'last-action': None,
                                'stack-curr': 0,
                                'stack-full': 0,
                                'num-raises-curr': 0,
                                'num-raises-full': 0}
    
    # -------------------- pre ----------------------
    for action in hand.preflop_action:
        opp_name = [key for key in players.keys() if key != action.player_name][0]
        decision = Decision(action, players[action.player_name]['hand'], [],
                 Stage.PRE_FLOP, players[action.player_name]['dealer'],
                 players[opp_name]['last-action'], players[action.player_name]['last-action'], 
                 players[opp_name]['stack-curr'], players[action.player_name]['stack-curr'],
                 players[opp_name]['num-raises-curr'], players[action.player_name]['num-raises-curr'],
                 players[opp_name]['num-raises-full'], players[action.player_name]['num-raises-full'])
        decisions.append(decision)
        
        if action.action_type == ActionType.F:
            break
            
        players[action.player_name]['last-action'] = action
        players[action.player_name]['stack-curr'] += action.amount
        players[action.player_name]['stack-full'] += action.amount
        players[action.player_name]['num-raises-curr'] += 1
        players[action.player_name]['num-raises-full'] += 1
    
    # -------------------- post ----------------------
    players[action.player_name]['num-raises-curr'] = 0
    players[opp_name]['num-raises-curr'] = 0
    players[action.player_name]['stack-curr'] = 0
    players[opp_name]['stack-curr'] = 0
    
    for action in hand.postflop_action:
        opp_name = [key for key in players.keys() if key != action.player_name][0]
        decision = Decision(action, players[action.player_name]['hand'], board[0:3],
                 Stage.POST_FLOP, players[action.player_name]['dealer'],
                 players[opp_name]['last-action'], players[action.player_name]['last-action'], 
                 players[opp_name]['stack-curr'], players[action.player_name]['stack-curr'],
                 players[opp_name]['num-raises-curr'], players[action.player_name]['num-raises-curr'],
                 players[opp_name]['num-raises-full'], players[action.player_name]['num-raises-full'])
        decisions.append(decision)
        
        if action.action_type == ActionType.F:
            break
            
        players[action.player_name]['last-action'] = action
        players[action.player_name]['stack-curr'] += action.amount
        players[action.player_name]['stack-full'] += action.amount
        players[action.player_name]['num-raises-curr'] += action.amount
        players[action.player_name]['num-raises-full'] += action.amount
    
    players[action.player_name]['num-raises-curr'] = 0
    players[opp_name]['num-raises-curr'] = 0
    players[action.player_name]['stack-curr'] = 0
    players[opp_name]['stack-curr'] = 0
    
    # -------------------- turn ----------------------
    players[action.player_name]['num-raises-curr'] = 0
    players[opp_name]['num-raises-curr'] = 0
    players[action.player_name]['stack-curr'] = 0
    players[opp_name]['stack-curr'] = 0
    
    for action in hand.turn_action:
        opp_name = [key for key in players.keys() if key != action.player_name][0]
        decision = Decision(action, players[action.player_name]['hand'], board[0:4],
                 Stage.TURN, players[action.player_name]['dealer'],
                 players[opp_name]['last-action'], players[action.player_name]['last-action'], 
                 players[opp_name]['stack-curr'], players[action.player_name]['stack-curr'],
                 players[opp_name]['num-raises-curr'], players[action.player_name]['num-raises-curr'],
                 players[opp_name]['num-raises-full'], players[action.player_name]['num-raises-full'])
        decisions.append(decision)
        
        if action.action_type == ActionType.F:
            break
            
        players[action.player_name]['last-action'] = action
        players[action.player_name]['stack-curr'] += action.amount
        players[action.player_name]['stack-full'] += action.amount
        players[action.player_name]['num-raises-curr'] += action.amount
        players[action.player_name]['num-raises-full'] += action.amount
    
    # -------------------- river ----------------------
    players[action.player_name]['num-raises-curr'] = 0
    players[opp_name]['num-raises-curr'] = 0
    players[action.player_name]['stack-curr'] = 0
    players[opp_name]['stack-curr'] = 0
    
    for action in hand.river_action:
        opp_name = [key for key in players.keys() if key != action.player_name][0]
        decision = Decision(action, players[action.player_name]['hand'], board[0:5],
                 Stage.RIVER, players[action.player_name]['dealer'],
                 players[opp_name]['last-action'], players[action.player_name]['last-action'], 
                 players[opp_name]['stack-curr'], players[action.player_name]['stack-curr'],
                 players[opp_name]['num-raises-curr'], players[action.player_name]['num-raises-curr'],
                 players[opp_name]['num-raises-full'], players[action.player_name]['num-raises-full'])
        decisions.append(decision)
        
        if action.action_type == ActionType.F:
            break
            
        players[action.player_name]['last-action'] = action
        players[action.player_name]['stack-curr'] += action.amount
        players[action.player_name]['stack-full'] += action.amount
        players[action.player_name]['num-raises-curr'] += action.amount
        players[action.player_name]['num-raises-full'] += action.amount



    for decision in decisions:
        my_last_action = None if decision.my_last_action == None else decision.my_last_action.action_type.value
        opp_last_action = None if decision.opp_last_action == None else decision.opp_last_action.action_type.value
        highest_card = None if decision.highest_card == None else decision.highest_card.rank
        df_decision.loc[len(df_decision.index)] = [decision.actual_outcome.action_type.value, decision.stage.value,
                            decision.dealer, decision.hand_strength, decision.hand_rank, 
                            my_last_action, opp_last_action, 
                            decision.my_stack_committed_curr_phase, decision.opp_stack_committed_curr_phase,
                            decision.my_num_raises_curr_phase, decision.opp_num_raises_curr_phase,
                            decision.my_num_raises_total, decision.opp_num_raises_total, decision.num_outs, 
                            decision.winning_prob, highest_card, decision.num_aces,
                            decision.num_kings, decision.num_queens]
    
    return df_decision
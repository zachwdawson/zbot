#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 22:44:26 2021

@author: zacharydawson
"""

"""
Decision Features: 
    
    1 Hand strength 
        Enumerate over all (N choose 2) remaining card combinations
        for a given board and count wins losses and ties to determine hand strength.
    2 PPot 
        The chance that a hand that is not currently the best improves to win at showdown.
            Enumerate ove all opponent hands and all possible turns and river. Very expensive.
            Might not be feasible but can substitute with a prediction for the #outs 
    3 NPot
        The chance that a currently leading hand ends up losing. Same as PPot
    4 Whether the player is dealer or not.
        if num_players_x = position dealter = True
    5 Last action of the opponent (null, call, raise, or all-in)
        preflop_action flop_action turn_action river_action
    6 Last action of the opponent
    in context (null, check, call, bet, raise, or all in)
        preflop_action flop_action turn_action river_action
    7 Stack (money) committed by the player in this phase
        In player state potentially
    8 Stack committed by the opponent in this phase
        In player state potentially
    9 Number of raises by the the player in this phase
        preflop_action flop_action turn_action river_action 'b' and 'r'
    10 Number of raises by the opponents in this phase
         preflop_action flop_action turn_action river_action 'b' and 'r'
    11 Number of checks before the player in this phase
         preflop_action flop_action turn_action river_action 'c' and 'k'
    12 Hand rank
        Basic rules of poker
    13 Winning probability
        P(win) = HS × (1 − NP ot) + (1 − HS) × P P ot (1)
    14 Hand outs
        Need fast way to lookup how hand ranks in terms of outs
    15 Number of raises by the player in previous phases
        preflop_action flop_action turn_action river_action 'b' and 'r'
    16 Number of raises by the opponents in previous phases
        preflop_action flop_action turn_action river_action 'b' and 'r'
    17 Number of players left to act after the player
        Check for 'f' or '-' in previous round action to determine who still acts
    19 Highest valued card on the board
        Check 'board' cards up to current phase length
    20 Number of queens on the board
        Check 'board' cards up to current phase length
    21 Number of kings on the board
        Check 'board' cards up to current phase length
    22 Number of aces on the board
        Check 'board' cards up to current phase length


Statistic features:
    VPIP
    check preflop action in each player file and calculate percent of hands where player limps or raises
    PFR
    check preflop action in each player file and calculate the percent of hands where players raise only
    Agg
    postflop (bets + raises)/calls
    Average preflop pot size for table (BB)
    intractable
    Average final pot size for table (BB)
    intractable
    
    
    
God Mode:
    Other hole cards
    
"""
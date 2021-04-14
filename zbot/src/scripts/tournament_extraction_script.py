#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 20:44:52 2021

@author: zacharydawson
"""

import os
import glob
import pandas as pd


tourney_dir = '/Users/zacharydawson/artificial-intelligence/poker/data/IRCdata/tourney/200110'

dirs = glob.glob(tourney_dir)

for directory in dirs:
    #hdb_main
    hdb_orig = os.path.join(directory, 'hdb')
    hdb_main = os.path.join(directory, 'hdb_main')
    hdb_board = os.path.join(directory, 'hdb_board')
    os.system('cut -c-59 %s > %s'%(hdb_orig, hdb_main))
    os.system('cut -c60- %s > %s'%(hdb_orig, hdb_board))
    
    #hroster_main
    hroster_orig = os.path.join(directory, 'hroster')
    hroster_main = os.path.join(directory, 'hroster_main')
    hrsoter_players = os.path.join(directory, 'hroster_players')
    
    os.system('cut -c-13 %s > %s'%(os.path.join(directory, 'hroster'), os.path.join(directory, 'hroster_main')))
    os.system('cut -c14- %s > %s'%(os.path.join(directory, 'hroster'), os.path.join(directory, 'hroster_players')))
    
    #pdb_main
    pdb_paths = glob.glob(os.path.join(directory, 'pdb/*'))
    pdb_main = os.path.join(directory, 'pdb_main')
    
    with open(pdb_main,'w') as f:
        f.write("name timestamp num_players position preflop_action flop_action turn_action river_action bankroll action winnings card1 card2")
        f.close()

    for path in pdb_paths:
        os.system('cat %s >> %s'%(path, os.path.join(directory, 'pdb_main')))
    
    #pdb individual
    full_player_stats = {}
    for path in pdb_paths:
        player_name = os.path.basename(path)
        player_stats = {}
        with open(path,'r') as f1:
            with open('newfile.txt', 'w') as f2:
                f2.write("name timestamp num_players position preflop_action flop_action turn_action river_action bankroll action winnings card1 card2")
                f2.write(f1.read())
                f2.close()
                f1.close()
        os.rename('newfile.txt', path)
        
        player_df = pd.read_csv(path, delim_whitespace=True,low_memory=False)
        pre = player_df['preflop_action'].sum()
        post = player_df['preflop_action'].sum() + player_df['turn_action'].sum() + player_df['river_action'].sum()
        
        player_stats['pre'] = pre
        player_stats['post'] = post
        
        full_player_stats[player_name] = player_stats
    
    stats_df = pd.DataFrame(full_player_stats)
    print(stats_df.head(5))
    stats_df.to_csv(os.path.join(directory, 'player_stats.csv'))
        
        
        
        
        
        
    
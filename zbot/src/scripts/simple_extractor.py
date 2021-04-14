#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('/Users/zacharydawson/artificial-intelligence/poker/zbot/src/structures')
from subprocess import call
from extraction_util import process_hand_history_simple, process_hand_dicts_simple, create_decisions_from_hand

paths = ['/Users/zacharydawson/artificial-intelligence/poker/data/hand_histories/SBvMB-600.txt']

#paths = ['/Users/zacharydawson/artificial-intelligence/poker/data/hand_histories/SBvMB-9.txt',
#         '/Users/zacharydawson/artificial-intelligence/poker/data/hand_histories/SBvMB-38.txt',
#         '/Users/zacharydawson/artificial-intelligence/poker/data/hand_histories/SBvMB-150.txt',
#         '/Users/zacharydawson/artificial-intelligence/poker/data/hand_histories/SBvMB-600.txt']

out = '/Users/zacharydawson/artificial-intelligence/poker/data/hand_histories/test.csv'

header = True

for file in paths:
    hands = process_hand_history_simple(file)
    
    hands = process_hand_dicts_simple(hands)
    
    with open(out, 'w') as f:
        for hand in hands:
            new_decisions = create_decisions_from_hand(hand)
            tmp = '/Users/zacharydawson/artificial-intelligence/poker/data/hand_histories/tmp.csv'
            new_decisions.to_csv(tmp, header=header)
            script = "cat %s >> %s"%(tmp, out)
            call(script, shell=True)
            header = False
    f.close()
            
            


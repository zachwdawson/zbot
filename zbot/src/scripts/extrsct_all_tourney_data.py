#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 23:25:37 2021

@author: zacharydawson
"""

import os
import glob

dirs = glob.glob('/Users/zacharydawson/artificial-intelligence/poker/IRCdata/tourney.*.tgz')

for directories in dirs:
    os.system('tar zxvf %s'%directories)
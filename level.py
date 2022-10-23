#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 12:47:44 2022

@author: max
"""

import pygame as pg
import numpy as np
from settings import *
from stats import *
from lib import *

grid = create_grid(w=18,h=10,win_w = win_w, win_h=win_h)
#terrain setup
blocks += [block('wall.jpg',x=10,y=i,solid = True) for i in range(5) if i != 3]
blocks += [block('wall.jpg',x=i,y=5,solid = True) for i in range(5,11) if i != 8]
blocks.append(directionalDoor('door.png',x=8,y=5,orientation = 'bot'))
blocks.append(directionalDoor('door.png',x=10,y=3,orientation = 'right'))

#fighters setup
n_teams = 2
team1 = [fighter('cheems_batte.png', 4,4 , cheems_stats, [pitchfork()]),
         scout('cheems_scout.png', 8,4 ,stats = cheems_stats, items = [pitchfork()]),
         fighter("dogeatthan.png",5,2, dogeatthan_stats, [comet()])]

team2 = [fighter('choge.jpg',15,2, choge_stats, [bareFist()],team = 2), 
         fighter("dogion.png",13,4, dogion_stats, [maw()], team = 2),
         fighter("dogion.png",17,5, dogion_stats, [maw()], team = 2)]

teams = [team1, team2]
fighters += team1 + team2
blocks += fighters

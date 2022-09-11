#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 00:12:33 2022

@author: max
"""
from dataclasses import dataclass

cheems_stats = { 'hp':20, 'atk':7,'pm':6, 'deff':4,'res':2}
choge_stats = {'hp':33, 'atk':14, 'pm':5, 'deff':7, 'res':6}
dogeatthan_stats = {"hp":17, 'atk':5, 'mag':12, 'pm':4, 'deff':1, 'res':9 }
dogion_stats = {'hp':15, 'atk':7,'pm':6,'deff':2,'res':0}

@dataclass
class pitchfork():
    dmg = 7
    acc = 90
    range = [1]
    dmg_type = 'physical'

@dataclass
class comet():
    dmg = 9
    acc = 85
    range = [1,2]
    dmg_type = 'magic'

@dataclass
class maw():
    dmg = 5
    acc = 80
    range = [1]
    dmg_type = 'physical'

@dataclass
class bareFist():
    dmg = 0
    acc = 90
    range = [1]
    dmg_type = "physical"
    
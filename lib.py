#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 12:45:28 2022

@author: max
"""
import pygame as pg
import numpy as np

player = None
fighters = []
blocks = []
turn = 1
playing_team = 1


class Grid():
    def __init__(self, w, h, win_w, win_h):             
        self.g = np.empty((w,h),dtype= object)
        for i in range(w):
            for l in range(h):
                self.g[i,l] = []
        self.w, self.h = w, h
        self.tile_w, self.tile_h = win_w //w, win_h // h
    def __getitem__(self, key):
        return self.g[key]
    def __repr__(self):
        return str(self.g) + f'\n h:{self.w}, w:{self.h}, t_h:{self.tile_w}, t_w:{self.tile_h}'


grid = Grid(18,10,800,500)




""" ============== BLOCKS =================== """

class block(pg.sprite.Sprite):
    name = ''
    x,y = 0,0
    def __init__(self,img_path, x, y,solid = False):
        super().__init__()
        self.x, self.y = x,y
        self.solid = solid
        base_img = pg.image.load('assets/'+img_path)
        self.img = pg.transform.scale(base_img, (grid.tile_w,grid.tile_h))
        self.rect = self.img.get_rect()
        grid[x,y].append(self)
        
class fighter(block):
    can_attack = True
    def __init__(self,img_path,x,y, stats, items, team = 1):
        super().__init__(img_path ,x,y,solid = True)
        self.team, self.items, self.grid = team, items, grid
        for k,v in stats.items():
            setattr(self, k, v) #modifiable stats
            setattr(self, 'base_'+k, v) #base stats 
    @property
    def hp(self):
        return self.__hp
    
    @hp.setter
    def hp(self,value):
        self.__hp = value
        if self.hp <= 0:
            self.die()
    def has_attacked(self):
        self.can_attack = False
        self.pm = 0
    def die(self):
        fighters.remove(self)
        blocks.remove(self)
        global player
        if player == self:
            print("deleting self")
            player = None
        print(self, "dying")
        self.grid[self.x,self.y].remove(self)

class scout(fighter):
    def __init__(self, img_path, x, y, stats, items, team = 1):
        super().__init__(img_path, x, y, stats, items, team )
    def has_attacked(self):
        self.can_attack = False
class directionalDoor(block):
    def __init__(self,img_path, x ,y, orientation: str):
        super().__init__(img_path,x,y,solid = False)  
        self.orientation = orientation
        if orientation == 'right':
            self.img = pg.transform.rotate(self.img, 90)
        elif orientation == 'top':
            self.img = pg.transform.rotate(self.img, 180)
        elif orientation == 'left':
            self.img = pg.transform.rotate(self.img, 270)





""" "============== PATHFINDING =================== """

from collections import namedtuple
from dataclasses import dataclass

def is_passable(x,y,target):
    if x >= grid.shape[0] or y >= grid.shape[1]:
        return False
    return not sum(b.solid for b in grid[x,y])

def has_collision(target,x,y):
    n_coll = 0
    for b in grid[x,y]:
        print(b)
        if b.solid:
            n_coll += 1
        if isinstance(b,directionalDoor):
            if b.orientation == 'left' and target.x != x +1:
                n_coll += 1
            elif b.orientation == 'right' and target.x != x -1:
                n_coll += 1
            elif b.orientation == 'top' and target.y != y +1:
                n_coll += 1
            elif b.orientation == 'bot' and target.y != y -1:
                n_coll += 1 
    return bool(n_coll)

class node():
    dist = None
    prev = None
    cost = None
    def __init__(self,x,y, prev = None):
        if prev:
            self.cost = prev.cost + 1
        self.prev = prev
        self.x, self.y = x,y
    def __repr__(self):
        return f"node(x={self.x},y={self.y},dist={self.dist}, cost = {self.cost})"
    def __eq__(self, other):
        if isinstance(other, node):
            return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))
    
def find_path(base,target, obstacles = set(), max_nodes = 200, max_cost = 12):
    base.cost = 0
    frontier = [base]
    expanded = set()
       
    while True:
        if len(frontier) == 0:
            print("no path found")
            return expanded, frontier, None  
        current = frontier[0]
        for n in frontier:
            if n.dist < current.dist:
                current = n
        
        if len(expanded) > max_nodes:
            print("max number of expanded nodes exeeded")
            return expanded, frontier, None   
        if current == target:
            print("found target")
            path = []
            while current.prev != None:
                path.append(current.prev)
                current = current.prev
            return expanded, frontier, path
        
        expanded.add(current)
        print(current)
        frontier.remove(current)
        
        x,y = current.x, current.y
        childs = [node(x+1,y, prev = current), node(x-1,y, prev = current),
                  node(x,y+1,prev = current), node(x,y-1, prev = current)]
        frontier += {c for c in childs if c not in obstacles and c not in expanded and c.cost+c.dist <= max_cost}

def find_movable_squares(target, grid):
    max_cost = target.pm
    current = node(target.x, target.y)
    current.cost = 0
    expanded, frontier = set(), {current}
    while len(frontier) > 0:
        current = min((n for n in frontier), key = lambda n : n.cost)
        frontier.remove(current)
        expanded.add(current)
        
        x,y = current.x, current.y
        childs = [node(x+1,y), node(x-1,y), node(x,y+1), node(x,y-1)]
        for c in childs:
            c.cost = current.cost + 1
            if c.cost <= max_cost and c not in expanded and is_passable(c.x,c.y,target, grid) and c not in frontier:
                frontier.add(c)
    expanded.remove(node(target.x,target.y))  
    return expanded


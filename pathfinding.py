#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 21:51:26 2022

@author: max
"""

from collections import namedtuple
from dataclasses import dataclass

from lib import is_passable

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




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 21:51:26 2022

@author: max
"""

from collections import namedtuple
from dataclasses import dataclass

class node():
    dist = None
    prev = None
    cost = None
    dist = None
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

def find_movable_squares(current,obstacles = {}, max_cost = 6):
    current.cost = 0
    expanded, frontier = set(), [current]
    while len(frontier) > 0:
        current = min((n for n in frontier), key = lambda n : n.cost)
        frontier.remove(current)
        expanded.add(current)
        
        x,y = current.x, current.y
        childs = [node(x+1,y), node(x-1,y), node(x,y+1), node(x,y-1)]
        for c in childs:
            c.cost = current.cost + 1
            if c.cost <= max_cost and c not in expanded and c not in obstacles and c not in frontier:
                frontier.append(c)
                
    return expanded, frontier

def is_passable(node):
    return node not in obstacles     

if __name__ == "__main__":
    import pygame as pg
    pg.init()
    
    search_mode = 'find'
    frontier = []
    expanded = []
    target = None
    target = node(2,2)
    base = node(7,7)
    obstacles = {node(6,16),node(6,17),node(6,18),node(7,16),node(8,16)}
    i = 0
            
    win_w,win_h = 900, 500
    win = pg.display.set_mode((win_w,win_h))
    
    WHITE, BLACK = (255,255,255), (0,0,0)
    
    grid_w, grid_h = 18,10
    tile_w, tile_h = win_w//grid_w, win_h//grid_h
    
    def place_block(pos):
        global base
        global target
        global expanded
        global frontier
        global path
        
        x,y = pos[0] // tile_w, pos[1] // tile_w
        if mode == 'base':
            base = node(x,y)
        if mode == 'target':
            target = node(x,y)
        if mode == 'obstacle':
            obstacles.add(node(x,y))
        print("base:",base,'target:',target)
        if search_mode == 'find':
            expanded, frontier, path = find_path(base, target, obstacles)
        elif search_mode == 'possible':
            expanded, frontier = find_movable_squares(base,obstacles, max_cost = 6) 
            path = []
    
    #drawing stuff 
    def draw_grid():
        for i in range(grid_w):
            pg.draw.line(win,BLACK,(i*tile_w,0),(i*tile_w, win_h))
        for i in range(grid_h):
            pg.draw.line(win, BLACK, (0,i*tile_h),(win_w,i*tile_h))
    
    def draw_blocks():
        for o in obstacles:
            pg.draw.rect(win,(170,120,155),pg.Rect(o.x * tile_w, o.y * tile_h, tile_w , tile_h))
        for n in expanded:
            pg.draw.rect(win,(0,0,160),pg.Rect(n.x * tile_w, n.y * tile_h, tile_w-5 , tile_h-5))   
        for f in frontier:
            pg.draw.rect(win, (120,120,160),
                         pg.Rect(f.x * tile_w + 5, f.y * tile_h + 5,
                                 tile_h - 15, tile_w - 15))
        if path != None:
            for n in path:
                pg.draw.rect(win,(160,0,160),pg.Rect(n.x * tile_w, n.y * tile_h, tile_w-5 , tile_h-5))
        pg.draw.rect(win,(0,250,0),pg.Rect(base.x * tile_w, base.y * tile_h, tile_w-5 , tile_h-5))
        pg.draw.rect(win,(250,0,0),pg.Rect(target.x * tile_w, target.y * tile_h, tile_w-5 , tile_h-5))
    clock = pg.time.Clock()
    fps = 60
    running = True
    mode = 'base'
    path = []
    while running:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False   
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_b:
                    mode = 'base'
                if event.key == pg.K_t:
                    mode = 'target'
                if event.key == pg.K_o:
                    mode = 'obstacle'  
                if event.key == pg.K_f:
                    search_mode = 'find'
                if event.key == pg.K_p:
                    search_mode = 'possible'
            if event.type == pg.MOUSEBUTTONUP:
                place_block(pg.mouse.get_pos())
        
        
        #draw window ..
        win.fill(WHITE)
        draw_grid()
        draw_blocks()
        pg.display.flip()
             
    pg.quit()
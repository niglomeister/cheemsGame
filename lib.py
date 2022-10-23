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
def create_grid(w,h,win_w,win_h):
        grid = np.empty((w,h),dtype= object)
        grid.w, grid.h = w,h
        for i in range(w):
            for l in range(h):
                grid[w,h] = []
        grid.tile_w, grid.tile_h = win_w //w, win_h // h
        return grid
    
class Grid(np.ndarray):
    def __init__(self,w,h,win_w,win_h):
        #super().__init__([[]])
        pass
grid = Grid([],b'll', 900, 500)
k=k
class block(pg.sprite.Sprite):
    name = ''
    x,y = 0,0
    def __init__(self,img_path, x, y, grid,solid = False):
        super().__init__()
        self.x, self.y = x,y
        self.solid = solid
        base_img = pg.image.load('assets/'+img_path)
        self.img = pg.transform.scale(base_img, (grid.tile_w,grid.tile_h))
        self.rect = self.img.get_rect()
        grid[x,y].append(self)
        
class fighter(block):
    can_attack = True
    def __init__(self,img_path,x,y, stats, items, grid, team = 1):
        super().__init__(img_path ,x,y, grid,solid = True)
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

def is_passable(x,y,target, grid):
    if x >= grid.shape[0] or y >= grid.shape[1]:
        return False
    return not sum(b.solid for b in grid[x,y])
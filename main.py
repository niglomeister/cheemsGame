#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 10:44:17 2022

@author: max
"""
import pygame as pg
import os
import numpy as np

from level import *  
from stats import *
from pathfinding import find_path, find_movable_squares
pg.init()  

win_w,win_h = 900, 500
win = pg.display.set_mode((win_w,win_h))
pg.display.set_caption("best game")

WHITE, BLACK = (255,255,255), (0,0,0)

grid_w, grid_h = 18,10
tile_w, tile_h = win_w//grid_w, win_h//grid_h

grid = np.empty((grid_w,grid_h),dtype=object)
for w in range(grid_w):
    for h in range(grid_h):
        grid[w,h] = []

blocks = []
fighters = []
player = None
n_teams = 2
turn = 1
playing_team = 1
font = pg.font.SysFont(pg.font.get_default_font(),24)
class block(pg.sprite.Sprite):
    name = ''
    x,y = 0,0
    def __init__(self,img_path, x, y, solid = False):
        super().__init__()
        self.x, self.y = x,y
        self.solid = solid
        base_img = pg.image.load('assets/'+img_path)
        self.img = pg.transform.scale(base_img, (tile_w,tile_h))
        self.rect = self.img.get_rect()
        grid[x,y].append(self)
    
class fighter(block):
    can_attack = True
    def __init__(self,img_path,x,y, stats, items,team = 1):
        super().__init__(img_path ,x,y, solid = True)
        self.team, self.items = team, items
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
        grid[self.x,self.y].remove(self)

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

#terrain
blocks += [block('wall.jpg',x=10,y=i,solid = True) for i in range(5) if i != 3]
blocks += [block('wall.jpg',x=i,y=5,solid = True) for i in range(5,11) if i != 8]
blocks.append(directionalDoor('door.png',x=8,y=5,orientation = 'bot'))
blocks.append(directionalDoor('door.png',x=10,y=3,orientation = 'right'))

#place units
cheems = scout('cheems_scout.png', 8,4 ,stats = cheems_stats, items = [pitchfork()])

team1 = [fighter('cheems_batte.png', 4,4 , cheems_stats, [pitchfork()]),
         cheems,
         fighter("dogeatthan.png",5,2, dogeatthan_stats, [comet()])]

team2 = [fighter('choge.jpg',15,2, choge_stats, [bareFist()],team = 2), 
         fighter("dogion.png",13,4, dogion_stats, [maw()], team = 2),
         fighter("dogion.png",17,5, dogion_stats, [maw()], team = 2)]

fighters += team1 + team2
teams = [team1, team2]
blocks += fighters

def check_move_inputs(target):
    if event.key == pg.K_d:
        move(target,target.x+1, target.y)
    
    if event.key == pg.K_q:
        move(target,target.x -1, target.y)
    
    if event.key == pg.K_z:
        move(target,target.x, target.y -1)
    
    if event.key == pg.K_s:
        move(target,target.x, target.y + 1)
        
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
            
def move(target, x,y):
    if x in range(grid_w) and y in range(grid_h) and target.pm > 0 and not has_collision(target, x, y) :
        target.pm -= 1
        grid[target.x,target.y].remove(target)
        
        target.x, target.y = x,y 
        grid[target.x,target.y].append(target)


def dmg_calc(player,target):  
    weapon = player.items[0]    
    if weapon.dmg_type == 'physical':
        return player.atk + weapon.dmg - target.deff
    elif weapon.dmg_type == 'magic':
        return player.mag + weapon.dmg - target.res
def attack(player, target):
        target.hp -= dmg_calc(player,target)
        if target.hp > 0 and in_range(target, player):
            player.hp -= dmg_calc(target,player)
        player.has_attacked()
        print(player.hp, target.hp)

def in_range(player, target):
    return abs(player.x - target.x) + abs(player.y - target.y) in player.items[0].range

            
def select(target):
    return target
#============ drawing stuff =============
def draw_grid():
    for i in range(grid_w):
        pg.draw.line(win,BLACK,(i*tile_w,0),(i*tile_w, win_h))
    for i in range(grid_h):
        pg.draw.line(win, BLACK, (0,i*tile_h),(win_w,i*tile_h))

def draw_movable_squares(movable_squares):
    for s in movable_squares:
        pg.draw.rect(win,(0,0,255),pg.Rect(s.x * tile_w, s.y * tile_h, tile_w - 20,tile_h - 20))
    
def draw_hud(x,y):
    
    #draw the square around the selected fighter
    if player: 
        pg.draw.rect(win,(0,0,255),pg.Rect(player.rect.x, player.rect.y, tile_w,tile_h),3)
    
    #draw turn informations
    win.blit(font.render(f"Team {playing_team} playing",True,BLACK),(win_w - 130, 20))
    win.blit(font.render(f"turn: {turn}",True,BLACK),(win_w - 130, 50))
    
    #draw fighterwin.blit(font.render(f"{fighter.hp} / {fighter.base_hp} hp",True, BLACK),(50, 20)) info bubble
    for b in grid[x,y]:
        if isinstance(b,fighter):
            win.blit(font.render(f"{b.hp} / {b.base_hp} hp",True, BLACK),(50, 20))


def draw_blocks(blocks):
    for block in blocks:
        block.rect.x, block.rect.y = block.x * tile_w, block.y * tile_h
        win.blit(block.img, block.rect)

def is_passable():
    return True
movable_squares = []
i = 0    
fps = 60
clock = pg.time.Clock()
running = True
while running:
    clock.tick(fps)  
    mouse_pos = pg.mouse.get_pos()
    mouse_x, mouse_y = mouse_pos[0] // tile_w, mouse_pos[1] // tile_h
    
    for event in pg.event.get():
        
        #keyboard
        if event.type == pg.QUIT:
            running = False   
        if event.type == pg.KEYDOWN:
            if player:
                check_move_inputs(player)
                
            #skip turn
            if event.key == pg.K_p:
                turn +=1
                playing_team = ((turn+1) % n_teams) + 1
                player = None
                for f in teams[playing_team - 1]:
                    f.pm = f.base_pm
                    f.can_attack = True
                    
        #mouse          
        if event.type == pg.MOUSEBUTTONUP:
            blocks_at_mouse = grid[mouse_x,mouse_y]
            
            #point at fighter 
            fighters_at_mouse = [b for b in blocks_at_mouse if isinstance(b, fighter)]
            if len(fighters_at_mouse) != 0:
                target = fighters_at_mouse[0]  
                movable_squares, _ = find_movable_squares(target, grid)
                
                #select player
                if target.team == playing_team: 
                    player = target        
                #attack enemy with selected player
                if player and target.team != player.team and player.can_attack: 
                    if in_range(player,target):
                        attack(player,target)
                        
            #unselect current player
            else: 
                player = None
                movable_squares = []
    
    #draw window ..
    win.fill(WHITE)
    draw_blocks(blocks)
    draw_movable_squares(movable_squares)
    draw_grid()
    draw_hud(mouse_x,mouse_y)
    pg.display.flip()
    
        
pg.quit()


            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    

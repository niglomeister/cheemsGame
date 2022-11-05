#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 10:44:17 2022

@author: max
"""
import pygame as pg
import os
import numpy as np

from pathfinding import find_path, find_movable_squares
from stats import *
from lib import *

pg.init()  

BLACK = (0,0,0)
win_w, win_h = 900, 500
win = pg.display.set_mode((win_w,win_h))
pg.display.set_caption("cheems battle ultimate")
font = pg.font.SysFont(pg.font.get_default_font(),24)

def check_move_inputs(target):
    if event.key == pg.K_d:
        move(target,target.x+1, target.y)
    
    if event.key == pg.K_q:
        move(target,target.x -1, target.y)
    
    if event.key == pg.K_z:
        move(target,target.x, target.y -1)
    
    if event.key == pg.K_s:
        move(target,target.x, target.y + 1)
        
            
def move(target, x,y):
    if x in range(grid.w) and y in range(grid.h) and target.pm > 0 and not has_collision(target, x, y) :
        target.pm -= 1
        grid[target.x,target.y].remove(target)
        
        target.x, target.y = x,y 
        grid[target.x,target.y].append(target)
    return find_movable_squares(target)


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


#============ drawing stuff =============
def draw_grid():
    for i in range(grid.w):
        pg.draw.line(win,BLACK,(i*grid.tile_w,0),(i*grid.tile_w, win_h))
    for i in range(grid.h):
        pg.draw.line(win, BLACK, (0,i*grid.tile_h),(win_w,i*grid.tile_h))

def draw_movable_squares(movable_squares):
    for s in movable_squares:
        pg.draw.rect(win,(0,0,255),pg.Rect(s.x * grid.tile_w, s.y * grid.tile_h, grid.tile_w - 20,grid.tile_h - 20))
    
def draw_hud(x,y):
    
    #draw the square around the selected fighter
    if player: 
        pg.draw.rect(win,(0,0,255),pg.Rect(player.rect.x, player.rect.y, grid.tile_w,grid.tile_h),3)
    
    #draw turn informations
    win.blit(font.render(f"Team {playing_team} playing",True,BLACK),(win_w - 130, 20))
    win.blit(font.render(f"turn: {turn}",True,BLACK),(win_w - 130, 50))
    
    for b in grid[x,y]:
        if isinstance(b,fighter):
            win.blit(font.render(f"{b.hp} / {b.base_hp} hp",True, BLACK),(50, 20))


def draw_blocks(blocks):
    for block in blocks:
        block.rect.x, block.rect.y = block.x * grid.tile_w, block.y * grid.tile_h
        win.blit(block.img, block.rect)

def is_passable():
    return True
movable_squares = []
i = 0    
fps = 60
clock = pg.time.Clock()
running = True

""" ============ LEVEL =========== """
grid_w, grid_h = 18, 10
#terrain setup
blocks += [block('wall.jpg',x=10,y=i, solid = True) for i in range(5) if i != 3]
blocks += [block('wall.jpg',x=i,y=5, solid = True) for i in range(5,11) if i != 8]
blocks.append(directionalDoor('door.png',x=8,y=5, orientation = 'bot'))
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

grid = Grid(grid_w, grid_h,win_w,win_h )

while running:
    clock.tick(fps)  
    mouse_pos = pg.mouse.get_pos()
    mouse_x, mouse_y = mouse_pos[0] // grid.tile_w, mouse_pos[1] // grid.tile_h
    
    for event in pg.event.get():
        
        #keyboard
        if event.type == pg.QUIT:
            running = False   
        if event.type == pg.KEYDOWN:
            
            #skip turn
            if event.key == pg.K_p:
                print(playing_team)
                turn +=1
                playing_team = ((turn+1) % n_teams) + 1
                player = None
                for f in teams[playing_team - 1]:
                    f.pm = f.base_pm
                    f.can_attack = True
                    
            #check move inputs
            if player:
                if event.key == pg.K_d:
                    movable_squares = move(player,player.x+1, player.y)
                if event.key == pg.K_q:
                    movable_squares = move(player,player.x -1, player.y)      
                if event.key == pg.K_z:
                    movable_squares = move(player,player.x, player.y -1)
                if event.key == pg.K_s:
                    movable_squares = move(player,player.x, player.y + 1)
                    
        #mouse          
        if event.type == pg.MOUSEBUTTONUP:
            blocks_at_mouse = grid[mouse_x,mouse_y]
            
            #point at fighter 
            fighters_at_mouse = [b for b in blocks_at_mouse if isinstance(b, fighter)]
            if len(fighters_at_mouse) != 0:
                target = fighters_at_mouse[0]  
                
                #select player
                if target.team == playing_team: 
                    player = target   
                    
                #attack enemy with selected player
                if player and target.team != player.team and player.can_attack: 
                    if in_range(player,target):
                        attack(player,target)
                else:   
                    movable_squares = find_movable_squares(target)
                        
            #unselect current player
            else: 
                player = None
                movable_squares = []
    
    #draw window ..
    win.fill((255,255,255))
    draw_blocks(blocks)
    draw_movable_squares(movable_squares)
    draw_grid()
    draw_hud(mouse_x,mouse_y)
    pg.display.flip()
    
        
pg.quit()


            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    

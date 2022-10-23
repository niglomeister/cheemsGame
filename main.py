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

win = pg.display.set_mode((win_w,win_h))
pg.display.set_caption(game_name)
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
            
def move(target, x,y, grid):
    if x in range(grid_w) and y in range(grid_h) and target.pm > 0 and not has_collision(target, x, y) :
        target.pm -= 1
        grid[target.x,target.y].remove(target)
        
        target.x, target.y = x,y 
        grid[target.x,target.y].append(target)
    return find_movable_squares(target, grid)


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
                    movable_squares = move(player,player.x+1, player.y, grid)
                if event.key == pg.K_q:
                    movable_squares = move(player,player.x -1, player.y, grid)      
                if event.key == pg.K_z:
                    movable_squares = move(player,player.x, player.y -1, grid)
                if event.key == pg.K_s:
                    movable_squares = move(player,player.x, player.y + 1, grid)
                    
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
                    movable_squares = find_movable_squares(target, grid)
                        
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


            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    

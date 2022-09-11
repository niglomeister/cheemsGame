#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 23:35:45 2022

@author: max
"""

def move(target):
    if target.pm > 0:
        x,y = target.x, target.y
        if event.key == pg.K_d and collision_grid[x+1,y] == 0:
            target.x += 1
            target.pm -= 1
        elif event.key == pg.K_q and collision_grid[x-1,y] == 0:
            target.x -= 1
            target.pm -=1
        elif event.key == pg.K_z and collision_grid[x,y-1] == 0:
            target.y -= 1
            target.pm -= 1
        elif event.key == pg.K_s and collision_grid[x,y+1] == 0:
            target.y += 1
            target.pm -= 1
        print(collision_grid)
        collision_grid[x,y] -= 1
        collision_grid[target.x, target.y] += 1
        
        
"""
def is_collision(x,y):
    collision_targets = [b for b in blocks if b.rect.collidepoint(x*tile_w , y*tile_h ) and b.solid == True]
    if collision_targets:
        return True
    else:
        return True
"""
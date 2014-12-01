from __future__ import division
import pygame, sys
import math
from pygame.locals import * 
#Remember to make this code cleaner than fighters.py
#Frigates are actually pretty small, only 128x128 so I need to make a corvette class or something
#Also make frigate 1 wider cause it looks like a pencil
#TODO: rotation bs

def get_alpha_hitmask(image, rect, alpha=0):
    mask=[]
    for x in range(rect.width):
        mask.append([])
        for y in range(rect.height):
            mask[x].append(not image.get_at((x,y))[3]==alpha)
    return mask

class Frigate:
	def __init__(self, ship_type, thruster):
		self.ship_type = ship_type
		self.thruster = thruster
		self.ship = pygame.image.load('img/frigate_' + self.ship_type + '.png')
		self.ship = pygame.Surface.convert_alpha(self.ship)
		self.ship_final = self.ship.copy()
		self.thruster = pygame.image.load('img/fr_thrust_' + self.thruster + '.png')
		self.thruster = pygame.Surface.convert_alpha(self.thruster)
		self.thruster_final = self.thruster
		self.ship_destroyed = pygame.image.load('img/frigate_' + self.ship_type + '_destroyed.png')
		self.ship_destroyed = pygame.Surface.convert_alpha(self.ship_destroyed)
		self.rect = self.ship.get_rect()
		self.hp = 10
		self.x = 1
		self.y = 1
		self.x_const = 1
		self.y_const = 1
		self.rect[0] = 1
		self.rect[1] = 1
		
		self.rotation = 0
		self.hitmask = get_alpha_hitmask(self.ship_final, self.rect, 0)
		self.counter = 0
		self.speed = 1

	def rotate(self):
		self.ship_final = pygame.transform.rotate(self.ship, self.rotation)
		self.thruster_final = pygame.transform.rotate(self.thruster, self.rotation)
		self.rect = self.ship_final.get_rect(center=self.rect.center)
		
		

	def move_calc(self):
		#Rect cannot have a decimal as its position.
		rads = math.radians(self.rotation)
		self.y = (-math.sin(rads) * self.speed) + self.y
		self.x = (math.cos(rads) * self.speed) + self.x
		
		final = [self.x, self.y]
		return final

	def update_ship(self, display_surf):
		self.rect.center = [self.x, self.y]
		self.rotate()
		self.move_calc()
		print(self.rect)
		display_surf.blit(self.ship_final, (self.rect))
		display_surf.blit(self.thruster_final, (self.rect[0], self.rect[1]))
		self.hitmask = get_alpha_hitmask(self.ship_final, self.rect, 0)
		self.speed = 0
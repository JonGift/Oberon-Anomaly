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
	def __init__(self, ship_type, thruster, display_surf):
		self.name = ('Temp Frigate Name')
		self.ship_type = ship_type
		self.thruster = thruster
		self.display_surf = display_surf
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
		self.is_selected = False
		self.rect[1] = 1
		self.moved_by_player = False
		self.target = None
		self.team = 2
		self.target_loc_personal = None
		#help I don't understand
		
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

	def target_enemy(self, target):
		#This whole thing really needs some comments
		x_difference = (target.x) - (self.x)
		y_difference = (target.y) - (self.y)
		
		def pythag_absolute(numb):
			new_numb = 0
			if numb > 0:
				new_numb = 1
			elif numb < 0:
				new_numb = -1
				
			final_numb = abs(numb * numb) # * new_numb
			
			return final_numb
		
		x = pythag_absolute(x_difference)
		y = pythag_absolute(y_difference)
		hyp = (x + y)
		hyp = math.sqrt(hyp)
		radian_calc = 360
		
		for x in range(radian_calc):
			rads = math.radians(x+1)
			f_point_bs = round((math.cos(rads)), 1)
			f_point_bs_diff = round((x_difference / hyp), 1)
			f_point_bs2 = round((math.sin(rads)), 1)
			f_point_bs2_diff = round((-y_difference / hyp), 1)
			if f_point_bs == f_point_bs_diff:
				if f_point_bs2 == f_point_bs2_diff:
					if x+1 != self.rotation:
						change = 0
						difference = self.rotation - (x+1)
						about_x1 = x+3
						about_x2 = x-3
						if difference  == 1:
							change = 0
						elif difference == -1:
							change = 0
						elif difference > 1:
							change = -1
						else:
							change = 1
							
						if(abs(difference) > 180):
							change = 0 - change
						if self.target is not None:
							if(self.rotation < about_x1):
								if(self.rotation > about_x2):
									#if hyp <= self.range:
									#	self.is_shooting = True
									print('oh baby a triple')
						
						self.rotation += change
						return
			

	def update_ship(self):
		if self.rotation < 0:
			self.rotation = 360 + self.rotation
		if self.rotation > 360:
			self.rotation = self.rotation - 360
		self.rect.center = [self.x, self.y]
		if self.target != None:
			pass
		self.rotate()
		self.move_calc()
		self.display_surf.blit(self.ship_final, (self.rect))
		self.display_surf.blit(self.thruster_final, (self.rect[0], self.rect[1]))
		self.hitmask = get_alpha_hitmask(self.ship_final, self.rect, 0)
		self.speed = 0
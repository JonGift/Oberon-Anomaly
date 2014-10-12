import pygame, sys
from pygame.locals import * 

class stars:
	def __init__(self, color = 'yellow'):
		self.color = color
		self.stars = pygame.image.load('star_' + self.color + '.png')
		self.starfield = pygame.image.load('star_field_' + self.color + '.png')
		self.move_x = 10
		self.move_y = 10
	def moving_starfield(self, display_surf, speed):
		if self.move_x <= -1500:
			self.move_x = speed
		
	
		self.move_x -= speed
		display_surf.blit(self.starfield, (self.move_x, self.move_y))
		display_surf.blit(self.starfield, (self.move_x+1500, self.move_y))
import pygame, sys
from pygame.locals import * 

class stars:
	def __init__(self, color = 'yellow'):
		self.color = color
		self.starfield = pygame.image.load('img/star_field_' + self.color + '.png')
		self.x = 10
		self.y = 10
	def moving_starfield(self, display_surf, speed):
		if self.x <= -1500:
			self.x = speed
		
	
		self.x -= speed
		display_surf.blit(self.starfield, (self.x, self.y))
		display_surf.blit(self.starfield, (self.x+1500, self.y))
		
class Title:
	def __init__(self):
		self.counter = 0
		self.title1 = pygame.image.load('img/title_1.png')
		self.title2 = pygame.image.load('img/title_2.png')
		self.title3 = pygame.image.load('img/title_3.png')
		
	def title_begin(self, display_surf):
		if self.counter == 0:
			display_surf.blit(self.title1, (0,0))
		if self.counter == 100:
			display_surf.blit(self.title2, (0,0))
		if self.counter == 200:
			self.counter = -100
			display_surf.blit(self.title3, (0,0))
		else:
			self.counter += 1
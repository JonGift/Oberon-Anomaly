import pygame, sys
from pygame.locals import * 

class fighter:
	def __init__(self, faction = 'No faction', ship_type = '1', bullet_type = '1', speed = 10):
		self.faction = faction
		self.ship_type = ship_type
		self.bullet_type = bullet_type
		self.ship = pygame.image.load('fighter_' + self.ship_type + '.png')
		self.ship_bullet = pygame.image.load('bullet_' + self.bullet_type + '.png')
		self.acceleration = 0
		self.min_acceleration = 0
		self.speed = speed
		self.move_x = 1
		self.move_y = 1
		self.bullet_x = 0
		self.bullet_y = 0
		self.accelerating = False
		self.current_bullet = None
	
	def update_ship(self, display_surf):
		display_surf.blit(self.ship, (self.move_x, self.move_y))
		self.shoot(display_surf)
		
	def shoot(self, display_surf):
		def make_bullet():
			self.current_bullet = Bullet({"x":self.move_x+2, "y":self.move_y+6}, 'right')
			
		if not self.current_bullet:
			make_bullet()
		if self.current_bullet.delete_me == False:
			self.current_bullet.display(display_surf)
		else:
			make_bullet()
		
		

class Bullet:
	def __init__(self, position, direction):
		self.__dict__.update(locals())
		self.ship_bullet = pygame.image.load('bullet_1.png')
		self.distance = 0
		self.delete_me = False
		
	def display(self, display_surf):
		if self.distance > 1000:
			self.delete_me = True
			return
		self.distance += 2
		self.position["x"] += 2
		display_surf.blit(self.ship_bullet, (self.position["x"], self.position["y"]))
import pygame, sys
import math
from pygame.locals import * 

#Fun fact: the following code is as readable as the mindfuck language written in pig latin.

def rotate_checker(commander, ship):
	c_x = round(commander.x, 0)
	c_y = round(commander.y, 0)
	s_x = round(ship.x, 0)
	s_y = round(ship.y, 0)
	x = False
	y = False
	r = False
	if ship.formation == False:
		if s_x > c_x:
			ship.x -= 1
		elif s_x < c_x:
			ship.x += 1
		else:
			x = True
	if ship.formation == False:
		if s_y > c_y:
			ship.y -= 1
		elif s_y < c_y:
			ship.y += 1
		else:
			y = True
	if ship.formation == False:
		if ship.rotate > commander.rotate:
			ship.rotate -= 1
		else:
			ship.rotate += 1
		if ship.rotate == commander.rotate:
			r = True
	else:
		return True
	if x == True:
		if y == True:
			if r == True:
				return True
	return False
	
def squadron(display_surf, commander, *args):
	temp = (args)
	squad = list(temp)
	altitude = 20
	counter = 0
	for i in range(len(squad)):
		if rotate_checker(commander, squad[i]) != True:
			return False
		if counter == 0:
			squad[i].y = commander.y - altitude
			squad[i].x = commander.x - altitude
			squad[i].rotate = commander.rotate
			counter = 1
		elif counter == 1:
			squad[i].y = commander.y + altitude
			squad[i].x = commander.x - altitude
			squad[i].rotate = commander.rotate
			counter = 0
			altitude = altitude * 2
		if commander.speed == 1:
			squad[i].thrust_override = True
		else:
			squad[i].thrust_override = False
		if commander.is_shooting == True:
			squad[i].is_shooting = True
		squad[i].formation = True
	return True

class fighter:
	def __init__(self, ship_type = '1', thruster = '1', max_acc = 0, proj_speed = 5):
		self.ship_type = ship_type
		self.thruster = thruster
		self.ship = pygame.image.load('img/fighter_' + self.ship_type + '.png')
		self.thruster = pygame.image.load('img/f_thrust_' + self.thruster + '.png')
		self.speed = 0
		self.x = 0
		self.y = 0
		self.x2 = 0
		self.y2 = 0
		self.stat_rotate = 0
		self.current_bullet = None
		self.is_shooting = False
		self.rotate = 0
		self.ship_final = self.ship
		self.thrust_final = self.thruster
		self.counter = 0
		self.counter2 = 0
		self.acceleration = 0
		self.max_acc = max_acc
		self.proj_speed = proj_speed
		self.formation = False
		self.thrust_override = False
		self.rect = self.ship.get_rect()
		
	
	def update_ship(self, display_surf):
		#Needs to rotate on center
		if self.rotate < 0:
			self.rotate = 360 + self.rotate
		if self.rotate > 360:
			self.rotate = self.rotate - 360
		
		self.ship_final = pygame.transform.rotate(self.ship, self.rotate)
		self.thrust_final = pygame.transform.rotate(self.thruster, self.rotate)
		display_surf.blit(self.ship_final, (self.move_calc(self.rotate, self.speed+self.acceleration)))
		self.rect[0] = self.x
		self.rect[1] = self.y
		if self.speed == 1:
			display_surf.blit(self.thrust_final, (self.move_calc(self.rotate, self.speed+self.acceleration)))
			if self.acceleration < self.max_acc:
				if self.counter2 < 10:
					self.counter2 +=1
				else:
					self.counter2 = 0
					self.acceleration += 1
		else:
			self.acceleration = 0
		if self.is_shooting == True:
			self.shoot(display_surf)
		if self.thrust_override == True:
			display_surf.blit(self.thrust_final, (self.x, self.y))
	def move_calc(self, rotation, speed):
		rads = math.radians(rotation)
		self.y = -math.sin(rads) * speed + self.y
		self.x = math.cos(rads) * speed + self.x
		final = [self.x, self.y]
		return final
		
	def move_calc_bullet(self, rotation, speed):
		rads = math.radians(rotation)
		self.y2 = -math.sin(rads) * speed + self.y
		self.x2 = math.cos(rads) * speed + self.x
		self.stat_rotate = rads
		final = [self.x2+5, self.y2+5]
		return final
		
	def move_calc_bullet_stat(self, rotation, speed):
		rads = rotation
		self.y2 = -math.sin(rads) * speed + self.y2
		self.x2 = math.cos(rads) * speed + self.x2
		final = [self.x2+5, self.y2+5]
		return final
		
	def shoot(self, display_surf):
		def make_bullet():
			self.current_bullet = Bullet(2)
			
		if not self.current_bullet:
			make_bullet()
		if self.current_bullet.delete_me == False:
			if (self.counter == 0):
				self.current_bullet.display(display_surf, self.move_calc_bullet(self.rotate, self.proj_speed))
				self.counter += 1
			else:
				self.current_bullet.display(display_surf, self.move_calc_bullet_stat(self.stat_rotate, self.proj_speed))
		else:
			self.current_bullet = None
			self.is_shooting = False
			self.counter = 0
		
class Bullet:
	def __init__(self, damage = 1):
		self.__dict__.update(locals())
		self.ship_bullet = pygame.image.load('img/bullet_1.png')
		self.distance = 0
		self.delete_me = False
		self.bullet_final = self.ship_bullet
		self.velocity = 4
		self.damage = damage
		self.rect = self.ship_bullet.get_rect()
		
	def display(self, display_surf, *args):
		counter = 0
		temp = (args)
		coords = list(temp)
		if self.distance > 300:
			self.delete_me = True
			return
		self.distance += 5
		display_surf.blit(self.bullet_final, (args))
		for i in range(len(coords)):
			if counter == 0:
				counter += 1
				self.x = coords[i]
			else:
				self.y = coords[i]
				
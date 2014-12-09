from __future__ import division
import pygame, sys
import math
import random
from pygame.locals import * 
#Add dogfight code. Improve ai. Improve speed and friction.
#Fun fact: the following code is as readable as the mindfuck language written in pig latin.

def get_alpha_hitmask(image, rect, alpha=0):
    mask=[]
    for x in range(rect.width):
        mask.append([])
        for y in range(rect.height):
            mask[x].append(not image.get_at((x,y))[3]==alpha)
    return mask

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
	if commander.hp > 0:
		for i in range(len(squad)):
			if squad[i].hp > 0:
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
				if commander.speed > 0:
					squad[i].thrust_override = True
				else:
					squad[i].thrust_override = False
				if commander.is_shooting == True:
					squad[i].is_shooting = True
				squad[i].formation = True
			else:
				squad[i].formation = False
	else:
		for i in range(len(squad)):
			squad[i].formation = False
		return False
	return True

class fighter:
	def __init__(self, ship_type = '1', thruster = '1', max_acc = 0, proj_speed = 3, team = 0):
		self.name = ('Temp Fighter Name')
		self.ship_type = ship_type
		self.type_name = 'Fighter'
		self.thruster = thruster
		self.team = team
		self.ship = pygame.image.load('img/fighter_' + self.ship_type + '.png')
		self.thruster = pygame.image.load('img/f_thrust_' + self.thruster + '.png')
		self.ship_destroyed = pygame.image.load('img/fighter_' + self.ship_type + '_destroyed.png')
		self.speed = 0
		self.hp = 5
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
		self.counter3 = 0
		self.acceleration = 0
		self.max_acc = max_acc
		self.proj_speed = proj_speed
		self.formation = False
		self.thrust_override = False
		self.rect = self.ship.get_rect()
		self.ship = pygame.Surface.convert_alpha(self.ship)
		self.hitmask = pygame.mask.from_surface(self.ship)
		self.blank = 0
		self.target = None
		self.range = 300
		self.is_selected = False
		self.moved_by_player = False
		self.hitmask = get_alpha_hitmask(self.ship,self.rect)
		self.rotate_static = 0
		self.static_rotate_counter = 0
		self.rotate_random = random.randint(-10,10)
		self.target_loc_personal = None
		
	
	def update_ship(self, display_surf):
		self.rect[0] = self.x
		self.rect[1] = self.y
		if self.hp > 0:
			if self.rotate < 0:
				self.rotate = 360 + self.rotate
			if self.rotate > 360:
				self.rotate = self.rotate - 360
			if self.target is not None:
				if self.moved_by_player == False:
					self.target = self.target
					self.target_enemy(self.target)
					if self.target.speed == 0:
						self.speed = .2
					else:
						self.speed = 1
					if self.target.target is not None:
						if self.target.target == self:
							#TODO: Dogfight anybody?
							pass
					if self.target.hp < 1:
						self.target = None
						self.speed = 0
			else:
				self.target = None
				
			self.ship_final = pygame.transform.rotate(self.ship, self.rotate)
			self.thrust_final = pygame.transform.rotate(self.thruster, self.rotate)
			display_surf.blit(self.ship_final, (self.move_calc(self.rotate, self.speed+self.acceleration)))
			if self.speed > 0:
				display_surf.blit(self.thrust_final, (self.move_calc(self.rotate, self.speed+(self.acceleration*self.speed))))
				if self.acceleration < self.max_acc:
					if self.counter2 < 20:
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
		else:
			if self.static_rotate_counter == 0:
				self.rotate_static = self.rotate
				self.static_rotate_counter += 1
			self.ship_destroyed_final = pygame.transform.rotate(self.ship_destroyed, self.rotate)
			self.speed = 1
			self.rotate += (self.rotate_random)*.1
			display_surf.blit(self.ship_destroyed_final, (self.move_calc(self.rotate_static, self.speed)))
			self.current_bullet = None
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
				self.current_bullet.rect[0] = self.x2+5
				self.current_bullet.rect[1] = self.y2+5
			else:
				self.current_bullet.display(display_surf, self.move_calc_bullet_stat(self.stat_rotate, self.proj_speed))
				self.current_bullet.rect[0] = self.x2+5
				self.current_bullet.rect[1] = self.y2+5
		else:
			self.current_bullet = None
			self.is_shooting = False
			self.counter = 0
		
		
	def target_enemy(self, target):
		
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
					if x+1 != self.rotate:
						change = 0
						difference = self.rotate - (x+1)
						about_x1 = x+3
						about_x2 = x-3
						if difference  <= 5 and difference >= -5:
							change = 0
						elif difference > 5:
							change = -5
						else:
							change = 5
							
						if(abs(difference) > 180):
							change = 0 - change
						if self.target is not None:
							if(self.rotate < about_x1):
								if(self.rotate > about_x2):
									if hyp <= self.range:
										self.is_shooting = True
						
						
						self.rotate += change
						return
			
		
		
		
class Bullet:
	def __init__(self, damage = 1):
		self.name = 'bullet'
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
				
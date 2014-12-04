from __future__ import division
from copy import deepcopy
import pygame, sys
from pygame.locals import * 
import ship_generation
import graphical_effects
import fighters
import frigates

#Use pixel perfect collision

FPS = 30
fpsClock = pygame.time.Clock()

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Oberon Anomaly')
starfield = pygame.image.load('img/star_field_galaxy.png')

def PixelPerfectCollision(obj1, obj2):
    try:rect1, rect2, hm1, hm2 = obj1.rect, obj2.rect, obj1.hitmask, obj2.hitmask
    except AttributeError:return False
    rect=rect1.clip(rect2)
    if rect.width==0 or rect.height==0:
        return False
    x1,y1,x2,y2 = rect.x-rect1.x,rect.y-rect1.y,rect.x-rect2.x,rect.y-rect2.y
    for x in range(rect.width):
        for y in range(rect.height):
            if hm1[x1+x][y1+y] and hm2[x2+x][y2+y]:return True
            else:continue
    return False

def collision_detection_fighters(*args):
	temp_entities = (args)
	entities = list(temp_entities)
	for x in range(len(entities)):
		if entities[x].current_bullet is not None:
			test = entities[x].current_bullet.rect.collidelist(entities)
			if test != -1:
				if entities[test].team == entities[x].team:
					pass
				else:
					entities[test].hp -= entities[x].current_bullet.damage
						
		


def move_camera(list):
	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_LEFT]:
		for i in range(len(list)):
			list[i].x += 3
	if keys[pygame.K_RIGHT]:
		for i in range(len(list)):
			list[i].x -= 3
	if keys[pygame.K_UP]:
		for i in range(len(list)):
			list[i].y += 3
	if keys[pygame.K_DOWN]:
		for i in range(len(list)):
			list[i].y -= 3

class point_location():
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
			
def select(var, target_loc, target_list):
	if var.hp > 0:
		if pygame.mouse.get_pressed()[0]:
			if var.rect.collidepoint(pygame.mouse.get_pos()) == True:
				if var.is_selected != True:
					var.is_selected = True
			else:
				for x in range(len(target_list)):
					if target_list[x].rect.collidepoint(pygame.mouse.get_pos()):
						var.is_selected = True
				else:
					var.is_selected = False
		#if pygame.mouse.get_pressed()[2]:
		if pygame.mouse.get_pressed()[2]:
			if var.is_selected == True:
				for x in range(len(target_list)):
					if target_list[x].rect.collidepoint(pygame.mouse.get_pos()):
						if target_list[x].team != var.team:
							if target_list[x].hp > 0:
								var.target = target_list[x]
								var.moved_by_player = False
								break
				else:
					var.target = None
					var.moved_by_player = True
					target_loc.x = pygame.mouse.get_pos()[0]
					target_loc.y = pygame.mouse.get_pos()[1]
		if var.moved_by_player == True:			
			var.speed = 1
			if var.is_selected == True:
				var.target_loc_personal = deepcopy(target_loc)
				var.target_enemy(var.target_loc_personal)
			else:
				var.target_enemy(var.target_loc_personal)
			if abs(var.x - target_loc.x) < 10:
				if abs(var.y - target_loc.y) < 10:
					var.moved_by_player = False
					var.target_loc_personal = None
					var.speed = 0


test = graphical_effects.stars()
pointer = point_location()
fighter_test = fighters.fighter('2', '1', 1, 5, 1)
fighter1 = fighters.fighter('2', '1', 1, 5, 1)
fighter2 = fighters.fighter('2', '1', 1, 5, 1)
fighter3 = fighters.fighter('1', '1', 1, 5, 0)
fighter4 = fighters.fighter('1', '1', 1, 5, 0)

frigate_test = frigates.Frigate('2','2', DISPLAYSURF)

fighter_list = []
fighter_list.append(fighter1)
fighter_list.append(fighter2)
fighter_list.append(fighter3)
fighter_list.append(fighter4)
temp_list = [fighter_test, fighter1, fighter2, fighter3, fighter4, frigate_test]

while True:
	print('Frigate: ' + str(frigate_test.is_selected) + ' Fighter: ' + str(fighter_test.is_selected))
	print(frigate_test.target_loc_personal, fighter_test.target_loc_personal)
	keys_pressed = pygame.key.get_pressed()
	fighter_test.speed = 0
	if keys_pressed[pygame.K_e]:
		fighter4.target = fighter_test
	select(frigate_test, pointer, fighter_list)
	select(fighter_test, pointer, fighter_list)
	fighters.squadron(DISPLAYSURF, fighter_test, fighter1, fighter2)
	fighters.squadron(DISPLAYSURF, fighter4, fighter3)

	if keys_pressed[pygame.K_SPACE]:
		fighter_test.is_shooting = True
		
	collision_detection_fighters(fighter_test, fighter1, fighter2, fighter3, fighter4)
	
	DISPLAYSURF.blit(starfield, (0,0))
	frigate_test.update_ship()
	fighter_test.update_ship(DISPLAYSURF)
	fighter1.update_ship(DISPLAYSURF)
	fighter2.update_ship(DISPLAYSURF)
	fighter3.update_ship(DISPLAYSURF)
	fighter4.update_ship(DISPLAYSURF)
	
	PixelPerfectCollision(frigate_test, fighter_test)
	move_camera(temp_list)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
	fpsClock.tick(FPS)	
import pygame, sys
from pygame.locals import * 
import ship_generation
import graphical_effects
import fighters
#TODO: Update collision on bullets. It currently starts and never updates.


FPS = 59
fpsClock = pygame.time.Clock()

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Oberon Anomaly')
starfield = pygame.image.load('img/star_field_galaxy.png')

def collision_detection(*args):
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

test = graphical_effects.stars()
fighter_test = fighters.fighter('2', '1', 5, 4, 1)
fighter1 = fighters.fighter('1', '1', 5, 4, 1)
fighter2 = fighters.fighter('2', '1', 5, 4, 1)
fighter3 = fighters.fighter('1', '1', 5, 4, 1)
fighter4 = fighters.fighter('1', '1', 5, 15, 0)


while True:
	keys_pressed = pygame.key.get_pressed()
	fighter_test.speed = 0
	if keys_pressed[pygame.K_a]:
		fighter_test.rotate += 2
	if keys_pressed[pygame.K_d]:
		fighter_test.rotate -= 2
	if keys_pressed[pygame.K_w]:
		fighter_test.speed = 1.0
	if keys_pressed[pygame.K_s]:
		fighter_test.speed = -1.0
	if keys_pressed[pygame.K_e]:
		fighter4.target = fighter_test

	fighters.squadron(DISPLAYSURF, fighter_test, fighter1, fighter2, fighter3)
	
		

	if keys_pressed[pygame.K_SPACE]:
		fighter_test.is_shooting = True
		
	collision_detection(fighter_test, fighter1, fighter2, fighter3, fighter4)
	
	DISPLAYSURF.blit(starfield, (0,0))
	fighter_test.update_ship(DISPLAYSURF)
	fighter1.update_ship(DISPLAYSURF)
	fighter2.update_ship(DISPLAYSURF)
	fighter3.update_ship(DISPLAYSURF)
	fighter4.update_ship(DISPLAYSURF)
	temp_list = [fighter_test, fighter1, fighter2, fighter3, fighter4]
	move_camera(temp_list)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
	fpsClock.tick(FPS)	
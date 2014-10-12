import pygame, sys
from pygame.locals import * 
import ship_generation
import graphical_effects
import fighters

FPS = 59
fpsClock = pygame.time.Clock()

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Oberon Anomaly')

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
test = graphical_effects.stars()
fighter_test = fighters.fighter()

while True:
	DISPLAYSURF.fill(GREEN)
	test.moving_starfield(DISPLAYSURF, 2)
	fighter_test.update_ship(DISPLAYSURF)
	fighter_test.move_x += 1
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
	fpsClock.tick(FPS)	
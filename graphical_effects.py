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

class title:
    def __init__(self):
        self.y = 800
        self.counter = 0
        self.title1 = pygame.image.load('img/title_screen.png')
        self.title2 = pygame.image.load('img/star_field_galaxy.png')
        self.new_game = pygame.image.load('img/new_game.png')
        self.load_game = pygame.image.load('img/load_game.png')
        self.options = pygame.image.load('img/options.png')
        self.new_game_rect = self.new_game.get_rect()
        self.load_game_rect = self.load_game.get_rect()
        self.options_rect = self.options.get_rect()
        self.new_game_rect[0] = 384
        self.load_game_rect[0] = 384
        self.options_rect[0] = 384

    def update(self, display_surf):
        self.new_game_rect[1] = self.y
        self.load_game_rect[1] = self.y + 116
        self.options_rect[1] = self.y + 232
        if self.counter < 200:
            self.counter += 1
        if self.counter >= 0:
            display_surf.blit(self.title2, (0, 0))
        if self.counter >= 50:
            display_surf.blit(self.title1, (0,0))
        if self.counter >= 100:
            if self.y > 200:
                self.y -= 4
            display_surf.blit(self.new_game, (self.new_game_rect))
            display_surf.blit(self.load_game, (self.load_game_rect))
            display_surf.blit(self.options, (self.options_rect))
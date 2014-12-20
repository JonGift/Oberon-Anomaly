from __future__ import division
from copy import deepcopy
import pygame
import sys
from pygame.locals import * 
import graphical_effects
import fighters
import frigates
import ai
import random
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

def fighter_pixel_perfect(fighter, target):
    if fighter.current_bullet is not None:
        if fighter.target is not None:
            if fighter.target.type_reference != 'Fighter' and fighter.target.type_reference != 'Bomber':
                if PixelPerfectCollision(fighter.current_bullet, target) == True:
                    target.hp -= (fighter.current_bullet.damage / target.armor)
                    fighter.bullet_cooldown += fighter.current_bullet.distance / 2
                    fighter.current_bullet.delete_me = True

def collision_detection_fighters(list_of_fighters):
    temp_entities = list_of_fighters
    entities = list(temp_entities)
    for x in range(len(entities)):
        if entities[x].current_bullet is not None:
            test = entities[x].current_bullet.rect.collidelist(entities)
            if test != -1:
                if entities[test].team == entities[x].team:
                    pass
                else:
                    if entities[test].hp > entities[test].delete_hp:
                        entities[test].hp -= (entities[x].current_bullet.damage / entities[test].armor)
                        entities[x].bullet_cooldown += entities[x].current_bullet.distance / 2
                        entities[x].current_bullet.delete_me = True




def auto_squadron(ship):
    temp1 = 0
    temp2 = 0
    commander = None
    for x in range(len(fighter_list)):
        if fighter_list[x].team == ship.team:
            if fighter_list[x].is_commanding is not False:
                too_large = False
                for i in range(len(fighter_list[x].fighter_list)):
                    if i > 2:
                        too_large = True
                if too_large == False:
                    commander = fighter_list[x]

    if commander == None:
        ship.is_commanding = True
        return

    for x in range(len(fighter_list)):
        if fighter_list[x] == commander:
            temp1 = x
        if fighter_list[x] == ship:
            temp2 = x

    fighter_list[temp1].fighter_list.append(fighter_list[temp2])

def move_camera(list):	
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        for i in range(len(list)):
            if list[i].target_loc_personal != None:
                list[i].target_loc_personal.x += 12
            if list[i].current_bullet != None:
                list[i].x2 += 12
            list[i].x += 12
    if keys[pygame.K_RIGHT]:
        for i in range(len(list)):
            if list[i].target_loc_personal != None:
                list[i].target_loc_personal.x -= 12
            if list[i].current_bullet != None:
                list[i].x2 -= 12
            list[i].x -= 12
    if keys[pygame.K_UP]:
        for i in range(len(list)):
            if list[i].target_loc_personal != None:
                list[i].target_loc_personal.y += 12
            if list[i].current_bullet != None:
                list[i].y2 += 12
            list[i].y += 12
    if keys[pygame.K_DOWN]:
        for i in range(len(list)):
            if list[i].target_loc_personal != None:
                list[i].target_loc_personal.y -= 12
            if list[i].current_bullet != None:
                list[i].y2 -= 12
            list[i].y -= 12

class point_location():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.current_bullet = None
        self.target_loc_personal = None

def select(var, target_loc, target_list):
    key = pygame.key.get_pressed()
    if var.hp > 0:
        if pygame.mouse.get_pressed()[0] or key[pygame.K_j]:
            if var.rect.collidepoint(pygame.mouse.get_pos()) == True:
                var.is_selected = True
            else:
                for x in range(len(target_list)):
                    if target_list[x].rect.collidepoint(pygame.mouse.get_pos()) and var.is_selected == True:
                        var.is_selected = True
                        break
                else:
                    var.is_selected = False
        if pygame.mouse.get_pressed()[2] or key[pygame.K_k]:
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
                    var.target_loc_personal = deepcopy(target_loc)
        if var.moved_by_player == True:
            var.speed = 1
            if var.is_selected == True:
                var.target_enemy(var.target_loc_personal)
            else:
                var.target_enemy(var.target_loc_personal)
            if abs(var.x - target_loc.x) < 20:
                if abs(var.y - target_loc.y) < 20:
                    var.moved_by_player = False
                    var.target_loc_personal = None
                    var.speed = 0


title_screen = graphical_effects.title()
pointer = point_location()
x_y = point_location()
fighter_dict = {}
fighter_test = fighters.fighter('1', '1', 2, 10, 1, 'fighter_test', 'fighter_test')
fighter1 = fighters.fighter('1', '1', 2, 10, 1, 'fighter1', 'fighter1')
fighter2 = fighters.fighter('1', '1', 2, 10, 1, 'fighter2', 'fighter2')
fighter3 = fighters.fighter('2', '2', 2, 10, 2, 'fighter3', 'fighter3')
fighter4 = fighters.fighter('2', '2', 2, 10, 2, 'fighter4', 'fighter4')
fighter5 = fighters.fighter('2', '2', 2, 10, 2, 'fighter5', 'fighter5')
fighter6 = fighters.fighter('3', '3', 2, 10, 3, 'fighter6', 'fighter6')
fighter7 = fighters.fighter('3', '3', 2, 10, 3, 'fighter7', 'fighter7')
fighter8 = fighters.fighter('3', '3', 2, 10, 3, 'fighter8', 'fighter8')
fighter9 = fighters.fighter('4', '4', 2, 10, 4, 'fighter9', 'fighter9')
fighter10 = fighters.fighter('4', '4', 2, 10, 4, 'fighter10', 'fighter10')
fighter11 = fighters.fighter('4', '4', 2, 10, 4, 'fighter11', 'fighter11')
fighter12 = fighters.fighter('5', '5', 2, 10, 5, 'fighter12', 'fighter12')
fighter13 = fighters.fighter('5', '5', 2, 10, 5, 'fighter13', 'fighter13')
fighter14 = fighters.fighter('5', '5', 2, 10, 5, 'fighter14', 'fighter14')
fighter15 = fighters.fighter('6', '6', 2, 10, 6, 'fighter15', 'fighter15')
fighter16 = fighters.fighter('6', '6', 2, 10, 6, 'fighter16', 'fighter16')
fighter17 = fighters.fighter('6', '6', 2, 10, 6, 'fighter17', 'fighter17')

#frigate_test = frigates.Frigate('2','2', DISPLAYSURF, 2)
#frigate1 = frigates.Frigate('4', '4', DISPLAYSURF, 4)

fighter_list = []
fighter_list.append(fighter_test)
fighter_list.append(fighter1)
fighter_list.append(fighter2)
fighter_list.append(fighter3)
fighter_list.append(fighter4)
fighter_list.append(fighter5)
fighter_list.append(fighter6)
fighter_list.append(fighter7)
fighter_list.append(fighter8)
fighter_list.append(fighter9)
fighter_list.append(fighter10)
fighter_list.append(fighter11)
fighter_list.append(fighter12)
fighter_list.append(fighter13)
fighter_list.append(fighter14)
fighter_list.append(fighter15)
fighter_list.append(fighter16)
fighter_list.append(fighter17)

fighter_test.fighter_list = [fighter1, fighter2]
fighter_test.is_commanding = True
fighter3.fighter_list = [fighter4, fighter5]
fighter3.is_commanding = True
fighter6.fighter_list = [fighter7, fighter8]
fighter6.is_commanding = True
fighter9.fighter_list = [fighter10, fighter11]
fighter9.is_commanding = True
fighter12.fighter_list = [fighter13, fighter14]
fighter12.is_commanding = True
fighter15.fighter_list = [fighter16, fighter17]
fighter15.is_commanding = True

ships_list = [fighter_test, fighter1, fighter2, fighter3, fighter4, fighter5, fighter6, fighter7, fighter8, fighter9, fighter10, fighter11, fighter12, fighter13, fighter14, fighter15, fighter16, fighter17]
temp_list = [fighter_test, fighter1, fighter2, fighter3, fighter4, fighter5, fighter6, fighter7, fighter8, fighter9, fighter10, fighter11, fighter12, fighter13, fighter14, fighter15, fighter16, fighter17]
fighter_test.x = 200
fighter3.x = 400
fighter6.x = 100
fighter6.y = 200
fighter9.x = 200
fighter9.y = 400
fighter12.x = 400
fighter12.y = 400
fighter15.x = 500
fighter15.y = 200

game_state = 0
counter = 0

while True:
    if game_state == 0:
        title_screen.update(DISPLAYSURF)
        if title_screen.new_game_rect.collidepoint(pygame.mouse.get_pos()) == True and pygame.mouse.get_pressed()[0]:
            game_state = 1
    else:
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_e]:
            counter = 1
        if keys_pressed[pygame.K_r]:
            name1 = raw_input('Enter color here (1-6)')
            name2 = raw_input('Enter name here.')
            name3 = raw_input('Enter x coord.')
            name4 = raw_input('Enter y coord.')
            name5 = raw_input('Enter team number.')
            fighter_dict_test = fighters.fighter(name1, name1, 3, 10, int(name5), name2)
            fighter_dict_test.x = int(name3)
            fighter_dict_test.y = int(name4)
            fighter_dict[fighter_dict_test.dictionary_name] = fighter_dict_test
            fighter_list.append(fighter_dict[name2])
            ships_list.append(fighter_dict[name2])
            temp_list.append(fighter_dict[name2])

        if keys_pressed[pygame.K_t]:
            commander = raw_input('Enter ship commander name.')
            ship = raw_input('Enter fighter dict name.')
            temp1 = 0
            temp2 = 0
            for x in range(len(fighter_list)):
                if fighter_list[x].type_name == commander:
                    temp1 = x
                if fighter_list[x].dictionary_name == ship:
                    temp2 = x

            fighter_list[temp1].fighter_list.append(fighter_list[temp2])
            print(ships_list[temp1].fighter_list)

        if keys_pressed[pygame.K_g]:
            #Just make this a counter later, doesn't needa be all random.
            name1 = random.randrange(1, 7, 1)
            name2_part1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
            name2_part1 = name2_part1[random.randrange(0,6,1)]
            name2_part2 = ['abc', 'def', 'ghi', 'jkl', 'mno', 'pqr', 'stu']
            name2_part2 = name2_part2[random.randrange(0,6,1)]
            name2_part3 = str(random.randrange(1, 1000, 1))
            name3_part1 = name2_part1.join(name2_part2)
            name3 = name3_part1.join(name2_part3)
            fighter_dict_auto = fighters.fighter(str(name1), str(name1), 3, 10, name1, name3)
            fighter_dict_auto.x = 512 + random.randrange(-20, 20, 1)
            fighter_dict_auto.y = 384 + random.randrange(-20, 20, 1)
            fighter_dict[fighter_dict_auto.dictionary_name] = fighter_dict_auto
            fighter_list.append(fighter_dict[name3])
            ships_list.append(fighter_dict[name3])
            temp_list.append(fighter_dict[name3])
            auto_squadron(fighter_dict[fighter_dict_auto.dictionary_name])


        #select(frigate_test, pointer, ships_list)
        #select(frigate1, pointer, ships_list)

        for x in range(len(fighter_list)):
            if fighter_list[x].fighter_list is not None:
                fighters.squadron(DISPLAYSURF, fighter_list[x])

        collision_detection_fighters(fighter_list)

        DISPLAYSURF.blit(starfield, (0,0))

        #frigate_test.update_ship()
        #frigate1.update_ship()

        for x in range(len(fighter_list)):
            fighter_list[x].update_ship(DISPLAYSURF)

        if counter > 0:
            for x in range(len(fighter_list)):
                if fighter_list[x].formation == False:
                    fighter_list[x].target = ai.ai_target_enemy(fighter_list[x], ships_list)

        #for x in range(len(ships_list)):
           # fighter_pixel_perfect(ships_list[x], frigate_test)
        move_camera(temp_list)

        for x in range(len(ships_list)):
            if ships_list[x].delete_me == True:
                ships_list.remove(ships_list[x])
                break

        for x in range(len(fighter_list)):
            if fighter_list[x].delete_me == True:
                fighter_dict[fighter_list[x].dictionary_name] = None
                fighter_list.remove(fighter_list[x])
                break

        for x in range(len(temp_list)):
            try:
                if temp_list[x].delete_me == True:
                    temp_list.remove(temp_list[x])

                    break

            except:
                pass

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)
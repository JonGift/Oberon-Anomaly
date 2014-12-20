from __future__ import division
import pygame, sys
import math
import random
from pygame.locals import * 
#Add dogfight code. Add in boundries code.

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

    if ship.formation == False:
        ship.target = commander
        if c_x - s_x < 30:
            if s_x - c_x < 30:
                x = True
    if ship.formation == False:
        ship.target = commander
        if c_y - s_y < 30:
            if s_x - c_x < 30:
                y = True
    if x == True:
        if y == True:
            ship.target = None
            ship.acceleration = 0
            ship.speed = 0
            return True
    return False

def squadron(display_surf, commander):
    squad = []
    for i in range(len(commander.fighter_list)):
        squad.append(commander.fighter_list[i])
    squad = list(squad)
    squad_armor = 1
    for x in range(len(squad)):
        if squad[x].hp >= 0:
            squad_armor += 1
    altitude = 20
    counter = 0
    if commander.hp > 0:
        for i in range(len(squad)):
            if squad[i].hp > 0:
                squad[i].armor = squad_armor
                if squad[i].formation == False:
                    if rotate_checker(commander, squad[i]) == False:
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
                    if squad[i].bullet_cooldown == 0:
                        squad[i].is_shooting = True
                squad[i].formation = True
            else:
                squad[i].formation = False
    else:
        for i in range(len(squad)):
            squad[i].formation = False
            squad[i].afterburner = True
            squad[i].afterburner_counter = 100
        return False
    return True

class fighter:
    def __init__(self, ship_type = '1', thruster = '1', max_acc = 1, proj_speed = 3, team = 0, dictionary_name = 'Fighter', type_name = 'Fighter', delete_hp = -3, turn_speed = 5, type_reference = 'Fighter'):
        self.name = ('Temp Fighter Name')
        self.ship_type = ship_type
        self.dictionary_name = dictionary_name
        self.type_name = type_name
        self.thruster = thruster
        self.team = team
        self.type_reference = type_reference
        self.ship = pygame.image.load('img/fighter_' + self.ship_type + '.png')
        self.thruster = pygame.image.load('img/f_thrust_' + self.thruster + '.png')
        self.ship_destroyed = pygame.image.load('img/fighter_' + self.ship_type + '_destroyed.png')
        self.speed = 0
        self.turn_speed = turn_speed
        self.hp_max = 5
        self.hp = self.hp_max
        self.delete_hp = delete_hp
        self.delete_counter = 1000
        self.delete_me = False
        self.armor = 1
        self.x = 0
        self.y = 0
        self.x2 = 0
        self.y2 = 0
        self.stat_rotate = 0
        self.current_bullet = None
        self.bullet_cooldown = 0
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
        self.distance_counter = 0
        self.afterburner = False
        self.afterburner_counter = 0

        self.fighter_list = []
        self.is_commanding = False

    def __del__(self):
        print('Deleting fighter.')

    def update_ship(self, display_surf):
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1
        self.rect.center = (self.x, self.y)
        if self.hp > 0:
            self.move_calc(self.rotate, self.speed + self.acceleration)
            if self.rotate < 0:
                self.rotate = 360 + self.rotate
            if self.rotate > 360:
                self.rotate = self.rotate - 360
            if self.target is not None:
                if self.moved_by_player == False:
                    self.target = self.target
                    self.target_enemy(self.target)
                    self.speed = 1
                    if self.target.target is not None:
                        if self.target.target == self:
                            self.bullet_cooldown = 0
                            if random.randrange(0, 11, 1) > 9:
                                self.afterburner = True
                                self.afterburner_counter = 200
                            if random.randrange(0, 41, 1) > 39:
                                self.distance_counter += 1
                        else:
                            if random.randrange(0,50,1) > 48:
                                self.afterburner = True
                                self.afterburner_counter = 100
                    if self.target.hp < 1:
                        self.target = None
            else:
                if self.speed > 0:
                    self.speed -= .004

            if self.afterburner_counter < 1:
                self.afterburner_counter = 0
                self.afterburner = False
            if self.afterburner == True:
                self.afterburner_counter -= random.randrange(0,5,1)

            self.ship_final = pygame.transform.rotate(self.ship, self.rotate)
            self.thrust_final = pygame.transform.rotate(self.thruster, self.rotate)
            if self.acceleration < 0:
                self.acceleration = 0
            if self.speed < 0:
                self.speed = 0
            display_surf.blit(self.ship_final, (self.rect.center))
            if self.speed > 0:
                display_surf.blit(self.thrust_final, (self.rect.center))
                if self.acceleration < self.max_acc:
                    if self.afterburner == True:
                        self.acceleration += self.max_acc / 16
                    if self.counter2 < 10:
                        self.counter2 +=1
                    else:
                        if random.randrange(0, 4, 1) > 2:
                            self.acceleration += .1
                        self.counter2 = 0
                        self.acceleration += .2
                else:
                    if self.is_shooting == False:
                        if self.afterburner == True:
                            if self.acceleration < self.max_acc * 2:
                                self.acceleration += self.max_acc / 16
                        else:
                            if self.acceleration > self.max_acc:
                                self.acceleration -= self.max_acc / 10
                    if random.randrange(0, 4, 1) > 3:
                        self.acceleration -= .4
            else:
                self.acceleration = 0
            if self.is_shooting == True:
                self.shoot(display_surf)
            if self.thrust_override == True:
                display_surf.blit(self.thrust_final, (self.rect.center))
        else:
            if self.hp > self.delete_hp and self.delete_counter > 0:
                self.target = None
                self.acceleration = 0
                self.delete_counter -= 1
                if self.static_rotate_counter == 0:
                    self.rotate_static = self.rotate
                    self.static_rotate_counter += 1
                self.ship_destroyed_final = pygame.transform.rotate(self.ship_destroyed, self.rotate)
                self.speed = 1
                self.rotate += (self.rotate_random)*.1
                display_surf.blit(self.ship_destroyed_final, (self.move_calc(self.rotate_static, self.speed)))
                self.current_bullet = None
            else:
                self.delete_me = True
                self.fighter_list = None
                self = None
                del self

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
                        if self.is_shooting == True or self.distance_counter > 0:
                            change = 0
                            self.distance_counter += 1 + random.randrange(0, 3, 1)
                            if self.distance_counter >= 50:
                                self.distance_counter = 0
                        else:

                            if difference  <= 5 and difference >= -5:
                                change = 0
                            elif difference > 5:
                                if self.afterburner == True:
                                    change = -self.turn_speed * 1.5
                                change = -self.turn_speed
                            else:
                                if self.afterburner == True:
                                        change = self.turn_speed * 1.5
                                change = self.turn_speed

                        if(abs(difference) > 180):
                            change = 0 - change
                        if self.target is not None:
                            if self.bullet_cooldown == 0:
                                if self.target.type_name == 'Fighter' or self.target.type_name == 'Bomber':
                                    if(self.rotate < about_x1):
                                        if(self.rotate > about_x2):
                                            if self.team != self.target.team:
                                                if hyp <= self.range:
                                                    self.is_shooting = True
                                else:
                                    if(self.rotate < about_x1 + 10):
                                        if(self.rotate > about_x2 - 10):
                                            if self.team != self.target.team:
                                                if hyp <= self.range:
                                                    self.is_shooting = True


                        self.rotate += change
                        return




class Bullet:
    def __init__(self, damage = 1):
        self.name = 'bullet'
        self.__dict__.update(locals())
        self.ship_bullet = pygame.image.load('img/bullet_1.png')
        self.distance = 60
        self.range = 0
        self.delete_me = False
        self.bullet_final = self.ship_bullet
        self.damage = damage
        self.rect = self.ship_bullet.get_rect()
        self.hitmask = get_alpha_hitmask(self.ship_bullet, self.rect)

    def display(self, display_surf, *args):
        counter = 0
        temp = (args)
        coords = list(temp)
        if self.range > self.distance:
            self.delete_me = True
            return
        self.range += 1
        display_surf.blit(self.bullet_final, (args))
        for i in range(len(coords)):
            if counter == 0:
                counter += 1
                self.x = coords[i]
            else:
                self.y = coords[i]

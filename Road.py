import math
import random

import pygame
# for general data to all classes below-------------


class DataForClasses:
    WHITE = None
    H_OF_W = 0
    W_OF_W = 0
    MARGIN = 0
    GREEN = None
    LIST_OF_PRESETS = {}

    def __init__(self, HofW, WofW, Margin, list):
        DataForClasses.H_OF_W = HofW
        DataForClasses.W_OF_W = WofW
        DataForClasses.MARGIN = Margin
        DataForClasses.GREEN = (0, 255, 0)
        DataForClasses.LIST_OF_PRESETS = list
        DataForClasses.WHITE = (255, 255, 255)

# Class for menu buttons


class Buttons(pygame.sprite.Sprite, DataForClasses):
    def __init__(self, x, y, width, height, title, Menu_num, filename=None):
        pygame.sprite.Sprite.__init__(self)
        if filename is not None:
            self.image = pygame.image.load(filename).convert()
            self.image.set_colorkey((23, 21, 22))
        else:
            self.image = pygame.image.load("images/for_buttons.bmp").convert()
        if Menu_num in DataForClasses.LIST_OF_PRESETS.values():
            self.image = pygame.image.load(
                "images/for_buttons_pr.bmp").convert()
        self.image.set_colorkey((23, 21, 22))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.pr_img = pygame.image.load("images/for_buttons_pr.bmp").convert()
        self.pr_img = pygame.transform.scale(self.pr_img, (width, height))
        self.unpr_img = pygame.image.load("images/for_settings.png").convert()
        self.unpr_img = pygame.transform.scale(self.unpr_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.title = title
        self.menu_num = Menu_num

    def check_condition(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.rect.x < mouse[0] < self.rect.right:
            if self.rect.y < mouse[1] < self.rect.bottom:
                if click[0] == 1 and self.menu_num not in [21, 22]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def update(self, *args):
        if args[0] == "check_cond":
            return self.check_condition()
        elif args[0] == "get_title":
            return self.title
        elif args[0] == "get_menu_stage":
            return self.menu_num
        elif args[0] == "set_unpr_img":
            self.image = self.unpr_img
        elif args[0] == "set_pr_img":
            self.image = self.pr_img
# Class for barriers on the road


class RoadBarrier(pygame.sprite.Sprite, DataForClasses):
    def __init__(
            self,
            filename,
            height,
            width,
            type_of_barrier,
            delay_min,
            delay_max,
            existing_after_col,
            speed_sub,
            score_min,
            score_pl,
            obj_speed=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(DataForClasses.GREEN)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.speed_sub = speed_sub
        self.width = width
        self.height = height
        self.score_pl = score_pl
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.myevent = 0
        self.score_min = score_min
        self.delay_rnd = random.randrange(delay_min, delay_max)
        self.iterator_to_del = 0
        if type_of_barrier != "Finish":
            self.rect.x = random.randrange(
                self.MARGIN + 2,
                self.W_OF_W - self.MARGIN - self.width - 2)
        else:
            self.rect.x = DataForClasses.MARGIN
        self.rect.y = - height - 5
        self.del_of_spawn = 0
        self.type_of_barrier = type_of_barrier
        self.fl_for_falling = False
        self.to_continue_exist = False
        self.existing_after_col = existing_after_col
        self.obj_speed = obj_speed
        self.set_barriers_position()
        self.cur_tr = 0
        self.cur_FPS = 0

    def to_spawn_obj(self):
        ex_delay = 1
        if self.cur_FPS == 100:
            ex_delay = 1.7
        elif self.cur_FPS == 120:
            ex_delay = 2
        self.myevent += ((1 + self.cur_tr) * ex_delay)
        if self.myevent >= self.delay_rnd:
            self.delay_rnd = random.randrange(self.delay_min, self.delay_max)
            self.myevent = 0
            return True
        else:
            return False

    def set_spd(self, speed, cur_FPS):
        self.cur_tr = speed
        self.cur_FPS = cur_FPS

# method that sets position of every barrier

    def set_barriers_position(self):
        if self.type_of_barrier == "police_block":
            self.rect.x = DataForClasses.MARGIN + 590
        elif self.type_of_barrier == "Wh_car_60":
            self.rect.x = random.randrange(0, 2)
            if self.rect.x == 1:
                self.rect.x = DataForClasses.MARGIN + 5
            else:
                self.rect.x = DataForClasses.MARGIN + 435
        elif self.type_of_barrier == "Pol_60":
            self.rect.x = random.randrange(0, 2)
            if self.rect.x == 1:
                self.rect.x = DataForClasses.MARGIN + 155
            else:
                self.rect.x = DataForClasses.MARGIN + 500
        elif self.type_of_barrier == "Truck_80":
            self.rect.x = random.randrange(0, 2)
            if self.rect.x == 1:
                self.rect.x = DataForClasses.MARGIN + 70
            else:
                self.rect.x = DataForClasses.MARGIN + 285
        elif self.type_of_barrier == "Taxi_60":
            self.rect.x = random.randrange(0, 2)
            if self.rect.x == 1:
                self.rect.x = DataForClasses.MARGIN + 220
            else:
                self.rect.x = DataForClasses.MARGIN + 370

    def fall(self, speed):
        if self.rect.y < DataForClasses.H_OF_W:
            self.rect.y += (speed - self.obj_speed)
        else:
            self.rect.bottom = 0
            self.fl_for_falling = False
            if self.type_of_barrier != "Finish":
                self.rect.x = random.randrange(
                    DataForClasses.MARGIN +
                    2,
                    DataForClasses.W_OF_W -
                    DataForClasses.MARGIN -
                    self.width -
                    2)
            self.set_barriers_position()

    def update(self, *args):
        if args[0] == "fall":
            self.fall(args[1])
        elif args[0] == "get_score_min":
            return self.score_min
        elif args[0] == "set_bar_pos":
            self.set_barriers_position()
        elif args[0] == "wait_set_delay":
            return self.to_spawn_obj()
        elif args[0] == "set_spd_and_FPS":
            self.set_spd(args[1], args[2])
        elif args[0] == "get_delay":
            return self.myevent
        elif args[0] == "get_score_pl":
            return self.score_pl
        elif args[0] == "get_del_rnd":
            return self.delay_rnd
        elif args[0] == "get_type_br":
            return self.type_of_barrier
        elif args[0] == "get_spawn_delay":
            return self.del_of_spawn
        elif args[0] == "set_flag_for_fall":
            if self.fl_for_falling is False:
                self.fl_for_falling = True
            else:
                self.fl_for_falling = False
        elif args[0] == "get_fl_for_falling":
            return self.fl_for_falling
        elif args[0] == "get_height":
            return self.height
        elif args[0] == "get_width":
            return self.width
        elif args[0] == "set_continuing_roading":
            if self.existing_after_col is True:
                self.to_continue_exist = args[1]
        elif args[0] == "get_existing_after_col":
            return self.existing_after_col
        elif args[0] == "get_continuing_roading":
            return self.to_continue_exist
        elif args[0] == "get_cur_spd":
            return self.cur_tr
        elif args[0] == "get_speed_sub":
            if self.speed_sub == 1:
                if self.cur_tr > 1:
                    return self.cur_tr - 1
                else:
                    return 1
            elif self.speed_sub == 2:
                if self.cur_tr > 2:
                    return self.cur_tr - 2
                else:
                    return 1
            elif self.speed_sub == 3:
                return 1

# for explosion animation -------------------------


class car_crush(pygame.sprite.Sprite, DataForClasses):
    def __init__(self, car, car_rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = car
        self.car_rect = car_rect
        self.blast = pygame.image.load("images/boom.bmp").convert()
        self.blast.set_colorkey(DataForClasses.GREEN)
        self.blast = pygame.transform.scale(self.blast, (98, 152))
        self.blast_rekt = self.blast.get_rect()

    def crush_1(self, rect):
        self.rect = rect
        x = self.rect.x
        y = self.rect.y - 24
        self.blast_rekt = [x, y]
# Class for opponents cars


class Opponent(pygame.sprite.Sprite, DataForClasses):
    def __init__(
            self,
            x,
            y,
            filename,
            w,
            margin,
            turn_to,
            detect_obj,
            speed,
            perc_of_dodging,
            name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image = pygame.transform.scale(self.image, (60, 138))
        self.image.set_colorkey(self.GREEN)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.fl_dodged = False
        self.fl_l = False
        self.fl_r = False
        self.tmp_turnto = self.turn_to = turn_to
        self.W_of_window = w
        self.Car_slizzy = 0
        self.F_slizzy = 0
        self.speed = speed
        self.tmp_speed = speed
        self.car_rot = pygame.transform.rotate(self.image, 0)
        self.detect_obj = detect_obj
        self.Margin = margin + 20
        self.perc_of_dodging = perc_of_dodging
        self.flag_of_dodging = 0
        self.F_ops_Slizzy = 0
        self.Name = name
        self.catch_user = self.catch_op = 0
        self.rem_y = 0
    # to moving opponent's car

    def moving(self, speed, opspeed):
        self.rect.y += speed - opspeed

    def update(self, *args):
        if args[0] == "moving":
            self.moving(args[1], self.speed)
        elif args[0] == "Get_name":
            return self.Name
        elif args[0] == "dodging":
            if random.randrange(
                    1, 101) <= self.perc_of_dodging and self.flag_of_dodging == 0:
                self.dodging(args[1], args[2], args[3], args[4])
            else:
                self.flag_of_dodging = 1
        elif args[0] == "get_F_ops_slizzy":
            return self.F_ops_Slizzy
        elif args[0] == "set_F_ops_slizzy":
            self.F_ops_Slizzy = args[1]
        elif args[0] == "dodged":
            self.dodged()
        elif args[0] == "alignment":
            self.alignment(args[1], args[2], args[3])
        elif args[0] == "change_fl_dodging":
            self.change_flag_dodging()
        elif args[0] == "rotate_car":
            self.rotating()
        elif args[0] == "check_speed":
            return self.speed
        elif args[0] == "check_slizzy":
            return self.F_slizzy
        elif args[0] == "Slizzy_on":
            self.turn_to = 1
            self.F_slizzy = 1
            self.Car_slizzy = 0
        elif args[0] == "change_speed":
            self.speed = args[1]
        elif args[0] == "Slizzy_off":
            self.turn_to = self.tmp_turnto
            self.F_slizzy = 0
            self.speed = self.tmp_speed
            self.Car_slizzy = 0
        elif args[0] == "rotating_img":
            return self.car_rot
        elif args[0] == "catch_up_user":
            self.catch_up_user()
        elif args[0] == "catch_up_opponent":
            self.catch_up_opponent()
        elif args[0] == "remember_y_of_op":
            self.rem_y = self.rect.centery
        elif args[0] == "get_rem_y":
            return self.rem_y

    def change_flag_dodging(self):
        self.flag_of_dodging = 0

    def turn_op(self, x_br, w_br, flag):
        if flag is False:
            sdvig = self.rect.x + 60 - x_br - 1
            sdvig = math.ceil(sdvig / self.turn_to)
            if self.rect.x - sdvig * self.turn_to < 0 + self.Margin or sdvig < 0:
                return False
            else:
                return True
        else:
            sdvig = x_br + w_br - self.rect.x + 1
            sdvig = math.ceil(sdvig / self.turn_to)
            if self.rect.right + sdvig * self.turn_to > self.W_of_window - self.Margin:
                return False
            else:
                return True

    def dodging(self, x_br, y_br, wid_br, height):
        if self.rect.right in range(
                x_br,
                x_br +
                wid_br //
                2) or self.rect.centerx in range(
                x_br,
                x_br +
                wid_br) or self.rect.right >= x_br and x_br in range(
                self.rect.x,
                self.rect.right) or self.fl_l is True and self.fl_r is False:
            if self.rect.y - y_br - height <= self.detect_obj and y_br + height >= 0:
                if self.turn_op(x_br, wid_br, False) is True:
                    self.rect.x -= self.turn_to
                else:
                    if self.rect.x < x_br + \
                            wid_br and self.rect.right <= (self.W_of_window - self.Margin) // 2:
                        self.rect.x += self.turn_to
                        self.fl_r = True
        elif self.rect.x in range(x_br + wid_br // 2, x_br + wid_br) \
            or self.rect.x <= x_br + wid_br and x_br + wid_br in range(self.rect.x, self.rect.right)\
                or self.fl_r is True:
            if self.rect.y - y_br - height <= self.detect_obj and y_br + height >= 0:
                if self.turn_op(x_br, wid_br, True) is True:
                    self.rect.x += self.turn_to
                else:
                    self.rect.x -= self.turn_to
                    self.fl_l = True

    def dodged(self):
        self.fl_r = self.fl_l = False

    def rotating(self):
        if self.F_slizzy == 1:
            self.car_rot = pygame.transform.rotate(self.image, self.Car_slizzy)
            self.Car_slizzy += 1
            self.car_rot.set_colorkey((0, 255, 0))
            if self.Car_slizzy == 70:
                self.F_slizzy = 2
        elif self.F_slizzy == 2:
            self.car_rot = pygame.transform.rotate(self.image, self.Car_slizzy)
            self.Car_slizzy -= 1
            self.car_rot.set_colorkey((0, 255, 0))
            if self.Car_slizzy == -30:
                self.F_slizzy = 3
        elif self.F_slizzy == 3:
            self.car_rot = pygame.transform.rotate(self.image, self.Car_slizzy)
            self.Car_slizzy += 1
            self.car_rot.set_colorkey((0, 255, 0))
            if self.Car_slizzy == 0:
                self.F_slizzy = 4

# method to catch up user car
    def catch_up_user(self):
        self.catch_user += 1
        if self.catch_user == 3000:
            self.rect.top = self.H_OF_W
            self.rect.x = self.W_of_window // 2
            self.catch_user = 0

# method to catch up opponent car
    def catch_up_opponent(self):
        self.catch_op += 1
        if self.catch_op == 2000:
            self.rect.x = self.W_of_window // 2
            self.rect.bottom = 0
            self.catch_op = 0

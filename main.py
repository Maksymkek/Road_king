import random
from datetime import datetime
import os
import pygame
from Road import RoadBarrier, car_crush, Opponent, DataForClasses, Buttons

pygame.init()
H = 900  # Height of the main window
W = 920  # Width of the main window
MARGIN = 25  # Margin right and left in game window
sc = pygame.display.set_mode((500, 750))
pygame.display.set_caption("Road King")
sc.fill((59, 59, 61))
# ----------------- colors -----------------------------
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
# ------------------------------------------------------
# ====================== FONTS =========================
BASE_FONT = pygame.font.SysFont('Consolas', 20, True)
TITLE_FONT = pygame.font.SysFont('Mistral', 70)
MENU_FONT = pygame.font.SysFont('Consolas', 34, True)
FILE_FONT = pygame.font.SysFont('Consolas', 18, True)
AUTHOR_FONT = pygame.font.SysFont('Mistral', 20)
VERS_FONT = pygame.font.SysFont('Consolas', 18)
# ====================== ===== =========================
# ##############################################################################################
# ############################### INITIALIZING PARTS OF THE GAME PROCESS #
# ##############################################################################################
barriers = pygame.sprite.Group()  # group for barriers
opponents = pygame.sprite.Group()  # group for opponents
# ==================== playable car initializing ======================
# playable car_surface load
car_sc = pygame.image.load("images/car_4.bmp").convert()
car_sc = pygame.transform.scale(car_sc, (60, 138))
car_rot_sc = car_sc = pygame.transform.scale(car_sc, (60, 138))
car_sc.set_colorkey(GREEN)
car_rect = car_sc.get_rect()
chng_tr = {1: 5, 2: 10, 3: 14, 4: 21, 5: 28, 6: 35}  # variants of speeds
cur_tr = 1  # current transmission
speed = 5  # for speed
turnto = 8  # for sensitivity
del_trans_add = 0  # iterator for transmission(adding)
del_trans_sub = 0  # iterator for transmission(subbing)
angle_to_rot = 0  # angle for rotating(Slizzy animation)(Don't TOUCH!!)
fl_for_rot = 0  # flag for rotating animation
tempturnto = turnto  # for unblocking sensitivity on rotating method
# ====================== game elements initializing ======================
score = 1000  # amount of scores in game
FPS = 60  # (recommended: 60, supports any)

myframe = pygame.time.Clock()  # to FPS control
for_road_anim = 0  # iterator for road animation
# ------------- Finish --------------
finish_f = 0  # event for Finish
finish_timer = 50000  # time from start to finish
bFinish = RoadBarrier("images/Финишная_линия.bmp", 100, W -
                      MARGIN, "Finish", 2, 22, True, 1, 50, 0, )
# -----------------------------------
List_of_preset = {"FPS": FPS, "Sensetivity": turnto}
data = DataForClasses(H, W, MARGIN, List_of_preset)
# ----------- for blast animation ---------------
Boom = car_crush(car_sc, car_rect)
flForBoom = 0
# -----------------------------------------------
# #################################################################################
# #################### INITIALIZING PARTS OF MENU PROCESS ################
# #################################################################################
Menu_stage = 0  # switcher between stages on menu
Menu = True  # switcher to menu cycle
frst_line_read = -1  # frow what line we start reading
sc = pygame.display.set_mode((500, 750))
bg_menu = pygame.image.load("images/фон_меню.bmp").convert()
lvl = 0  # for lvl of difficult
x_mouse = y_mouse = 0  # to save cursor position for click
List_of_settings = {
    "FPS": [
        60, 100, 120], "Sensetivity": [
            6, 8, 12]}  # for settings
# ----------------------------RGB for Menu--------------------------------
# dict of flags to switch menu color(Text_menu_gradient())
fl_RGB_menu = {'R': 0, 'G': 0, 'B': 0}
R_menu = 220
G_menu = 80
B_menu = 0
Zero_btns = pygame.sprite.Group()
Frst_btns = pygame.sprite.Group()
Third_btns = pygame.sprite.Group()
Sens_btns = pygame.sprite.Group()
Scor_btns = pygame.sprite.Group()
FPS_btns = pygame.sprite.Group()


def set_ui_buttons():
    global Zero_btns, Frst_btns, Third_btns, FPS_btns, Sens_btns, Scor_btns
    Bt1 = Buttons(
        75,
        180,
        160,
        160,
        'Вибрати складність',
        1,
        "images/chg_dif.png")
    Bt2 = Buttons(
        180,
        350,
        160,
        160,
        '    Досягнення',
        2,
        'images/trophies.png')
    Bt3 = Buttons(
        285,
        520,
        160,
        160,
        '   Налаштування',
        3,
        'images/settings.png')
    Zero_btns.add([Bt1, Bt2, Bt3])

    Bt4 = Buttons(
        75,
        200,
        355,
        80,
        '     Новачок',
        11,
        "images/for_lvl_dif.png")
    Bt5 = Buttons(
        75,
        290,
        355,
        80,
        '     Любитель',
        12,
        "images/for_lvl_dif.png")
    Bt6 = Buttons(
        75,
        380,
        355,
        80,
        '     Вправний',
        13,
        "images/for_lvl_dif.png")
    Bt7 = Buttons(
        75,
        470,
        355,
        80,
        '      Профі',
        14,
        "images/for_lvl_dif.png")
    Bt8 = Buttons(75, 560, 355, 80, '      Назад', 0)
    Frst_btns.add([Bt4, Bt5, Bt6, Bt7, Bt8])

    Bt9 = Buttons(75, 200, 355, 80, '       FPS', 31)
    Bt10 = Buttons(75, 290, 100, 80, '60', 60, "images/for_settings.png")
    Bt11 = Buttons(203, 290, 100, 80, '100', 100, "images/for_settings.png")
    Bt12 = Buttons(330, 290, 100, 80, '120', 120, "images/for_settings.png")
    Bt13 = Buttons(75, 380, 355, 80, '    Чутливість', 32)
    Bt14 = Buttons(75, 470, 100, 80, 'Низ', 6, "images/for_settings.png")
    Bt15 = Buttons(203, 470, 100, 80, 'Сер', 8, "images/for_settings.png")
    Bt16 = Buttons(330, 470, 100, 80, 'Вис', 12, "images/for_settings.png")
    Third_btns.add([Bt9, Bt10, Bt11, Bt12, Bt13, Bt14, Bt15, Bt16, Bt8])
    FPS_btns.add(Bt10, Bt11, Bt12)
    Sens_btns.add(Bt14, Bt15, Bt16)

    Bt18 = Buttons(75, 200, 355, 80, " Найкраща спроба", 21)
    Bt19 = Buttons(75, 600, 355, 80, '      Назад', 0)
    Bt20 = Buttons(75, 330, 355, 80, "  Останні спроби", 22)
    Scor_btns.add([Bt18, Bt19, Bt20])


# ------------------------------------------------------------------------
# ------------------------- MENU BUTTONS ADDING --------------------------
set_ui_buttons()
# --------------------------------------------------------------------------
# #############################################################################################
# #############################################################################################
# #############################################################################################
# method to set finish time


def set_finish(time):
    global lvl, finish_f
    finish_f = time
# method to make an iredescent colors


def text_menu_gradient(color, switcher):
    global fl_RGB_menu
    if color < 255 and fl_RGB_menu.get(switcher) == 0:
        color += 1
        return color
    else:
        color -= 1
        fl_RGB_menu[switcher] = 1
        if color == 0:
            fl_RGB_menu[switcher] = 0
            return color
        else:
            return color
# ===================== Method to turn on game process ==================


def Set_game_window(lvl_difficulty):
    global sc, flForBoom, for_road_anim, score,\
        del_trans_add, del_trans_sub, angle_to_rot, fl_for_rot, cur_tr, speed, for_user_color, bg_sc, bg_rect, W,\
        MARGIN, turnto, \
        tempturnto, bFinish, lvl, FPS
    lvl = lvl_difficulty
    sc = pygame.display.set_mode((W, H))
    car_rect.bottom = H - H // 100  # car's position height
    car_rect.x = W // 2 - 30
    flForBoom = 0
    for_road_anim = 0
    score = 1000
    del_trans_add = 0
    del_trans_sub = 0
    for_user_color = 0
    angle_to_rot = 0
    fl_for_rot = 0
    cur_tr = 1
    speed = 5
    bar_start_delay = 1000
    Scorepl = Score_min = 25
    speed_sub = 1
    obj_speed = 1
    turnto = tempturnto
    op_det_obj = 100
    op_speed = 5
    op2_speed = 0
    if lvl_difficulty == 1:
        bar_start_delay = 700
        Scorepl = Score_min = 25
        speed_sub = 1
        obj_speed = 1
        op_det_obj = 100
        op_speed = 5
        op2_speed = 3
        bg_sc = pygame.image.load("images/асфальт.bmp").convert()
    elif lvl_difficulty == 2:
        bar_start_delay = 100
        Scorepl = Score_min = 25
        speed_sub = 1
        obj_speed = 1
        op_det_obj = 100
        op_speed = 6
        op2_speed = 7
        bg_sc = pygame.image.load("images/трасса_сложность_2.bmp").convert()
    elif lvl_difficulty == 3:
        bar_start_delay = 200
        Scorepl = Score_min = 25
        speed_sub = 1
        obj_speed = 1
        op_det_obj = 100
        op_speed = 7
        op2_speed = 13
        bg_sc = pygame.image.load("images/трасса_сложность_3.bmp").convert()
    elif lvl_difficulty == 4:
        bar_start_delay = 500
        Scorepl = Score_min = 25
        speed_sub = 1
        obj_speed = 1
        op_det_obj = 200
        op_speed = 9
        op2_speed = 9
        bg_sc = pygame.image.load("images/трасса_сложность_4.bmp").convert()
    sc.fill((16, 16, 16))
    bg_sc = pygame.transform.scale(bg_sc, (W - 50, H))
    bg_rect = bg_sc.get_rect()
    bg_rect.x = MARGIN
    bg_rect.y = 0
    car_rect.bottom = H - H // 100
    car_rect.x = W // 2 - 30
    br1 = RoadBarrier(
        "images/клякса_1.bmp",
        70,
        40,
        "klyaksa",
        bar_start_delay,
        900,
        True,
        1,
        Score_min,
        Scorepl)
    br2 = RoadBarrier(
        "images/truck.bmp",
        320,
        80,
        "Truck_80",
        bar_start_delay,
        2500,
        False,
        2,
        Score_min * 3,
        Scorepl,
        1)
    br3 = RoadBarrier(
        "images/Полицейские шипы.bmp",
        75,
        276,
        "police_block",
        bar_start_delay,
        1300,
        False,
        3,
        Score_min,
        Scorepl)
    br4 = RoadBarrier(
        "images/taxi.bmp",
        138,
        60,
        "Taxi_60",
        bar_start_delay,
        1200,
        False,
        2,
        Score_min * 2,
        Scorepl,
        2)
    br5 = RoadBarrier(
        "images/police_1.bmp",
        138,
        60,
        "Pol_60",
        bar_start_delay,
        1500,
        False,
        2,
        Score_min * 2,
        Scorepl,
        2)
    br6 = RoadBarrier(
        "images/white_car.bmp",
        138,
        60,
        "Wh_car_60",
        bar_start_delay,
        1800,
        False,
        2,
        Score_min * 2,
        Scorepl,
        3)
    bFinish = RoadBarrier(
        "images/Финишная_линия.bmp",
        100,
        W - MARGIN * 2,
        "Finish",
        2,
        22,
        True,
        1,
        50,
        0,
    )
    barriers.add(br1, br2, br3, br4, br5, br6)
    op_1 = Opponent(
        car_rect.x + 90,
        car_rect.y,
        "images/car_5.bmp",
        W,
        MARGIN,
        10,
        op_det_obj,
        op_speed,
        100,
        "Sophia Marthines")
    op_2 = Opponent(
        car_rect.x + 90,
        car_rect.y - 200,
        "images/car_2_1.bmp",
        W,
        MARGIN,
        10,
        op_det_obj + 70,
        op2_speed + 6,
        100,
        "Jack Benton")
    op_3 = Opponent(
        car_rect.x,
        car_rect.y - 200,
        "images/car_2.bmp",
        W,
        MARGIN,
        10,
        op_det_obj + 100,
        op_speed + 10,
        100,
        "Sally Teylor")
    op_4 = Opponent(
        car_rect.x,
        car_rect.y +
        200,
        "images/car_4.bmp",
        W,
        MARGIN,
        10,
        op_det_obj +
        100,
        op_speed +
        random.randrange(
            1,
            10),
        100,
        "Rey Carter")
    opponents.add(op_1, op_2, op_3, op_4)
    set_finish(2000 * FPS)
    set_start_readiness()
# ================== Method for menu animation ==================


def enter_menu():
    global Menu, Menu_stage, FPS, R_menu, G_menu, B_menu, frst_line_read, x_mouse, y_mouse, turnto
    while Menu:
        sc.fill(BLACK)
        sc.blit(bg_menu, bg_menu.get_rect())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x_mouse = event.pos[0]
                y_mouse = event.pos[1]
        R_menu = text_menu_gradient(R_menu, 'R')
        G_menu = text_menu_gradient(G_menu, 'G')
        B_menu = text_menu_gradient(B_menu, 'B')
        Text1 = TITLE_FONT.render("Road King", True, (R_menu, G_menu, B_menu))
        sc.blit(Text1, (135, 74))
        if Menu_stage == 0:
            for b in Zero_btns:
                if b.update("check_cond") is False:
                    sc.blit(b.image, b.rect)
                else:
                    pygame.mouse.set_pos([135, 70])
                    Menu_stage = b.update("get_menu_stage")

        elif Menu_stage == 1:
            for b1 in Frst_btns:
                if b1.update("check_cond") is False:
                    sc.blit(b1.image, b1.rect)
                    Text_b = MENU_FONT.render(
                        b1.update("get_title"), True, (R_menu, G_menu, B_menu))
                    sc.blit(Text_b, (b1.rect.x + 10, b1.rect.centery - 10))
                else:
                    pygame.mouse.set_pos([135, 70])
                    Menu_stage = b1.update("get_menu_stage")
                    if b1.update("get_menu_stage") == 11:
                        Menu = False
                        Set_game_window(1)
                    elif b1.update("get_menu_stage") == 12:
                        Menu = False
                        Set_game_window(2)
                    elif b1.update("get_menu_stage") == 13:
                        Menu = False
                        Set_game_window(3)
                    elif b1.update("get_menu_stage") == 14:
                        Menu = False
                        Set_game_window(4)
        elif Menu_stage == 2:
            y_of_line = 420
            Best_Score = -1000
            Best_line = None

            if os.path.isfile("Scores.txt") and os.path.getsize(
                    "Scores.txt") != 0:
                f = open("Scores.txt", 'r')
                frst_line_read = -1
                if frst_line_read == -1:
                    frst_line_read = f.read().count('Scores') - 7
                    if frst_line_read < 0:
                        frst_line_read = 0
                it_lines = 0
                f.close()
                f = open("Scores.txt", 'r')
                try:
                    for line in f:
                        if line != '\n':
                            if it_lines >= frst_line_read:
                                Text_f = FILE_FONT.render(
                                    line[0:-1], True, (R_menu, G_menu, B_menu))
                                sc.blit(Text_f, (16, y_of_line))
                                y_of_line += 25
                            if int(line[39:]) > Best_Score:
                                Best_Score = int(line[39:])
                                Best_line = FILE_FONT.render(
                                    line[0:-1], True, (R_menu, G_menu, B_menu))

                            it_lines += 1
                except BaseException:
                    print("smth get wrong ;(")
                f.close()
                sc.blit(Best_line, (16, 297))
            else:
                f = open("Scores.txt", 'w')
                f.close()
            for b in Scor_btns:
                if b.update("check_cond") is False:
                    sc.blit(b.image, b.rect)
                    Text_b = MENU_FONT.render(
                        b.update("get_title"), True, (R_menu, G_menu, B_menu))
                    sc.blit(Text_b, (b.rect.x + 10, b.rect.centery - 10))
                else:
                    pygame.mouse.set_pos([135, 70])
                    Menu_stage = b.update("get_menu_stage")
        elif Menu_stage == 3:
            for b in Third_btns:
                if b.update("check_cond") is False:
                    sc.blit(b.image, b.rect)
                    Text_b = MENU_FONT.render(
                        b.update("get_title"), True, (R_menu, G_menu, B_menu))
                    sc.blit(Text_b, (b.rect.x + 10, b.rect.centery - 10))
                else:
                    if b.update("get_menu_stage") not in [
                            8, 6, 12, 60, 120, 100, 32, 31]:
                        Menu_stage = b.update("get_menu_stage")
                    elif b.update("get_menu_stage") in List_of_settings.get("FPS"):
                        tmp = b.update("get_menu_stage")
                        for bf in FPS_btns:
                            if bf.update("get_menu_stage") == tmp:
                                bf.update("set_pr_img")
                                FPS = tmp
                            else:
                                bf.update("set_unpr_img")
                    elif b.update("get_menu_stage") in List_of_settings.get("Sensetivity"):
                        tmp = b.update("get_menu_stage")
                        for bf in Sens_btns:
                            if bf.update("get_menu_stage") == tmp:
                                bf.update("set_pr_img")
                                turnto = tmp
                            else:
                                bf.update("set_unpr_img")
                    pygame.mouse.set_pos([135, 70])
        Avtor = AUTHOR_FONT.render(
            "Designed by Hryshchenkov Maksym", True, (255, 12, 12))
        Vers = VERS_FONT.render("v1.1", True, (B_menu, R_menu, G_menu))
        sc.blit(Vers, (MARGIN + 9, 710))
        sc.blit(Avtor, (260, 710))
        text = BASE_FONT.render("FPS:" + str(int(myframe.get_fps())),
                                True, (R_menu, G_menu, B_menu))
        sc.blit(text, (0, 0))
        pygame.display.update()
        myframe.tick(FPS)
    sc.fill(BLACK)
# ============== For countdown before game process will be started =======


def set_start_readiness():
    global W, H, Menu_stage, Menu, sc
    F_for_num = 3
    Readiness = True
    R_start = 0
    flag_to_color = False
    text = text_1 = None
    font_1 = pygame.font.SysFont("Mistral", 130, True)
    font_2 = pygame.font.SysFont("Consolas", 30, True)
    while Readiness:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                F_for_num = F_for_num
        sc.fill(BLACK)
        if F_for_num == 3:
            text = font_1.render("3", True, (R_start, 0, 0))
            text_1 = font_2.render(
                "Для повороту машини клавіши K_left та K_right", True, (R_start, 0, 0))
        elif F_for_num == 2:
            text = font_1.render("2", True, (R_start, 0, 0))
            text_1 = font_2.render(
                "Для зміни передач клавіши K_up та K_down", True, (R_start, 0, 0))
        elif F_for_num == 1:
            text = font_1.render("1", True, (R_start, 0, 0))
            text_1 = font_2.render(
                "Для паузи натисніть Space", True, (R_start, 0, 0))
        elif F_for_num == 0:
            text = font_1.render("Go!", True, (R_start, 0, 0))
            text_1 = font_2.render("", True, (R_start, 0, 0))
        else:
            Readiness = False
        if R_start < 255 and flag_to_color is False:
            R_start += 1
        else:
            R_start -= 1
            flag_to_color = True
            if R_start == 0:
                flag_to_color = False
                F_for_num -= 1
        txt_rect = text.get_rect()
        txt_rect.centerx = W // 2
        txt_rect.centery = H // 2
        sc.blit(text, txt_rect)
        txt_1_rect = text_1.get_rect()
        txt_1_rect.centerx = W // 2
        txt_1_rect.bottom = H - 28
        sc.blit(text_1, txt_1_rect)
        pygame.display.update()
        myframe.tick(120)
# function to set flags for rotating user car after crushing in barrier ---


def fl_rot_car_on():
    global angle_to_rot, fl_for_rot, turnto
    angle_to_rot = 0
    fl_for_rot = 1
    turnto = 1
# ============= to update road after transmission changes =================


def road_update():
    global for_road_anim
    for_road_anim = bg_rect.y = 0

# ------------------------------- For printing list of drivers -----------


def Set_list_of_places(car_pos):
    list_of_coord.append(car_pos)


def get_list_of_places():
    list_of_coord.sort()
    for el in list_of_coord:
        if car_rect.y != el or "You" in list_of_places:
            for op in opponents:
                if op.rect.y == el:
                    list_of_places.append(op.update("Get_name"))
        else:
            list_of_places.append("You")
    print_list_of_places()


for_user_color = 0  # for function Print_list_of_places()
list_of_coord = []
list_of_places = []
fl_fr_places = 0


def print_list_of_places():
    it = 1
    Marg_top = 25
    global MARGIN, for_user_color, fl_fr_places
    list_of_coord.clear()
    for el in list_of_places:
        if el != "You":
            text_1 = BASE_FONT.render(
                '#' + str(it) + ' ' + str(el), True, (0, 0, 0))
        else:
            if for_user_color < 255 and fl_fr_places == 0:
                for_user_color += 1
            else:
                fl_fr_places = 1
                if for_user_color >= 1:
                    for_user_color -= 1
                else:
                    fl_fr_places = 0
            text_1 = BASE_FONT.render(
                '#' + str(it) + ' ' + str(el), True, (for_user_color, 0, 0))
        sc.blit(text_1, (MARGIN, Marg_top))
        Marg_top += 30
        it += 1
# ========================== for printing Score ======================


def resetListsofPlaces():
    list_of_coord.clear()
    list_of_coord.append(car_rect.y)
    list_of_places.clear()


def print_score():
    RGB = None
    global score, W, MARGIN
    if score >= 3000:
        RGB = (16, 171, 32)
    elif score >= 1500:
        RGB = (219, 223, 60)
    else:
        RGB = (232, 30, 35)
    text = BASE_FONT.render('Score: ' + str(score), True, RGB)
    txt1 = text.get_rect()
    txt1.right = W - MARGIN
    txt1.y = 0
    sc.blit(text, txt1)
# ======================= method that writes scores to file ===============


def write_score():
    myfile = None
    if os.path.isfile("Scores.txt"):
        myfile = open("Scores.txt", 'a')
    else:
        myfile = open("Scores.txt", 'w')
    myfile.write(
        datetime.now().strftime("Date: %d %m %Y time: %H %M %S") +
        " Scores: " +
        str(score) +
        '\n')
    myfile.close()


enter_menu()
stop = False
# =============== method for setting a pause in game process =============


def set_pause():
    global GREEN, FPS, sc, myframe, R_menu, G_menu, B_menu, W, H, MENU_FONT
    pygame.event.clear()
    pause_turn = True
    while pause_turn is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                enter_menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause_turn = False
        R_menu = text_menu_gradient(R_menu, 'R')
        G_menu = text_menu_gradient(G_menu, 'G')
        B_menu = text_menu_gradient(B_menu, 'B')
        pygame.draw.rect(sc, (R_menu, G_menu, B_menu),
                         (W // 2 - 40, H // 2 - 55, 30, 90))
        pygame.draw.rect(sc, (R_menu, G_menu, B_menu),
                         (W // 2, H // 2 - 55, 30, 90))
        Text_b = MENU_FONT.render(
            "Натисніть 'Space' щоб продовжити", True, (R_menu, G_menu, B_menu))
        sc.blit(Text_b, (155, H - 40))
        pygame.display.update()
        myframe.tick(FPS)
# ------------method for getting result after finishing--------------------


def get_result():
    global Menu, Menu_stage, sc, score, stop, BLACK
    stop = False
    sc = pygame.display.set_mode((500, 750))
    MyPosition = list_of_places.index("You") + 1
    if MyPosition == 1:
        score *= 4
    elif MyPosition == 2:
        score *= 3
    elif MyPosition == 3:
        score *= 2
    write_score()
    best_score = True
    text = text1 = None
    with open("Scores.txt") as f:
        try:
            for line in f:
                if line != '\n':
                    if int(line[40:-1]) > score:
                        best_score = False
                        break
        except BaseException:
            print("Error in reading file in method Get_result()")
    if best_score:
        text = MENU_FONT.render("КРАЩИЙ РЕЗУЛЬТАТ !!!", True, (96, 244, 122))
        text1 = MENU_FONT.render(str(score), True, (96, 244, 122))
    else:
        text = MENU_FONT.render("Непогано !", True, (237, 164, 103))
        text1 = MENU_FONT.render(str(score), True, (237, 164, 103))
    bg_menu = pygame.image.load("images/фон_меню.bmp").convert()
    sc.blit(bg_menu, bg_menu.get_rect())
    sc.blit(text, (105, 280))
    sc.blit(text1, (105, 345))
    pygame.display.update()
    Menu_stop = False
    while Menu_stop is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or score <= 0:
                Menu_stage = 0
                Menu = True
                sc = pygame.display.set_mode((500, 750))
                enter_menu()
                Menu_stop = True

        myframe.tick(FPS)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or score <= 0:
            Menu_stage = 0
            Menu = True
            sc = pygame.display.set_mode((500, 750))
            for op in opponents:
                op.kill()
            for b in barriers:
                b.kill()
            bFinish.kill()
            enter_menu()
            sc.fill((16, 16, 16))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                set_pause()
    if finish_f <= 0:
        bFinish.fall(speed)
        if bFinish.rect.colliderect(car_rect):
            score *= lvl
            for op in opponents:
                op.kill()
            for b in barriers:
                b.kill()
            bFinish.kill()
            get_result()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_rect.x -= turnto
        if car_rect.x < MARGIN:
            car_rect.x = MARGIN
    elif keys[pygame.K_RIGHT]:
        car_rect.x += turnto
        if car_rect.x > W - 60 - MARGIN:
            car_rect.x = W - 60 - MARGIN
    elif keys[pygame.K_UP]:
        if cur_tr != 6 and fl_for_rot == 0:
            del_trans_add += 1
            if del_trans_add > FPS:
                speed = chng_tr.get(cur_tr + 1)
                cur_tr += 1
                del_trans_add = 0
                road_update()
    elif keys[pygame.K_DOWN]:
        if cur_tr != 1:
            del_trans_sub += 1
            if del_trans_sub > FPS:
                speed = chng_tr.get(cur_tr - 1)
                cur_tr -= 1
                del_trans_sub = 0
                road_update()
    # here is a barriers  # to update current speed in
    # Data_for_classes(Road.py)
    for bar in barriers:
        bar.update("set_spd_and_FPS", cur_tr, FPS)
        if bar.update("get_fl_for_falling") is True:
            bar.update("fall", speed)
            if bar.rect.bottom == 0:
                bar.update("set_continuing_roading", True)
                opponents.update("dodged")
                opponents.update("change_fl_dodging")
                score += bar.update("get_score_pl") * cur_tr
            if bar.rect.colliderect(car_rect):
                if bar.update("get_continuing_roading") is True:
                    road_update()
                    cur_tr = bar.update("get_speed_sub")
                    speed = chng_tr.get(cur_tr)
                    fl_rot_car_on()
                    score -= bar.update("get_score_min")
                    bar.update("set_continuing_roading", False)
                    opponents.update("dodged")
                else:
                    if bar.update("get_existing_after_col") is False:
                        Boom.crush_1(bar.rect)
                        bar.rect.bottom = 0
                        bar.update("set_bar_pos")
                        road_update()
                        flForBoom = 1
                        score -= bar.update("get_score_min")
                        cur_tr = bar.update("get_speed_sub")
                        speed = chng_tr.get(cur_tr)
                        fl_rot_car_on()
                        opponents.update("dodged")
                        bar.update("set_flag_for_fall")

            for op in opponents:
                if bar.rect.colliderect(op.rect):
                    if bar.update("get_continuing_roading") is True:
                        road_update()
                        op.update("change_speed", (op.update("check_speed")))
                        op.update("Slizzy_on")
                        opponents.update("dodged")
                        op.update("set_F_ops_slizzy", 1)
                        bar.update("set_continuing_roading", False)
                    else:
                        if bar.update("get_existing_after_col") is False:
                            Boom.crush_1(bar.rect)
                            bar.rect.bottom = 0
                            bar.update("set_bar_pos")
                            op.update("change_speed", 5)
                            op.update("Slizzy_on")
                            road_update()
                            flForBoom = 1
                            op.update("set_F_ops_slizzy", 1)
                            bar.update("set_flag_for_fall")
                            opponents.update("dodged")
        else:
            if bar.update("wait_set_delay") is True:
                bar.update("set_flag_for_fall")
    # here is a control of cars colliding
    for op in opponents:
        if car_rect.colliderect(op.rect):
            if op.rect.bottom - 5 < car_rect.y < op.rect.bottom + 5:
                if cur_tr != 1:
                    cur_tr -= 1
                    speed = chng_tr.get(cur_tr)
                    road_update()
            elif car_rect.bottom - 5 < op.rect.y < op.rect.bottom + 5:
                op.rect.y -= 10
            elif op.rect.x >= car_rect.x + 55:
                if car_rect.x >= 5 + MARGIN:
                    car_rect.x -= 5
                if op.rect.right <= W - 5 - MARGIN:
                    op.rect.x += 5
            else:
                if car_rect.right <= W - 5 - MARGIN:
                    car_rect.x += 5
                if op.rect.x >= 5 + MARGIN:
                    op.rect.x -= 5
    # here is a road moving logic
    for_road_anim += speed
    Test1 = for_road_anim + speed - H
    if Test1 >= H:
        Test1 = -H
        for_road_anim = 0
    bg_rect.y = bg_rect.y + speed
    if bg_rect.y >= H:
        bg_rect.bottom = 0 + speed
    # here is an opponent

    for op in opponents:
        for bar in barriers:
            if bar.update("get_fl_for_falling") is True:
                opponents.update("dodged")
                opponents.update(
                    "dodging",
                    bar.rect.x,
                    bar.rect.y,
                    bar.update("get_width"),
                    bar.update("get_height"))
    # here is an output on display
    sc.blit(bg_sc, (bg_rect.x, Test1))
    sc.blit(bg_sc, bg_rect)
    sc.blit(bFinish.image, bFinish.rect)
    barriers.draw(sc)
    # here an animation of Slizzy road(car rotating)
    if fl_for_rot == 0:
        sc.blit(car_sc, (car_rect.x, car_rect.y))
    else:
        if fl_for_rot == 1:
            car_rot_sc = pygame.transform.rotate(car_sc, angle_to_rot)
            angle_to_rot += 1
            if angle_to_rot == 70:
                fl_for_rot = 2
        elif fl_for_rot == 2:
            car_rot_sc = pygame.transform.rotate(car_sc, angle_to_rot)
            angle_to_rot -= 1
            if angle_to_rot == -30:
                fl_for_rot = 3
        elif fl_for_rot == 3:
            car_rot_sc = pygame.transform.rotate(car_sc, angle_to_rot)
            angle_to_rot += 1
            if angle_to_rot == 0:
                fl_for_rot = 0
                turnto = tempturnto
        car_rot_sc.set_colorkey(GREEN)
        sc.blit(car_rot_sc, car_rect)
    # here is an animation of slizzy road(car rotating) for opponents
    for op in opponents:
        if op.rect.bottom not in range(-60, H + 198):
            op.update("remember_y_of_op")
            if speed >= op.update("check_speed"):
                if op.update("get_rem_y") < 0:
                    op.update("catch_up_opponent")
            else:
                if op.update("get_rem_y") > H + 138:
                    op.update("catch_up_user")
    for op in opponents:
        if op.update("get_F_ops_slizzy") == 0:
            sc.blit(op.image, op.rect)
        else:
            if 0 < op.update("check_slizzy") <= 4:
                if op.update("check_slizzy") == 4:
                    op.update("set_F_ops_slizzy", 0)
                    op.update("Slizzy_off")
                    sc.blit(op.image, op.rect)
                else:
                    op.update("rotate_car")
                    sc.blit(op.update("rotating_img"), op.rect)
    resetListsofPlaces()
    opponents.update("moving", speed)
    if 0 < flForBoom < FPS / 2:
        sc.blit(Boom.blast, Boom.blast_rekt)
        flForBoom += 1
    for op in opponents:
        Set_list_of_places(op.rect.y)
    get_list_of_places()
    text = BASE_FONT.render("FPS:" + str(int(myframe.get_fps())),
                            True, (136, 0, 21))
    finish_f -= speed
    print_score()
    sc.blit(text, (MARGIN, 0))
    text = MENU_FONT.render("Transmission:" + str(cur_tr),
                            True, (136, 0, 21))
    sc.blit(text, (MARGIN, H-40))
    pygame.display.update()
    myframe.tick(FPS)

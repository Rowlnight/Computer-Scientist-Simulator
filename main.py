import pygame
import os
import pylab
from pygame.locals import *
import cv2
import pickle
import random

import load_data
from button import Button, MCT
from plot import Plot

dir = os.path.abspath(os.curdir)

pygame.init()
pygame.mixer.init()

def add_image(file):
    image = pygame.image.load(os.path.join(file))
    image.convert()
    return image

WIDTH, HEIGHT = load_data.get_WIDTH_HEIGHT()

center_WIDTH = WIDTH / 2
center_HEIGHT = HEIGHT / 2

FPS = 30
main_font = dir + '\\Data\\fonts\\main.ttf'

WHITE, BLACK, RED, GREEN, BLUE, YELLOW, GREY, GREY_GAME = load_data.get_colors()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
current_size = screen.get_size()
virtual_surfase = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Computer Scientist Simulator")
clock = pygame.time.Clock()

sound_1 = dir + '\\Data\\sounds\\main.mp3'
button_sound = pygame.mixer.Sound(dir + '\\Data\\sounds\\button.mp3')
fear = pygame.mixer.Sound(dir + '\\Data\\sounds\\fear.mp3')
threat_has_passed = pygame.mixer.Sound(dir + '\\Data\\sounds\\threat_has_passed.mp3')
screamer2_sound = pygame.mixer.Sound(dir + '\\Data\\sounds\\screamer2_sound.mp3')
mind_4 = dir + '\\Data\\sounds\\mind4.mp3'

sain_sound_1 = pygame.mixer.Sound(dir + '\\Data\\sounds\\sain_sound_1.mp3')
sain_sound_2 = pygame.mixer.Sound(dir + '\\Data\\sounds\\sain_sound_2.mp3')
sain_sound_3 = pygame.mixer.Sound(dir + '\\Data\\sounds\\sain_sound_3.mp3')

pygame.mixer.music.load(sound_1)
pygame.mixer.music.play(loops=-1)



class Text:
    def __init__(self, font_color=BLACK, font_tipe=main_font, font_size=30):
        self.font_type = pygame.font.Font(font_tipe, font_size)
        self.font_color = font_color
        
    def print_text(self, message, x, y):
        text = self.font_type.render(message, True, self.font_color)
        screen.blit(text, (x, y))


class Improvements:
    def __init__(self, width, height, name, start_cost, rise_in_price, start_levl, improved_coefficient, power_of_improvement):
        self.name = name
        self.start_cost = start_cost
        self.rise_in_price = rise_in_price
        self.start_levl = start_levl
        self.improved_coefficient = improved_coefficient
        self.power_of_improvement = power_of_improvement
        self.width = width
        self.height = height

    def draw(self, x, y, font=15):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        pygame.draw.rect(screen, GREY, (x, y, self.width, self.height))
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            if click[0] == 1 and self.start_cost <= GAME.SKILLS and MCT.CL_check:
                pygame.mixer.Sound.play(GAME.level_up)
                pygame.time.delay(30)
                
                GAME.MONEY = GAME.MONEY - self.start_cost
                GAME.spent_per_turn = GAME.spent_per_turn + self.start_cost
                
                if self.improved_coefficient == 'improve_company_profit':
                    GAME.company_profit = GAME.company_profit + self.improved_coefficient
                    self.start_levl = self.start_levl + 1
                    GAME.MONEY = GAME.MONEY - self.start_cost
                    self.start_cost = self.start_cost + self.rise_in_price
                elif self.improved_coefficient == 'improve_SKILL_BONUS':
                    GAME.SKILL_BONUS = GAME.SKILL_BONUS + self.power_of_improvement
                    self.start_levl = self.start_levl + 1
                    GAME.SKILLS = GAME.SKILLS - self.start_cost
                    self.start_cost = self.start_cost + self.rise_in_price
                elif self.improved_coefficient == 'improve_repair_bonus':
                    GAME.repair_bonus = GAME.repair_bonus + self.power_of_improvement
                    self.start_levl = self.start_levl + 1
                    GAME.SKILLS = GAME.SKILLS - self.start_cost
                    self.start_cost = self.start_cost + self.rise_in_price
                elif self.improved_coefficient == 'improve_bonus_sales':
                    GAME.bonus_sales = GAME.bonus_sales + self.power_of_improvement
                    self.start_levl = self.start_levl + 1
                    GAME.SKILLS = GAME.SKILLS - self.start_cost
                    self.start_cost = self.start_cost + self.rise_in_price
                

        main_text.print_text(self.name + ' на ' + str(self.power_of_improvement), x + 23, y + 10)
        main_text.print_text(str(self.start_cost) + ' ОН', x + 23, y + 30)
        main_text.print_text('Уровень: ' + str(self.start_levl), x + 300, y + 30)

    def get_cost(self):
        return self.start_cost

    def get_levl(self):
        return self.start_levl

class Product:
    def __init__(self, width, height, min_price, max_price, names_list):
        self.width = width
        self.height = height
        self.min_price = min_price
        self.max_price = max_price
        self.names_list = names_list

    def draw(self, x, y, font=15):
        MONEY = GAME.MONEY
        warehouse_log = GAME.warehouse_log
        can_buy = GAME.can_buy
        CL_check = MCT.CL_check
        spent_per_turn = GAME.spent_per_turn
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        pygame.draw.rect(screen, GREY, (x, y, self.width, self.height))
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            if click[0] == 1 and self.is_sold == 0 and self.price <= MONEY and can_buy and CL_check:
                pygame.mixer.Sound.play(GAME.buy)
                pygame.time.delay(30)
                
                MONEY = MONEY - self.price
                spent_per_turn = spent_per_turn + self.price
                status = random.randint(1, 100)
                warehouse_log = self.name + ' ' + str(self.price) + ' ' + str(status)
                warehouse_log = warehouse_log.split()
                
                self.is_sold = 1
                can_buy = False

        main_text.print_text(self.name, x + 23, y + 10)
        main_text.print_text(str(self.price) + ' ₽', x + 23, y + 30)

        if self.is_sold:
            main_text.print_text('Продано', x + 163, y + 30)
        else:
            main_text.print_text('Не продано', x + 163, y + 30)


    def recover(self):
        self.is_sold = random.randint(0, 1)
        self.price = random.randint(self.min_price, self.max_price)
        self.name = random.choice(self.names_list)

        
class Hallucination(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.is_real = False
        self.is_checked = False
        self.entity = ''
        self.sain_veu = 11
        self.live_hallucination = False
        self.timer = 0
        
    def chenge_entity(self, entity, xy, WIDTH_HEIGHT):
        self.x = xy[0]
        self.y = xy[1]
        self.WIDTH = WIDTH_HEIGHT[0]
        self.HEIGHT = WIDTH_HEIGHT[1]
        self.entity = entity
        self.images = []
        for image in os.listdir(dir + '\\Data\\textures\\Hallucination_entity\\' + entity):
            if '.' in image:
                self.images.append(pygame.image.load(dir + '\\Data\\textures\\Hallucination_entity\\' + entity + '\\' + image))
        self.index = 0
        self.image = self.images[self.index]
        sur = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.rect = sur.get_rect(center=(self.x, self.y))

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))

class Screamer(pygame.sprite.Sprite):
    def __init__(self, xy, WIDTH_HEIGHT, function):
        pygame.sprite.Sprite.__init__(self)
        self.x = xy[0]
        self.y = xy[1]
        self.WIDTH = WIDTH_HEIGHT[0]
        self.HEIGHT = WIDTH_HEIGHT[1]
        self.is_scremming = False
        self.function = function

    def chenge_screamer(self, sound, dirrectory):
        self.sound = sound
        self.images = []
        print(dirrectory)
        for image in os.listdir(dirrectory):
            if '.' in image:
                self.images.append(pygame.image.load(dirrectory + '\\' + image))

        self.index = 0
        self.image = self.images[self.index]
        sur = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.rect = sur.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.is_scremming = True

    def update(self):
        if self.is_scremming:
            if self.index >= len(self.images):
                self.index = 0
                self.is_scremming = False
                self.function()
            elif self.index == 0:
                pygame.mixer.Sound.play(self.sound)
                pygame.time.delay(30)
            self.image = self.images[self.index]
            self.index += 1
    
class Main_game_logick:
    def __init__(self):
        self.is_running = True
        self.game_mode = 'main-menu'

        self.repair_fail = pygame.mixer.Sound(dir + '\\Data\\sounds\\repair_fail.mp3')
        self.buy = pygame.mixer.Sound(dir + '\\Data\\sounds\\buy.mp3')
        self.successful_repair = pygame.mixer.Sound(dir + '\\Data\\sounds\\successful_repair.mp3')
        self.lack_of = pygame.mixer.Sound(dir + '\\Data\\sounds\\lack_of.mp3')
        self.level_up = pygame.mixer.Sound(dir + '\\Data\\sounds\\level_up.mp3')
        self.update_info = pygame.mixer.Sound(dir + '\\Data\\sounds\\update_info.mp3')

        self.max_mind_per_minute = 500
        self.mind_per_minute = 25

        self.max_mind_on_repair = 500
        self.mind_on_repair = 100

        self.mind_on_sleep = -200

        self.mind_group = {"time": ["разум сейчас", 500],
                           "repair": ["разум сейчас", 500]}


    def get_improvements(self):
        self.company_profit_upgrade = Improvements(430, 60, 'Улучшить доход компании',
                                                   self.company_profit_upgrade_cost_now, 50,
                                                   self.company_profit_upgrade_levl_now, 'improve_company_profit', 1500)
        
        self.SKILL_BONUS_upgrade = Improvements(430, 60, 'Улучшить прирост очков навыка',
                                                self.SKILL_BONUS_upgrade_cost_now, 5,
                                                self.SKILL_BONUS_upgrade_levl_now, 'improve_SKILL_BONUS', 1)
        
        self.repair_bonus_upgrade = Improvements(430, 60, 'Улучшить бонус починки',
                                                 self.repair_bonus_upgrade_cost_now, 5,
                                                 self.repair_bonus_upgrade_levl_now, 'improve_repair_bonus', 0.1)
        
        self.bonus_sales_upgrade = Improvements(430, 60, 'Улучшить бонус продажи без починки',
                                                self.bonus_sales_upgrade_cost_now, 5,
                                                self.bonus_sales_upgrade_levl_now, 'improve_bonus_sales', 0.05)

    def get_plot(self):
        self.stocks_plot = Plot(self.stocks_list)
        
    def start_new_game(self):
        [self.can_buy, self.is_repaired, self.old_repair_cost_PC, self.MONEY,
        self.DAY, self.SKILLS, self.SKILL_BONUS, self.warehouse_log, self.repair_bonus,
        self.bonus_sales, self.DEBT, self.stocks_cost, self.stocks_list, self.stocks,
        self.spent_per_turn, self.received_per_turn, self.day_get_crdit, self.company, self.company_profit,
        self.total_sold, self.total_money_spent, self.total_money_earned, self.purchased_for,
        self.research_started, self.research_days, self.research_result,
        self.company_profit_upgrade_cost_now, self.company_profit_upgrade_levl_now,
        self.SKILL_BONUS_upgrade_cost_now, self.SKILL_BONUS_upgrade_levl_now,
        self.repair_bonus_upgrade_cost_now, self.repair_bonus_upgrade_levl_now,
        self.bonus_sales_upgrade_cost_now, self.bonus_sales_upgrade_levl_now,

        self.mind, self.mind_stage, self.mind_group["time"][0], self.mind_group["repair"][0]

        ] = load_data.get_data_for_new_game()

        self.get_improvements()
        self.get_plot()

        video_background.bg_now = dir + '\\Data\\textures\\game.mp4'
        self.game_mode = 'game'

    def load_game(self):
        try:
            with open(dir + '\\Data\\Save\\save.dat', 'rb') as f:
                [self.can_buy, self.is_repaired, self.old_repair_cost_PC, self.MONEY, self.DAY, self.SKILLS, self.SKILL_BONUS, self.warehouse_log, self.repair_bonus,
                self.bonus_sales, self.DEBT, self.stocks_cost, self.stocks_list, self.stocks, self.spent_per_turn, self.received_per_turn, self.day_get_crdit,
                self.company, self.company_profit, self.total_sold, self.total_money_spent, self.total_money_earned, self.purchased_for, self.research_days,
                self.research_started, self.research_result, self.company_profit_upgrade_cost_now, self.company_profit_upgrade_levl_now,
                self.SKILL_BONUS_upgrade_cost_now, self.SKILL_BONUS_upgrade_levl_now, self.repair_bonus_upgrade_cost_now, self.repair_bonus_upgrade_levl_now,
                self.bonus_sales_upgrade_cost_now, self.bonus_sales_upgrade_levl_now,

                self.mind, self.mind_stage, self.mind_group["time"][0], self.mind_group["repair"][0]] = pickle.load(f)

        except Exception as error:
            print(error)
            return

        self.get_improvements()
        self.get_plot()

        self.company_profit_upgrade = Improvements(430, 60, 'Улучшить доход компании', self.company_profit_upgrade_cost_now, 50, self.company_profit_upgrade_levl_now, 'improve_company_profit', 10000)
        self.SKILL_BONUS_upgrade = Improvements(430, 60, 'Улучшить прирост очков навыка', self.SKILL_BONUS_upgrade_cost_now, 5, self.SKILL_BONUS_upgrade_levl_now, 'improve_SKILL_BONUS', 1)
        self.repair_bonus_upgrade = Improvements(430, 60, 'Улучшить бонус починки', self.repair_bonus_upgrade_cost_now, 5, self.repair_bonus_upgrade_levl_now, 'improve_repair_bonus', 0.1)
        self.bonus_sales_upgrade = Improvements(430, 60, 'Улучшить бонус продажи без починки', self.bonus_sales_upgrade_cost_now, 5, self.bonus_sales_upgrade_levl_now, 'improve_bonus_sales', 0.05)

        video_background.bg_now = dir + '\\Data\\textures\\game.mp4'
        self.game_mode = 'game'

    def save_game(self):
        company_profit_upgrade_cost_now = self.company_profit_upgrade.get_cost()
        company_profit_upgrade_levl_now = self.company_profit_upgrade.get_levl()
        SKILL_BONUS_upgrade_cost_now = self.SKILL_BONUS_upgrade.get_cost()
        SKILL_BONUS_upgrade_levl_now = self.SKILL_BONUS_upgrade.get_levl()
        repair_bonus_upgrade_cost_now = self.repair_bonus_upgrade.get_cost()
        repair_bonus_upgrade_levl_now = self.repair_bonus_upgrade.get_levl()
        bonus_sales_upgrade_cost_now = self.bonus_sales_upgrade.get_cost()
        bonus_sales_upgrade_levl_now = self.bonus_sales_upgrade.get_levl()

        self.current_mind_on_repair = self.mind_group["repair"][0]
        self.current_mind_per_minute = self.mind_group["time"][0]
    
        with open(dir + '\\Data\\Save\\save.dat', 'wb') as f:
            pickle.dump([self.can_buy, self.is_repaired,
                         self.old_repair_cost_PC, self.MONEY,
                         self.DAY, self.SKILLS,
                         self.SKILL_BONUS, self.warehouse_log,
                         self.repair_bonus, self.bonus_sales,
                         self.DEBT, self.stocks_cost,
                         self.stocks_list, self.stocks,
                         self.spent_per_turn, self.received_per_turn,
                         self.day_get_crdit, self.company,
                         self.company_profit, self.total_sold,
                         self.total_money_spent, self.total_money_earned,
                         self.purchased_for, self.research_days,
                         self.research_started, self.research_result,
                         company_profit_upgrade_cost_now, company_profit_upgrade_levl_now,
                         SKILL_BONUS_upgrade_cost_now, SKILL_BONUS_upgrade_levl_now,
                         repair_bonus_upgrade_cost_now, repair_bonus_upgrade_levl_now,
                         bonus_sales_upgrade_cost_now, bonus_sales_upgrade_levl_now,

                         self.mind, self.mind_stage, self.mind_group["time"][0], self.mind_group["repair"][0]], f)

    def return_to_main_menu(self):
        self.save_game()
        video_background.bg_now = dir + '\\Data\\textures\\main_menu.mp4'
        self.game_mode = 'main-menu'
        video_background.draw_game_menu = False

    def exit_game(self):
        self.is_running = False

    def shoping(self):
        video_background.bg_now = dir + '\\Data\\textures\\activity.mp4'
        self.game_mode = 'shoping'

    def taxes(self):
        video_background.bg_now = dir + '\\Data\\textures\\bank.mp4'
        self.game_mode = 'bank'

    def skip_a_move(self):
        self.DAY = self.DAY + 1
        self.MONEY = self.MONEY - 2500
        if self.DEBT > 0:
            self.MONEY = self.MONEY - 1000
            self.DEBT = self.DEBT - 1000
        if self.DEBT < 0:
            self.DEBT = 0
        if self.research_started and self.research_days > 0:
            self.research_days = self.research_days - 1
    
        standart_product_1.recover()
        standart_product_2.recover()
        standart_product_3.recover()
        standart_product_4.recover()
        standart_product_5.recover()
        standart_product_6.recover()
        standart_product_7.recover()

        self.MONEY = self.MONEY + self.company_profit
        if self.DAY % 5 == 0:
            self.stocks_cost = random.randint(1, 25000)
        else:
            local_help = random.randint(0, 1)
            if local_help == 1:
                self.stocks_cost = self.stocks_cost + random.randint(100, 1500)
            else:
                self.stocks_cost = self.stocks_cost - random.randint(100, 1500)
        self.stocks_list.append(self.stocks_cost)
        if len(self.stocks_list) >= 16:
            self.stocks_list.pop(0)
        self.stocks_plot.reshow(self.stocks_list)
        if self.day_get_crdit < 10:
            self.day_get_crdit = self.day_get_crdit + 1
        self.total_money_earned = self.total_money_earned + self.received_per_turn + self.company_profit
        if self.DEBT > 0:
            self.total_money_spent = self.total_money_spent + self.spent_per_turn + 2500 + 1000
        else:
            self.total_money_spent = self.total_money_spent + self.spent_per_turn + 2500

        self.game_mode = 'skip_a_move'

        video_background.bg_now = dir + '\\Data\\textures\\pause.mp4'

        self.save_game()

    def completion_of_the_skip_a_move(self):
        self.spent_per_turn = 0
        self.received_per_turn = 0

        self.add_mind(1200)
        self.day_mind_control()

        self.game_mode = 'game'
        video_background.bg_now = dir + '\\Data\\textures\\game.mp4'

    def trade(self):
        video_background.bg_now = dir + '\\Data\\textures\\pause.mp4'
        self.game_mode = 'trade'

    def warehouse(self):
        video_background.bg_now = dir + '\\Data\\textures\\activity.mp4'
        self.game_mode = 'warehouse'

    def repair_pc(self):
        video_background.bg_now = dir + '\\Data\\textures\\workshop.mp4'
        self.game_mode = 'repair_pc'
        already_analyzed = True

    def sale(self, price_PC):
        self.warehouse_log = ''
        if int(self.status_PC) == 0:
            self.MONEY = (int(self.price_PC) + self.MONEY) + ((int(price_PC) + self.old_repair_cost_PC) * self.repair_bonus) + 4500
            self.received_per_turn = self.received_per_turn + ((int(price_PC) + self.old_repair_cost_PC) * self.repair_bonus) + int(price_PC) + 4500
        else:
            self.MONEY = self.MONEY + int(price_PC) + (int(price_PC) * self.bonus_sales)
            self.received_per_turn = self.received_per_turn + int(price_PC) + (int(price_PC) * self.bonus_sales)
        self.can_buy = True
        self.is_repaired = False
        self.already_analyzed = False

        self.total_sold = self.total_sold + 1

        self.MONEY = int(round(self.MONEY, 0))

        pygame.mixer.Sound.play(self.buy)
        pygame.time.delay(30)

    def completion_of_the_repair(self):  ##################################################################
        video_background.bg_now = dir + '\\Data\\textures\\activity.mp4'
        self.game_mode = 'warehouse'
        pygame.mixer.Sound.play(self.repair_fail)
        pygame.time.delay(30)

    def cancellation_of_repairs(self):  ##################################################################
        video_background.bg_now = dir + '\\Data\\textures\\activity.mp4'
        self.game_mode = 'warehouse'
    
    def go_back(self):
        video_background.bg_now = dir + '\\Data\\textures\\game.mp4'
        self.game_mode = 'game'

    def by_stocks(self):
        if self.MONEY >= self.stocks_cost and not self.stocks:
            self.MONEY = self.MONEY - self.stocks_cost
            self.spent_per_turn = self.spent_per_turn + self.stocks_cost
            self.stocks = True
            self.purchased_for = self.stocks_cost
            pygame.mixer.Sound.play(self.buy)
            pygame.time.delay(30)
        else:
            pygame.mixer.Sound.play(self.lack_of)
            pygame.time.delay(30)

    def sale_stocks(self):
        if self.stocks:
            self.MONEY = self.MONEY + self.stocks_cost
            self.received_per_turn = self.received_per_turn + self.stocks_cost
            self.stocks = False
            pygame.mixer.Sound.play(self.buy)
            pygame.time.delay(30)
        else:
            pygame.mixer.Sound.play(self.lack_of)
            pygame.time.delay(30)

    def pay_off(self, num):
        if self.day_get_crdit >= 10:
            self.MONEY = self.MONEY + num
            if num < 10000:
               self.DEBT = self.DEBT + num + 1000
               self.day_get_crdit = 8
            else:
                self.DEBT = self.DEBT + num + 5000
                self.day_get_crdit = 0
            
            pygame.mixer.Sound.play(self.buy)
            pygame.time.delay(30)

    def show_information(self):
        video_background.bg_now = dir + '\\Data\\textures\\info_bg.mp4'
        self.game_mode = 'show_information'

    def pay_debt(self, num):
        if self.MONEY >= num and self.DEBT > 0:
            self.MONEY = self.MONEY - num
            self.DEBT = self.DEBT - num
            if self.DEBT < 0:
                self.DEBT = 0
            pygame.mixer.Sound.play(self.buy)
            pygame.time.delay(30)
        else:
            pygame.mixer.Sound.play(self.lack_of)
            pygame.time.delay(30)

    #
    # работа с разумом ==================
    #

    def add_mind(self, mind, mind_group=None):  # добавление разума в глобальный или mind_group счетчик
        if mind_group is None:
            self.mind += mind
        else:
            if mind < self.mind_group[mind_group][1]:  # 1 - разум сейчас; 2 - максимальный разум
                if mind + self.mind_group[mind_group][0] < self.mind_group[mind_group][1]:
                    self.mind_group[mind_group][0] += mind
                else:
                    self.mind_group[mind_group][0] = self.mind_group[mind_group][1]
        print("added mind")

    def day_mind_control(self):  # изменение разума при окончании дня
        self.add_mind(self.mind_on_sleep)
        for i in self.mind_group.items():
            print(i)
            self.mind += i[1][0]
            self.mind_group[i[0]][0] = 0
            print(i)

        if self.mind > 1000 and self.mind_stage >= 4:
            self.mind = 1000
            self.mind_stage = 4

        elif self.mind > 1000:
            self.mind = 0
            self.mind_stage += 1
            if self.mind_stage == 4:
                pygame.mixer.music.unload()
                pygame.mixer.music.load(mind_4)
                pygame.mixer.music.play(loops=-1)

        elif self.mind < 0 and self.mind_stage <= 1:
            self.mind = 0
            self.mind_stage = 1

        elif self.mind < 0:
            self.mind = 1000
            self.mind_stage -= 1
            if self.mind_stage == 3:
                pygame.mixer.music.unload()
                pygame.mixer.music.load(sound_1)
                pygame.mixer.music.play(loops=-1)

        if self.mind_stage == 1:
            pygame.mixer.music.set_volume(1)
        elif self.mind_stage == 2:
            pygame.mixer.music.set_volume(0.7)
        elif self.mind_stage == 3:
            pygame.mixer.music.set_volume(0.3)
        elif self.mind_stage == 4:
            pygame.mixer.music.set_volume(0.7)

    #
    #
    #


class Background:
    def __init__(self):
        self.bg_now = dir + '\\Data\\textures\\main_menu.mp4'
        self.bg = dir + '\\Data\\textures\\main_menu.mp4'
        self.main_menu_bg = cv2.VideoCapture(self.bg_now)
        self.success, video_image = self.main_menu_bg.read()
        self.drow_holl = False

    def drow_background(self):
        if self.bg_now != self.bg:
            self.main_menu_bg = cv2.VideoCapture(self.bg_now)
            self.bg = self.bg_now
        
        success, video_image = self.main_menu_bg.read()
        if success:
            self.video_surf = pygame.image.frombuffer(
                video_image.tobytes(), video_image.shape[1::-1], "BGR")
        else:
            self.main_menu_bg = cv2.VideoCapture(self.bg_now)
        screen.blit(self.video_surf, (0, 0))


def every_second_function():
    if GAME.game_mode != 'main-menu' and GAME.game_mode != 'skip_a_move' and GAME.DAY != 0 and \
            not hallucination.live_hallucination and GAME.game_mode != 'holl' and GAME.mind_stage == 4:
        if random.randint(1, 5) == 1 and not hallucination.is_real:
            entity = random.choice(['gallows', 'shadow'])
            if entity == 'gallows':
                place = [random.randint(50, 900), 250]
                form = [100, 400]
            elif entity == 'shadow':
                place = random.choice([[50, 250], [850, 250]])
                form = [200, 300]
            hallucination.is_real = True
            
            sain_tipe = random.randint(1, 7)
            if sain_tipe in [4, 5, 6]:
                 hallucination.sain_veu = 0
            elif sain_tipe == 1:
                pygame.mixer.Sound.play(sain_sound_1)
                pygame.time.delay(30)
            elif sain_tipe == 2:
                pygame.mixer.Sound.play(sain_sound_2)
                pygame.time.delay(30)
            elif sain_tipe == 3:
                pygame.mixer.Sound.play(sain_sound_3)
                pygame.time.delay(30)
                
            hallucination.chenge_entity(entity, place, form)
            print(1)

    if hallucination.live_hallucination:
        hallucination.is_checked = False
        hallucination.is_real = False
        hallucination.live_hallucination = False
        GAME.mind = GAME.mind - 10

    if hallucination.is_real:
        hallucination.timer += 1

    if hallucination.timer == 20:
        screamer.chenge_screamer(screamer2_sound,   dir + '\\Data\\textures\\screamer\\gat')
        hallucination.timer = 0

def control_point():
    GAME.load_game()
    hallucination.is_checked = False
    hallucination.is_real = False
    video_background.drow_holl = False
    GAME.game_mode = 'skip_a_move'
    video_background.bg_now = dir + '\\Data\\textures\\pause.mp4'


#
#
#
#
#
#
#
#
#
#


GAME = Main_game_logick()
video_background = Background()
hallucination = Hallucination()
screamer = Screamer([0, 0], [1074, 654], control_point)

main_text = Text(font_color=WHITE, font_tipe=main_font, font_size=20)
global_text = Text(font_color=WHITE, font_tipe=main_font, font_size=40)

center_x = WIDTH
center_y = HEIGHT

#---------------------------------------------------Инициализация кнопок
#-------------------------главное меню
play_btn = Button(dir + '\\Data\\textures\\buttons\\menu_btn', xy=[center_WIDTH, 200], WIDTH_HEIGHT=[180, 60],
                  sound=button_sound, text=['Играть', WHITE], target=GAME.start_new_game)
load_btn = Button(dir + '\\Data\\textures\\buttons\\menu_btn', xy=[center_WIDTH, 300], WIDTH_HEIGHT=[180, 60],
                  sound=button_sound, text=['Загрузить', WHITE], target=GAME.load_game)
out_btn = Button(dir + '\\Data\\textures\\buttons\\menu_btn', xy=[center_WIDTH, 450], WIDTH_HEIGHT=[180, 60],
                 sound=button_sound, text=['Выйти', WHITE], target=GAME.exit_game)
btn_group_main_menu = pygame.sprite.Group(play_btn, load_btn, out_btn)
#-------------------------Меню паузы
save_and_exit_btn = Button(dir + '\\Data\\textures\\buttons\\menu_btn',
                           xy=[center_WIDTH, 200], WIDTH_HEIGHT=[300, 60], sound=button_sound,
                           text=['Сохранить и выйти', WHITE], target=GAME.return_to_main_menu)
btn_group_game_menu = pygame.sprite.Group(save_and_exit_btn)
#-------------------------Рабочий стол
game_shop_btn = Button(dir + '\\Data\\textures\\buttons\\shop', xy=[50, 50], WIDTH_HEIGHT=[50, 50], sound=button_sound, text=['', WHITE], target=GAME.shoping)
game_bank_btn = Button(dir + '\\Data\\textures\\buttons\\bank', xy=[50, 120], WIDTH_HEIGHT=[50, 50], sound=button_sound, text=['', WHITE], target=GAME.taxes)
game_move_btn = Button(dir + '\\Data\\textures\\buttons\\move', xy=[1001, 600], WIDTH_HEIGHT=[50, 50], sound=button_sound, text=['', WHITE], target=GAME.skip_a_move)
game_trading_btn = Button(dir + '\\Data\\textures\\buttons\\trading', xy=[50, 190], WIDTH_HEIGHT=[50, 50], sound=button_sound, text=['', WHITE], target=GAME.trade)
game_home_btn = Button(dir + '\\Data\\textures\\buttons\\home', xy=[50, 260], WIDTH_HEIGHT=[50, 50], sound=button_sound, text=['', WHITE], target=GAME.warehouse)
game_info_btn = Button(dir + '\\Data\\textures\\buttons\\info', xy=[50, 330], WIDTH_HEIGHT=[50, 50], sound=button_sound, text=['', WHITE], target=GAME.show_information)
btn_group_game_table = pygame.sprite.Group(game_shop_btn, game_bank_btn, game_move_btn, game_trading_btn, game_home_btn, game_info_btn)
#-------------------------Покупка
game_trade_btn = Button(dir + '\\Data\\textures\\buttons\\EUG_button', xy=[950, 600], WIDTH_HEIGHT=[180, 60], sound=button_sound, text=['Назад', WHITE], target=GAME.go_back)
btn_group_trade = pygame.sprite.Group(game_trade_btn)
#-------------------------Мастерская
game_repair_btn = Button(dir + '\\Data\\textures\\buttons\\EUG_button', xy=[50, 550], WIDTH_HEIGHT=[180, 60], sound=button_sound, text=['Починить', WHITE], target=GAME.completion_of_the_repair)
game_repair_exit_btn = Button(dir + '\\Data\\textures\\buttons\\EUG_button', xy=[950, 600], WIDTH_HEIGHT=[180, 60], sound=button_sound, text=['Отмена', WHITE], target=GAME.go_back)
game_sale_btn = Button(dir + '\\Data\\textures\\buttons\\EUG_button', xy=[250, 550], WIDTH_HEIGHT=[180, 60], sound=button_sound, text=['Продать', WHITE], target=GAME.sale)
btn_group_repair = pygame.sprite.Group(game_repair_btn, game_repair_exit_btn, game_sale_btn)
#-------------------------Починка
btn_group_repair_game = pygame.sprite.Group(game_repair_exit_btn)
#-------------------------Банк
game_bank_exit_btn = Button(dir + '\\Data\\textures\\buttons\\bank_operations_btn', xy=[950, 600], WIDTH_HEIGHT=[180, 60], sound=button_sound, text=['Назад', WHITE], target=GAME.go_back)
game_bank_get_10k_btn = Button(dir + '\\Data\\textures\\buttons\\bank_operations_btn', xy=[840, 150], WIDTH_HEIGHT=[450, 60], sound=button_sound, text=['Взять в кредит 10k', WHITE], target=GAME.pay_off, arg=10000)
game_bank_get_1k_btn = Button(dir + '\\Data\\textures\\buttons\\bank_operations_btn', xy=[840, 220], WIDTH_HEIGHT=[450, 60], sound=button_sound, text=['Взять в кредит 1k', WHITE], target=GAME.pay_off, arg=1000)
game_bank_get_stocks_btn = Button(dir + '\\Data\\textures\\buttons\\bank_operations_btn', xy=[125, 550], WIDTH_HEIGHT=[250, 60], sound=button_sound, text=['Купить акции', WHITE], target=GAME.by_stocks)
game_bank_sale_stocks_btn = Button(dir + '\\Data\\textures\\buttons\\bank_operations_btn', xy=[478, 550], WIDTH_HEIGHT=[250, 60], sound=button_sound, text=['Продать акции', WHITE], target=GAME.sale_stocks)
game_bank_pay_debt_1k_btn = Button(dir + '\\Data\\textures\\buttons\\bank_operations_btn', xy=[840, 360], WIDTH_HEIGHT=[450, 60], sound=button_sound, text=['Оплатить 1K', WHITE], target=GAME.pay_debt, arg=1000)
game_bank_pay_debt_10k_btn = Button(dir + '\\Data\\textures\\buttons\\bank_operations_btn', xy=[840, 290], WIDTH_HEIGHT=[450, 60], sound=button_sound, text=['Оплатить 10K', WHITE], target=GAME.pay_debt, arg=10000)
btn_group_bank = pygame.sprite.Group(game_bank_exit_btn, game_bank_get_10k_btn, game_bank_get_1k_btn,
                                            game_bank_get_stocks_btn, game_bank_sale_stocks_btn, game_bank_pay_debt_1k_btn,
                                            game_bank_pay_debt_10k_btn)
#-------------------------СЛЕД. ход
game_next_move = Button(dir + '\\Data\\textures\\buttons\\menu_btn', xy=[472, 550], WIDTH_HEIGHT=[180, 60], sound=button_sound, text=['Продолжить', WHITE], target=GAME.completion_of_the_skip_a_move)
btn_group_next_move = pygame.sprite.Group(game_next_move)
#---------------------------------------Создание товаров

standart_product_1 = Product(270, 60, 60000, 300000, ['Игровой_пк', 'Что-то_для_игр', 'Пк_для_геймеров', 'Пк_для_любителей_игр'])
standart_product_2 = Product(270, 60, 10000, 29000, ['Старый_пк', 'Допотопный_пк', 'Офисный_компьютер', 'Старый_ноут', 'Разобранный_пк'])
standart_product_3 = Product(270, 60, 1000, 10000, ['Сломанный_пк', 'Ненужный_компьютер', 'Компьютер(много_зависает)', 'ПК_на_металлолом'])
standart_product_4 = Product(270, 60, 30000, 80000, ['Обычный_компьютер', 'Домашний_пк', 'Новый_компьютер', 'Компьютер_для_всей_семьи'])
standart_product_5 = Product(270, 60, 15000, 35000, ['Ноутбук', 'ЭВМ', 'Шайтан-машина(лють_вообще:)', 'Серверный_блок', 'Мини-компьютер', 'Бесшумный_ПК', 'Школьный_компьютер', 'Крутой_пк', 'Стационарный_компьютер'])
standart_product_6 = Product(270, 60, 1000, 54000, ['Cовременный_пк', 'Миниатюрный_компьютер', 'Универсальный_ПК', 'Ручной_компьютер', 'Базовый_пк'])
standart_product_7 = Product(270, 60, 300000, 1000000, ['Квантовый_ПК', 'Навигационный_компьютер', 'Биологический_компьютер', 'Боевой_компьютер'])
standart_product_1.recover()
standart_product_2.recover()
standart_product_3.recover()
standart_product_4.recover()
standart_product_5.recover()
standart_product_6.recover()
standart_product_7.recover()

#------------------------------------Монстр
entity_group_hallucination = pygame.sprite.Group(hallucination)
screamer_group_hallucination = pygame.sprite.Group(screamer)

one_second_counter = 0
fps_counter = 0


while GAME.is_running:
    if one_second_counter == 60 and GAME.game_mode != "main-menu":
        one_second_counter = 0
        GAME.add_mind(25, "time")
    events = pygame.event.get()
    clock.tick(FPS)

    video_background.drow_background()
    
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            GAME.is_running = False

        elif event.type == pygame.KEYDOWN and GAME.game_mode != 'main-menu' and GAME.game_mode != 'skip_a_move':
            if event.key == pygame.K_SPACE:
                if not video_background.drow_holl:
                    video_background.drow_holl = True
                    bg_remowed = video_background.bg_now
                    game_mode_remowed = GAME.game_mode
                    GAME.game_mode = 'holl'
                    video_background.bg_now = dir + '\\Data\\textures\\holl.mp4'
                    
                    if hallucination.is_real and not hallucination.is_checked:
                        pygame.mixer.Sound.play(fear)
                        pygame.time.delay(30)
                        hallucination.is_checked = True
                        hallucination.live_hallucination = True
                        hallucination.timer = 0
                    elif not hallucination.is_real and not hallucination.is_checked:
                        pygame.mixer.Sound.play(threat_has_passed)
                        pygame.time.delay(30)
                else:
                    video_background.drow_holl = False
                    video_background.bg_now = bg_remowed
                    GAME.game_mode = game_mode_remowed
    
    if GAME.game_mode == 'main-menu' and not video_background.drow_holl:
        main_text.print_text('Computer Scientist Simulator', 180, 50)
        btn_group_main_menu.update()
        btn_group_main_menu.draw(screen)

    elif GAME.game_mode == 'game'and not video_background.drow_holl:
        main_text.print_text('День: ' + str(GAME.DAY + 1), 915, 25)
        main_text.print_text('Сознание: ' + str(GAME.mind_stage), 915, 50)
        btn_group_game_table.update()
        btn_group_game_table.draw(screen)

    elif GAME.game_mode == 'trade' and not video_background.drow_holl:
        main_text.print_text('Сегодня в продаже', 380, 25)
        main_text.print_text('Ваш счёт: ' + str(GAME.MONEY) + ' ₽', 480, 75)
        
        standart_product_1.draw(402, 100, font=15)
        standart_product_2.draw(402, 170, font=15)
        standart_product_3.draw(402, 240, font=15)
        standart_product_4.draw(402, 310, font=15)
        standart_product_5.draw(402, 380, font=15)
        standart_product_6.draw(402, 450, font=15)
        standart_product_7.draw(402, 520, font=15)

        btn_group_trade.update()
        btn_group_trade.draw(screen)

    elif GAME.game_mode == 'warehouse' and not video_background.drow_holl:
        if GAME.warehouse_log != '':
            if GAME.name_PC != GAME.warehouse_log[0]:
                GAME.name_PC = GAME.warehouse_log[0]
                GAME.price_PC = GAME.warehouse_log[1]
                if not GAME.is_repaired:
                    GAME.status_PC = GAME.warehouse_log[2]
                else:
                    GAME.status_PC = 0
                GAME.repair_cost_PC = int(round(1000 * (int(GAME.status_PC) / 100), 0))

            main_text.print_text('В наличии компьютер: ' + GAME.name_PC, 50, 50)
            
            if not GAME.is_repaired:
                main_text.print_text('Цена: ' + str(int(round(int(GAME.price_PC) + (int(GAME.price_PC) * GAME.bonus_sales)))) + ' ₽', 50, 100)
            else:
                main_text.print_text('Цена: ' + str(int(round(((int(GAME.price_PC) + GAME.old_repair_cost_PC) * GAME.repair_bonus) + int(GAME.price_PC) + 4500))) + ' ₽', 50, 100)
                
            main_text.print_text('Поломки: ' + str(GAME.status_PC) + ' %', 50, 150)
            main_text.print_text('Стоимость починки: ' + str(GAME.repair_cost_PC) + ' ₽', 50, 200)
            main_text.print_text('Ваш счёт: ' + str(GAME.MONEY) + ' ₽', 800, 50)

        btn_group_repair.update()
        btn_group_repair.draw(screen)

    elif GAME.game_mode == 'repair_pc' and not video_background.drow_holl:
        btn_group_repair_game.update()
        btn_group_repair_game.draw(screen)

    elif GAME.game_mode == 'bank' and not video_background.drow_holl:
        global_text.print_text('Банк', center_WIDTH, 20)
        main_text.print_text('Ваш счёт: ' + str(GAME.MONEY) + ' ₽', 850, 20)
        main_text.print_text('Ваш долг: ' + str(GAME.DEBT) + ' ₽', 850 , 50)
        main_text.print_text('Стоимость акций: ' + str(GAME.stocks_cost) + ' ₽', 5 , 85)
        
        screen.blit(GAME.stocks_plot.surf, (0, 116))

        btn_group_bank.update()
        btn_group_bank.draw(screen)

    elif GAME.game_mode == 'skip_a_move' and not video_background.drow_holl:
        main_text.print_text('Это был славный день ' + str(GAME.DAY), 350, 25)
        main_text.print_text('Заработано: ' + str(int(round(GAME.received_per_turn, 0))) + ' ₽', 350, 75)
        main_text.print_text('Потрачено: ' + str(int(round(GAME.spent_per_turn, 0))) + ' ₽', 350, 125)
        
        if GAME.DEBT > 0:
            main_text.print_text('Оплата кредита: ' + '1000 ₽', 350, 175)
            if GAME.received_per_turn - GAME.spent_per_turn - 1000 - 2500 < 0:
                main_text.print_text('Итог: ' + str(int(round(GAME.received_per_turn - GAME.spent_per_turn - 1000 - 2500, 0))) + ' ₽', 350, 325)
            else:
                main_text.print_text('Итог: ' + str(int(round(GAME.received_per_turn - GAME.spent_per_turn - 1000 - 2500, 0))) + ' ₽', 350, 325)
        else:
            main_text.print_text('Оплата кредита: ' + '0 ₽', 350, 175)
            
            if GAME.received_per_turn - GAME.spent_per_turn - 0 - 2500 < 0:
                main_text.print_text('Итог: ' + str(int(round(GAME.received_per_turn - GAME.spent_per_turn - 0 - 2500, 0))) + ' ₽', 350, 325)
            else:
                main_text.print_text('Итог: ' + str(int(round(GAME.received_per_turn - GAME.spent_per_turn - 0 - 2500, 0))) + ' ₽', 350, 325)

        main_text.print_text('Траты на себя: ' + '2500 ₽', 350, 225)

        main_text.print_text('Прибыль компании: ' + str(GAME.company_profit) + ' ₽', 350, 275)

        btn_group_next_move.update()
        btn_group_next_move.draw(screen)

    elif GAME.game_mode == 'shoping' and not video_background.drow_holl:
        main_text.print_text('Улучшения', 450, 25)
        main_text.print_text('Всего ОН: ' + str(GAME.SKILLS), 490, 75)

        GAME.company_profit_upgrade.draw(322, 100, font=15)
        GAME.SKILL_BONUS_upgrade.draw(322, 170, font=15)
        GAME.repair_bonus_upgrade.draw(322, 240, font=15)
        GAME.bonus_sales_upgrade.draw(322, 310, font=15)

        btn_group_repair_game.update()
        btn_group_repair_game.draw(screen)

    elif GAME.game_mode == 'show_information' and not video_background.drow_holl:
        btn_group_repair_game.update()
        btn_group_repair_game.draw(screen)

        background_image = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(background_image, (0, 0, 0, 50), (45, 5, 530, 435))

        main_text.print_text('Информация', 50, 10)
        main_text.print_text('Количество денег: ' + str(GAME.MONEY) + ' ₽', 50, 50)
        main_text.print_text('Количество Очков Навыка: ' + str(GAME.SKILLS) + '  ОН', 50, 80)
        main_text.print_text('День: ' + str(GAME.DAY + 1), 50, 110)
        main_text.print_text('Бонус починки: ' + str(GAME.repair_bonus), 50, 140)
        main_text.print_text('Бонус продажи без починки: ' + str(GAME.bonus_sales), 50, 170)
        main_text.print_text('Бонус получения Очков Навыка: ' + str(GAME.SKILL_BONUS), 50, 200)
        main_text.print_text('Кредит: ' + str(GAME.DEBT) + ' ₽', 50, 230)
        main_text.print_text('Новый кредит можно взять через : ' + str(10 - GAME.day_get_crdit) + ' дня/дней', 50, 410)
        
        if GAME.stocks:
            main_text.print_text('Акции: Куплены за ' + str(GAME.purchased_for) + ' ₽', 50, 260)
        else:
            main_text.print_text('Акции: НЕТ', 50, 260)
            
            
        main_text.print_text('Доход компании: ' + str(GAME.company_profit) + ' ₽ в день', 50, 290)
        main_text.print_text('Всего денег заработано: ' + str(GAME.total_money_earned) + ' ₽', 50, 320)
        main_text.print_text('Всего денег потрачено: ' + str(GAME.total_money_spent) + ' ₽', 50, 350)
        main_text.print_text('Всего компьютеров продано: ' + str(GAME.total_sold), 50, 380)

        screen.blit(background_image, (0, 0))


    elif GAME.game_mode == 'holl':
        if hallucination.is_real and hallucination.entity != '':
            entity_group_hallucination.update()
            entity_group_hallucination.draw(screen)

    if hallucination.is_real and hallucination.sain_veu <= 1:
        screen.blit(pygame.image.load(dir + '\\Data\\textures\\artefact.png'), (0, 0))
        hallucination.sain_veu += 1

    if screamer.is_scremming:
        screamer_group_hallucination.update()
        screamer_group_hallucination.draw(screen)

    MCT.check()
    pygame.display.update()
    fps_counter += 1
    if fps_counter == 30:
        fps_counter = 0
        if GAME.game_mode != "main-menu":
            one_second_counter += 1


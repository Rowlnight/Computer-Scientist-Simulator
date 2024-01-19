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
import widgets_for_game

import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.slider import Slider
from pygame_widgets.toggle import Toggle
from pygame_widgets.dropdown import Dropdown


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
main_font = load_data.get_fonts()

WHITE, BLACK, RED, GREEN, BLUE, YELLOW, GREY, GREY_GAME = load_data.get_colors()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
current_size = screen.get_size()
virtual_surfase = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Computer Scientist Simulator")
clock = pygame.time.Clock()

sound_1 = dir + "\\Data\\sounds\\main.mp3"
button_sound = pygame.mixer.Sound(dir + "\\Data\\sounds\\button.mp3")
fear = pygame.mixer.Sound(dir + "\\Data\\sounds\\fear.mp3")
threat_has_passed = pygame.mixer.Sound(dir + "\\Data\\sounds\\threat_has_passed.mp3")
screamer2_sound = pygame.mixer.Sound(dir + "\\Data\\sounds\\screamer2_sound.mp3")
shadow_lost = pygame.mixer.Sound(dir + "\\Data\\sounds\\shadow_lost.mp3")
mind_4 = dir + "\\Data\\sounds\\mind4.mp3"
ending_song = dir + "\\Data\\sounds\\ending_song.mp3"

sain_sound_1 = pygame.mixer.Sound(dir + "\\Data\\sounds\\sain_sound_1.mp3")
sain_sound_2 = pygame.mixer.Sound(dir + "\\Data\\sounds\\sain_sound_2.mp3")
sain_sound_3 = pygame.mixer.Sound(dir + "\\Data\\sounds\\sain_sound_3.mp3")

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
    def __init__(
        self,
        width,
        height,
        name,
        start_cost,
        rise_in_price,
        start_levl,
        improved_coefficient,
        power_of_improvement,
    ):
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

                if self.improved_coefficient == "improve_trade_slot":
                    for num, slot_data in enumerate(GAME.slots_data):
                        if slot_data == [False, False, False, None, None, None]:
                            GAME.slots_list[num].regenerated(
                                [True, False, False, None, None, None]
                            )
                            self.start_levl = self.start_levl + 1
                            self.start_cost = self.start_cost + self.rise_in_price
                            break

                elif self.improved_coefficient == "improve_SKILL_BONUS":
                    GAME.SKILL_BONUS = GAME.SKILL_BONUS + self.power_of_improvement
                    self.start_levl = self.start_levl + 1
                    GAME.SKILLS = GAME.SKILLS - self.start_cost
                    self.start_cost = self.start_cost + self.rise_in_price
                elif self.improved_coefficient == "improve_repair_bonus":
                    GAME.repair_bonus = GAME.repair_bonus + self.power_of_improvement
                    self.start_levl = self.start_levl + 1
                    GAME.SKILLS = GAME.SKILLS - self.start_cost
                    self.start_cost = self.start_cost + self.rise_in_price
                elif self.improved_coefficient == "improve_bonus_sales":
                    GAME.bonus_sales = GAME.bonus_sales + self.power_of_improvement
                    self.start_levl = self.start_levl + 1
                    GAME.SKILLS = GAME.SKILLS - self.start_cost
                    self.start_cost = self.start_cost + self.rise_in_price

        main_text.print_text(self.name, x + 23, y + 10)
        main_text.print_text(str(self.start_cost) + " ОН", x + 23, y + 30)
        main_text.print_text("Уровень: " + str(self.start_levl), x + 300, y + 30)

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

    def draw(self, x, y):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        pygame.draw.rect(screen, GREY, (x, y, self.width, self.height))
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            if (
                click[0] == 1
                and self.is_sold == 0
                and self.price <= GAME.MONEY
                and GAME.can_buy
                and MCT.CL_check
            ):
                pygame.mixer.Sound.play(GAME.buy)
                pygame.time.delay(30)

                GAME.MONEY = GAME.MONEY - self.price
                GAME.spent_per_turn = GAME.spent_per_turn + self.price
                status = random.randint(1, 100)

                GAME.download_the_product(self.name, self.price, status)

                self.is_sold = 1
                GAME.can_buy = False

        main_text.print_text(self.name, x + 23, y + 10)
        main_text.print_text(str(self.price) + " ₽", x + 23, y + 30)

        if self.is_sold:
            main_text.print_text("Продано", x + 400, y + 30)
        else:
            main_text.print_text("Не продано", x + 400, y + 30)

    def recover(self):
        self.is_sold = random.randint(0, 1)
        self.price = random.randint(self.min_price, self.max_price)
        self.name = random.choice(self.names_list)


class Hallucination(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.is_real = False
        self.is_checked = False
        self.entity = ""
        self.sain_veu = 11
        self.timer = 0

    def chenge_entity(self, entity, xy, WIDTH_HEIGHT):
        self.x = xy[0]
        self.y = xy[1]
        self.WIDTH = WIDTH_HEIGHT[0]
        self.HEIGHT = WIDTH_HEIGHT[1]
        self.entity = entity
        self.images = []
        for image in os.listdir(
            dir + "\\Data\\textures\\Hallucination_entity\\" + entity
        ):
            if "." in image:
                self.images.append(
                    pygame.image.load(
                        dir
                        + "\\Data\\textures\\Hallucination_entity\\"
                        + entity
                        + "\\"
                        + image
                    )
                )
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

        point = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(point):
            if click[0] == 1 and MCT.CL_check:
                self.is_checked = False
                self.is_real = False
                GAME.mind = GAME.mind - 10
                pygame.mixer.Sound.play(shadow_lost)
                pygame.time.delay(30)


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
        for image in os.listdir(dirrectory):
            if "." in image:
                self.images.append(pygame.image.load(dirrectory + "\\" + image))

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


class Trading_slot(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, data):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.uncorrect_input = pygame.mixer.Sound(dir + "\\Data\\sounds\\esc.mp3")
        self.correct_input = pygame.mixer.Sound(
            dir + "\\Data\\sounds\\pencil-write.mp3"
        )

        self.active = data[0]
        self.is_using = data[1]
        self.buyer = data[2]
        self.name = data[3]
        self.price = data[4]
        self.standart_price = data[5]

    def regenerated(self, data):
        self.active = data[0]
        self.is_using = data[1]
        self.buyer = data[2]
        self.name = data[3]
        self.price = data[4]
        self.standart_price = data[5]

    def draw(self, font=15):
        if self.active:
            pygame.draw.rect(screen, GREY, (self.x, self.y, self.width, self.height))
            if self.is_using:
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()

                if (
                    self.x < mouse[0] < self.x + self.width
                    and self.y < mouse[1] < self.y + self.height
                ):
                    if click[0] == 1 and MCT.CL_check:
                        if self.buyer:
                            self.confirm_the_transaction()
                            pygame.mixer.Sound.play(GAME.buy)
                            pygame.time.delay(30)
                        else:
                            GAME.chenge_price = [True, self]

                main_text.print_text(self.name, self.x + 23, self.y + 10)
                main_text.print_text(str(self.price) + " ₽", self.x + 23, self.y + 30)
                if self.buyer:
                    main_text.print_text("Есть покупатель!", self.x + 400, self.y + 30)
            else:
                main_text.print_text("Пустой слот", self.x + 23, self.y + 10)

    def dawnload_data(self, name, price):
        self.name = name
        self.price = price
        self.standart_price = self.price
        self.is_using = True

    def confirm_the_transaction(self):
        GAME.MONEY = GAME.MONEY + self.price
        GAME.received_per_turn = GAME.received_per_turn + self.price
        self.is_using = False
        self.buyer = False
        GAME.total_sold = GAME.total_sold + 1

    def recover(self, price):
        try:
            self.price = int(price)
            pygame.mixer.Sound.play(self.correct_input)
            pygame.time.delay(30)
        except:
            pygame.mixer.Sound.play(self.uncorrect_input)
            pygame.time.delay(30)
        GAME.chenge_price = [False, None]

    def generate_list(self):
        return [
            self.active,
            self.is_using,
            self.buyer,
            self.name,
            self.price,
            self.standart_price,
        ]


class Medicine:
    def __init__(self, width, height, x, y, price):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.price = price

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        pygame.draw.rect(screen, GREY, (self.x, self.y, self.width, self.height))
        if (self.x < mouse[0] < self.x + self.width
            and self.y < mouse[1] < self.y + self.height):
            if (
                click[0] == 1
                and self.price <= GAME.MONEY
                and MCT.CL_check
                and GAME.mind_stage > 1
            ):
                pygame.mixer.Sound.play(GAME.buy)
                pygame.time.delay(30)

                GAME.MONEY = GAME.MONEY - self.price
                GAME.spent_per_turn = GAME.spent_per_turn + self.price
                GAME.mind_stage = GAME.mind_stage - 1

        main_text.print_text(
            "Набор медикаментов для усиления сознания", self.x + 23, self.y + 10
        )
        main_text.print_text(str(self.price) + " ₽", self.x + 23, self.y + 30)


class Main_game_logick:
    def __init__(self):
        self.is_running = True
        self.game_mode = "main-menu"

        self.repair_fail = pygame.mixer.Sound(dir + "\\Data\\sounds\\repair_fail.mp3")
        self.buy = pygame.mixer.Sound(dir + "\\Data\\sounds\\buy.mp3")
        self.successful_repair = pygame.mixer.Sound(
            dir + "\\Data\\sounds\\successful_repair.mp3"
        )
        self.lack_of = pygame.mixer.Sound(dir + "\\Data\\sounds\\lack_of.mp3")
        self.level_up = pygame.mixer.Sound(dir + "\\Data\\sounds\\level_up.mp3")
        self.update_info = pygame.mixer.Sound(dir + "\\Data\\sounds\\update_info.mp3")

        self.core_types = []
        self.chenge_price = [False, None]

    def get_slots(self):
        trading_slot_1 = Trading_slot(500, 60, 287, 100, self.slots_data[0])
        trading_slot_2 = Trading_slot(500, 60, 287, 170, self.slots_data[1])
        trading_slot_3 = Trading_slot(500, 60, 287, 240, self.slots_data[2])
        trading_slot_4 = Trading_slot(500, 60, 287, 310, self.slots_data[3])
        trading_slot_5 = Trading_slot(500, 60, 287, 380, self.slots_data[4])
        self.slots_list = [
            trading_slot_1,
            trading_slot_2,
            trading_slot_3,
            trading_slot_4,
            trading_slot_5,
        ]

    def get_improvements(self):
        self.add_new_trading_slot = Improvements(
            430,
            60,
            "Добавить ещё один слот для продажи (максимум 5)",
            self.TRADE_SLOT_cost,
            15,
            self.TRADE_SLOT_levl,
            "improve_trade_slot",
            0,
        )

        self.SKILL_BONUS_upgrade = Improvements(
            430,
            60,
            "Улучшить прирост очков навыка",
            self.SKILL_BONUS_upgrade_cost_now,
            5,
            self.SKILL_BONUS_upgrade_levl_now,
            "improve_SKILL_BONUS",
            1,
        )

        self.repair_bonus_upgrade = Improvements(
            430,
            60,
            "Улучшить бонус починки",
            self.repair_bonus_upgrade_cost_now,
            5,
            self.repair_bonus_upgrade_levl_now,
            "improve_repair_bonus",
            0.1,
        )

        self.bonus_sales_upgrade = Improvements(
            430,
            60,
            "Улучшить бонус продажи без починки",
            self.bonus_sales_upgrade_cost_now,
            5,
            self.bonus_sales_upgrade_levl_now,
            "improve_bonus_sales",
            0.05,
        )

    def get_plot(self):
        self.stocks_plot = Plot(self.stocks_list)

    def start_new_game(self):
        [
            self.can_buy,
            self.is_repaired,
            self.old_repair_cost_PC,
            self.MONEY,
            self.DAY,
            self.SKILLS,
            self.SKILL_BONUS,
            self.current_computer_name,
            self.repair_bonus,
            self.current_computer_price,
            self.current_computer_status,
            self.bonus_sales,
            self.DEBT,
            self.stocks_cost,
            self.stocks_list,
            self.stocks,
            self.spent_per_turn,
            self.received_per_turn,
            self.day_get_crdit,
            self.total_sold,
            self.total_money_spent,
            self.total_money_earned,
            self.purchased_for,
            self.SKILL_BONUS_upgrade_cost_now,
            self.SKILL_BONUS_upgrade_levl_now,
            self.repair_bonus_upgrade_cost_now,
            self.repair_bonus_upgrade_levl_now,
            self.bonus_sales_upgrade_cost_now,
            self.bonus_sales_upgrade_levl_now,
            self.mind,
            self.slots_data,
            self.TRADE_SLOT_cost,
            self.TRADE_SLOT_levl,
            self.mind,
            self.mind_stage,
            self.mind_group,
            self.max_mind_per_minute,
            self.mind_per_minute,
            self.max_mind_on_repair,
            self.mind_on_repair,
            self.mind_on_sleep,
        ] = load_data.get_data_for_new_game()

        self.get_improvements()
        self.get_plot()
        self.get_slots()

        video_background.bg_now = dir + "\\Data\\textures\\game.mp4"
        self.game_mode = "game"

    def load_game(self):
        try:
            with open(dir + "\\Data\\Save\\save.dat", "rb") as f:
                [
                    self.can_buy,
                    self.is_repaired,
                    self.old_repair_cost_PC,
                    self.MONEY,
                    self.DAY,
                    self.SKILLS,
                    self.SKILL_BONUS,
                    self.current_computer_name,
                    self.current_computer_price,
                    self.current_computer_status,
                    self.repair_bonus,
                    self.bonus_sales,
                    self.DEBT,
                    self.stocks_cost,
                    self.stocks_list,
                    self.stocks,
                    self.spent_per_turn,
                    self.received_per_turn,
                    self.day_get_crdit,
                    self.total_sold,
                    self.total_money_spent,
                    self.total_money_earned,
                    self.purchased_for,
                    self.SKILL_BONUS_upgrade_cost_now,
                    self.SKILL_BONUS_upgrade_levl_now,
                    self.repair_bonus_upgrade_cost_now,
                    self.repair_bonus_upgrade_levl_now,
                    self.bonus_sales_upgrade_cost_now,
                    self.bonus_sales_upgrade_levl_now,
                    self.mind,
                    self.slots_data,
                    self.TRADE_SLOT_cost,
                    self.TRADE_SLOT_levl,
                    self.mind,
                    self.mind_stage,
                    self.mind_group,
                    self.max_mind_per_minute,
                    self.mind_per_minute,
                    self.max_mind_on_repair,
                    self.mind_on_repair,
                    self.mind_on_sleep,
                ] = pickle.load(f)
        except Exception as error:
            print(error)
            return

        self.get_improvements()
        self.get_plot()
        self.get_slots()

        self.add_new_trading_slot = Improvements(
            430,
            60,
            "Добавить ещё один слот для продажи (максимум 5)",
            self.TRADE_SLOT_cost,
            50,
            self.TRADE_SLOT_levl,
            "improve_trade_slot",
            10000,
        )
        self.SKILL_BONUS_upgrade = Improvements(
            430,
            60,
            "Улучшить прирост очков навыка",
            self.SKILL_BONUS_upgrade_cost_now,
            5,
            self.SKILL_BONUS_upgrade_levl_now,
            "improve_SKILL_BONUS",
            1,
        )
        self.repair_bonus_upgrade = Improvements(
            430,
            60,
            "Улучшить бонус починки",
            self.repair_bonus_upgrade_cost_now,
            5,
            self.repair_bonus_upgrade_levl_now,
            "improve_repair_bonus",
            0.1,
        )
        self.bonus_sales_upgrade = Improvements(
            430,
            60,
            "Улучшить бонус продажи без починки",
            self.bonus_sales_upgrade_cost_now,
            5,
            self.bonus_sales_upgrade_levl_now,
            "improve_bonus_sales",
            0.05,
        )

        if self.mind_stage == 4:
            pygame.mixer.music.unload()
            pygame.mixer.music.load(mind_4)
            pygame.mixer.music.play(loops=-1)

        video_background.bg_now = dir + "\\Data\\textures\\game.mp4"
        self.game_mode = "game"

    def save_game(self):
        SKILL_BONUS_upgrade_cost_now = self.SKILL_BONUS_upgrade.get_cost()
        SKILL_BONUS_upgrade_levl_now = self.SKILL_BONUS_upgrade.get_levl()
        repair_bonus_upgrade_cost_now = self.repair_bonus_upgrade.get_cost()
        repair_bonus_upgrade_levl_now = self.repair_bonus_upgrade.get_levl()
        bonus_sales_upgrade_cost_now = self.bonus_sales_upgrade.get_cost()
        bonus_sales_upgrade_levl_now = self.bonus_sales_upgrade.get_levl()

        self.slots_data = []
        for slot in self.slots_list:
            self.slots_data.append(slot.generate_list())

        with open(dir + "\\Data\\Save\\save.dat", "wb") as f:
            pickle.dump(
                [
                    self.can_buy,
                    self.is_repaired,
                    self.old_repair_cost_PC,
                    self.MONEY,
                    self.DAY,
                    self.SKILLS,
                    self.SKILL_BONUS,
                    self.current_computer_name,
                    self.current_computer_price,
                    self.current_computer_status,
                    self.repair_bonus,
                    self.bonus_sales,
                    self.DEBT,
                    self.stocks_cost,
                    self.stocks_list,
                    self.stocks,
                    self.spent_per_turn,
                    self.received_per_turn,
                    self.day_get_crdit,
                    self.total_sold,
                    self.total_money_spent,
                    self.total_money_earned,
                    self.purchased_for,
                    SKILL_BONUS_upgrade_cost_now,
                    SKILL_BONUS_upgrade_levl_now,
                    repair_bonus_upgrade_cost_now,
                    repair_bonus_upgrade_levl_now,
                    bonus_sales_upgrade_cost_now,
                    bonus_sales_upgrade_levl_now,
                    self.mind,
                    self.slots_data,
                    self.add_new_trading_slot.start_cost,
                    self.add_new_trading_slot.start_levl,
                    self.mind,
                    self.mind_stage,
                    self.mind_group,
                    self.max_mind_per_minute,
                    self.mind_per_minute,
                    self.max_mind_on_repair,
                    self.mind_on_repair,
                    self.mind_on_sleep,
                ],
                f,
            )

    def return_to_main_menu(self):
        self.save_game()
        video_background.bg_now = dir + "\\Data\\textures\\main_menu.mp4"
        self.game_mode = "main-menu"
        video_background.draw_game_menu = False

    def exit_game(self):
        self.is_running = False

    def go_back(self):
        video_background.bg_now = dir + "\\Data\\textures\\game.mp4"
        self.game_mode = "game"

    ##################################################################------------------Функции Рабочего стола
    def show_pharmacy(self):
        video_background.bg_now = dir + "\\Data\\textures\\activity.mp4"
        self.game_mode = "pharmacy"

    def shoping(self):
        video_background.bg_now = dir + "\\Data\\textures\\activity.mp4"
        self.game_mode = "shoping"

    def taxes(self):
        video_background.bg_now = dir + "\\Data\\textures\\bank.mp4"
        self.game_mode = "bank"

    def skip_a_move(self):
        self.DAY = self.DAY + 1
        self.MONEY = self.MONEY - 800

        standart_product_1.recover()
        standart_product_2.recover()
        standart_product_3.recover()
        standart_product_4.recover()
        standart_product_5.recover()
        standart_product_6.recover()
        standart_product_7.recover()

        for slot in self.slots_list:
            if slot.active and slot.is_using:
                difference = slot.price - slot.standart_price
                if difference <= 0:
                    slot.buyer = True
                else:
                    print(difference // 1000)
                    if random.randint(0, difference // 1000) == 0:
                        slot.buyer = True

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
        if self.DEBT > 0:
            self.total_money_spent = (
                self.total_money_spent + self.spent_per_turn + 2500 + 1000
            )
        else:
            self.total_money_spent = self.total_money_spent + self.spent_per_turn + 2500

        self.game_mode = "skip_a_move"
        video_background.bg_now = dir + "\\Data\\textures\\pause.mp4"

        self.save_game()

    def completion_of_the_skip_a_move(self):
        if self.DEBT == 0:
            self.game_mode = "end"
            video_background.bg_now = dir + "\\Data\\textures\\end.mp4"
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.unload()
            pygame.mixer.music.load(ending_song)
            pygame.mixer.music.play(loops=-1)
        else:
            self.spent_per_turn = 0
            self.received_per_turn = 0

            self.add_mind(800)
            self.day_mind_control()

            self.game_mode = "game"
            video_background.bg_now = dir + "\\Data\\textures\\game.mp4"

    def trade(self):
        video_background.bg_now = dir + "\\Data\\textures\\pause.mp4"
        self.game_mode = "trade"

    def warehouse(self):
        video_background.bg_now = dir + "\\Data\\textures\\activity.mp4"
        self.game_mode = "warehouse"

    def repair_pc(self):
        video_background.bg_now = dir + "\\Data\\textures\\workshop.mp4"
        self.game_mode = "repair_pc"
        already_analyzed = True

    ##################################################################------------------Функции мастерской-починки
    def download_the_product(self, name, price, status):
        self.current_computer_name = name
        self.current_computer_price = price
        self.current_computer_status = status
        self.repair_cost_PC = price * (100 - status) // 100

        self.core = random.choice(self.core_types).split()[0]
        self.firmware_version_max = random.randint(2, 99)
        self.firmware_version_min = random.randint(1, self.firmware_version_max)

        self.firmware_version = (
            f"Пролайн версия: {self.firmware_version_min} - {self.firmware_version_max}"
        )
        self.performance_factor = random.randint(
            self.firmware_version_min, self.firmware_version_max
        )
        self.performance_factor_PC = round(
            (self.firmware_version_min + self.firmware_version_max)
            / self.performance_factor,
            3,
        )

    def sale(self):
        is_success = False
        for slot in self.slots_list:
            if slot.active and not slot.is_using:
                if self.current_computer_status == 0:
                    slot.dawnload_data(
                        self.current_computer_name, self.current_computer_price
                    )
                else:
                    slot.dawnload_data(
                        self.current_computer_name,
                        self.current_computer_price
                        + (self.current_computer_price * self.bonus_sales),
                    )
                is_success = True
                break

        if is_success:
            self.can_buy = True
            self.is_repaired = False
            self.already_analyzed = False
            pygame.mixer.Sound.play(self.buy)
            pygame.time.delay(30)

    def repair_start(self, data):
        repair_widgets, slots_widgets = data
        video_background.bg_now = dir + "\\Data\\textures\\workshop.mp4"
        self.game_mode = "repair_pc"
        for widget in slots_widgets:
            widget.hide()
        for widget in repair_widgets:
            widget.show()

    def get_core(self):
        for core in self.core_types:
            if self.core in core:
                return core

    def repair_finish(self, arg):
        video_background.bg_now = dir + "\\Data\\textures\\activity.mp4"
        self.game_mode = "warehouse"
        if arg:
            core_info = self.get_core()

            try:
                Software = int(textbox_2.getText())
                min_Software = int(output_1.getText())
                max_Software = int(output_2.getText())
                cost_of_the_cooling_system = int(dropdown.getSelected().split()[1])
                cooling_temperature = int(dropdown.getSelected().split()[0])
                maximum_core_temperature = int(core_info.split()[1])
                if core_info.split()[2] == "True":
                    is_improved = True
                else:
                    is_improved = False

                if (
                    toggle.getValue() == is_improved
                    and (cooling_temperature <= maximum_core_temperature)
                    and (max_Software == self.firmware_version_max)
                    and (min_Software == self.firmware_version_min)
                    and (Software >= min_Software)
                    and (Software <= self.firmware_version_max)
                    and (Software == self.performance_factor)
                    and (self.MONEY >= cost_of_the_cooling_system)
                ):

                    self.MONEY = self.MONEY - cost_of_the_cooling_system
                    self.spent_per_turn = (
                        self.spent_per_turn + cost_of_the_cooling_system
                    )

                    self.current_computer_price = (
                        self.current_computer_price
                        + 3000
                        + (self.current_computer_price * self.repair_bonus)
                        + (
                            (self.current_computer_price // 1000)
                            * self.current_computer_status
                        )
                    )
                    self.current_computer_status = 0

                    self.SKILLS = self.SKILLS + random.randint(0, self.SKILL_BONUS)

                    pygame.mixer.Sound.play(self.successful_repair)
                    pygame.time.delay(30)

                else:
                    pygame.mixer.Sound.play(self.lack_of)
                    pygame.time.delay(30)
            except Exception as error:
                pygame.mixer.Sound.play(self.lack_of)
                pygame.time.delay(30)
                print(error)
        else:
            pass

    def show_info(self):
        self.game_mode = "show_information_about_cores"

    def close_info(self):
        self.game_mode = "repair_pc"

    ##################################################################------------------Функции Банка
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
                self.received_per_turn = self.received_per_turn + num + 1000
            else:
                self.DEBT = self.DEBT + num + 5000
                self.day_get_crdit = 0
                self.received_per_turn = self.received_per_turn + num + 5000

            pygame.mixer.Sound.play(self.buy)
            pygame.time.delay(30)

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

    ##################################################################------------------Функции воего магазина
    def open_shop(self, data):
        repair_widgets, slots_widgets = data
        video_background.bg_now = dir + "\\Data\\textures\\workshop.mp4"
        self.game_mode = "slots"
        for widget in slots_widgets:
            widget.show()
        for widget in repair_widgets:
            widget.hide()

    def clear_chenges_slot(self):
        self.chenge_price = [False, None]

    def applay_slot(self, text_class):
        self.chenge_price[1].recover(text_class.getText())

    ##################################################################------------------Функции Сознания
    def add_mind(
        self, mind, mind_group=None
    ):  # добавление разума в глобальный или mind_group счетчик
        if mind_group is None:
            self.mind += mind
        else:
            if (
                mind < self.mind_group[mind_group][1]
            ):  # 1 - разум сейчас; 2 - максимальный разум
                if (
                    mind + self.mind_group[mind_group][0]
                    < self.mind_group[mind_group][1]
                ):
                    self.mind_group[mind_group][0] += mind
                else:
                    self.mind_group[mind_group][0] = self.mind_group[mind_group][1]
        print("added mind")

    def day_mind_control(self):  # изменение разума при окончании дня
        self.add_mind(self.mind_on_sleep)
        for i in self.mind_group.items():
            self.mind += i[1][1]
            self.mind_group[i[0]][1] = 0

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

    ##################################################################------------------Показать статистику
    def show_information(self):
        video_background.bg_now = dir + "\\Data\\textures\\info_bg.mp4"
        self.game_mode = "show_information"

    ##################################################################------------------Выход
    def exit_game(self):
        self.is_running = False


class Background:
    def __init__(self):
        self.bg_now = dir + "\\Data\\textures\\main_menu.mp4"
        self.bg = dir + "\\Data\\textures\\main_menu.mp4"
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
                video_image.tobytes(), video_image.shape[1::-1], "BGR"
            )
        else:
            self.main_menu_bg = cv2.VideoCapture(self.bg_now)
        screen.blit(self.video_surf, (0, 0))


##################################################################------------------Вспомогательные функции игрового цикла
def every_second_function():
    if (
        GAME.game_mode != "main-menu"
        and GAME.game_mode != "skip_a_move"
        and GAME.DAY != 0
        and GAME.game_mode != "holl"
        and GAME.game_mode != "end"
    ):
        if not hallucination.is_real:
            if GAME.mind_stage == 1:
                entyty_show = random.randint(1, 60)
            elif GAME.mind_stage == 2:
                entyty_show = random.randint(1, 45)
            elif GAME.mind_stage == 3:
                entyty_show = random.randint(1, 30)
            elif GAME.mind_stage == 4:
                entyty_show = random.randint(1, 15)

            if entyty_show == 1:
                entity = random.choice(["gallows", "shadow"])
                if entity == "gallows":
                    place = [random.randint(50, 900), 250]
                    form = [100, 400]
                elif entity == "shadow":
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

    if hallucination.is_real:
        hallucination.timer += 1
        if hallucination.timer == 7 * (5 - GAME.mind_stage):
            screamer.chenge_screamer(
                screamer2_sound, dir + "\\Data\\textures\\screamer\\gat"
            )
            hallucination.timer = 0


def control_point():
    GAME.load_game()
    hallucination.is_checked = False
    hallucination.is_real = False
    video_background.drow_holl = False
    GAME.game_mode = "skip_a_move"
    video_background.bg_now = dir + "\\Data\\textures\\pause.mp4"


GAME = Main_game_logick()
video_background = Background()
hallucination = Hallucination()
screamer = Screamer([0, 0], [1074, 654], control_point)

main_text = Text(font_color=WHITE, font_tipe=main_font, font_size=17)
global_text = Text(font_color=WHITE, font_tipe=main_font, font_size=40)
big_text = Text(font_color=WHITE, font_tipe=main_font, font_size=25)
global_black_text = Text(font_color=BLACK, font_tipe=main_font, font_size=40)

# ---------------------------------------------------Инициализация виджетов
(
    core_types,
    dropdown,
    textbox_2,
    slider_1,
    slider_2,
    output_1,
    output_2,
    toggle,
) = widgets_for_game.get_widgets(screen)
repair_widgets = [dropdown, textbox_2, slider_1, slider_2, output_1, output_2, toggle]

textbox_input_new_price = widgets_for_game.get_widgets_for_slots(screen)
slots_widgets = [textbox_input_new_price]
GAME.core_types = core_types

# ---------------------------------------------------Инициализация кнопок
# -------------------------главное меню
play_btn = Button(
    dir + "\\Data\\textures\\buttons\\menu_btn",
    xy=[center_WIDTH, 200],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Играть", WHITE],
    target=GAME.start_new_game,
)
load_btn = Button(
    dir + "\\Data\\textures\\buttons\\menu_btn",
    xy=[center_WIDTH, 300],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Загрузить", WHITE],
    target=GAME.load_game,
)
out_btn = Button(
    dir + "\\Data\\textures\\buttons\\menu_btn",
    xy=[center_WIDTH, 450],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Выйти", WHITE],
    target=GAME.exit_game,
)
btn_group_main_menu = pygame.sprite.Group(play_btn, load_btn, out_btn)
# -------------------------Меню паузы
save_and_exit_btn = Button(
    dir + "\\Data\\textures\\buttons\\menu_btn",
    xy=[center_WIDTH, 200],
    WIDTH_HEIGHT=[300, 60],
    sound=button_sound,
    text=["Сохранить и выйти", WHITE],
    target=GAME.return_to_main_menu,
)
btn_group_game_menu = pygame.sprite.Group(save_and_exit_btn)
# -------------------------Рабочий стол
game_shop_btn = Button(
    dir + "\\Data\\textures\\buttons\\researches",
    xy=[50, 50],
    WIDTH_HEIGHT=[50, 50],
    sound=button_sound,
    text=["", WHITE],
    target=GAME.shoping,
)
game_bank_btn = Button(
    dir + "\\Data\\textures\\buttons\\bank",
    xy=[50, 120],
    WIDTH_HEIGHT=[50, 50],
    sound=button_sound,
    text=["", WHITE],
    target=GAME.taxes,
)
game_move_btn = Button(
    dir + "\\Data\\textures\\buttons\\move",
    xy=[1001, 600],
    WIDTH_HEIGHT=[50, 50],
    sound=button_sound,
    text=["", WHITE],
    target=GAME.skip_a_move,
)
game_trading_btn = Button(
    dir + "\\Data\\textures\\buttons\\trading",
    xy=[50, 400],
    WIDTH_HEIGHT=[50, 50],
    sound=button_sound,
    text=["", WHITE],
    target=GAME.trade,
)
game_home_btn = Button(
    dir + "\\Data\\textures\\buttons\\home",
    xy=[50, 260],
    WIDTH_HEIGHT=[50, 50],
    sound=button_sound,
    text=["", WHITE],
    target=GAME.warehouse,
)
game_self_shop_btn = Button(
    dir + "\\Data\\textures\\buttons\\shop",
    xy=[50, 330],
    WIDTH_HEIGHT=[50, 50],
    sound=button_sound,
    text=["", WHITE],
    target=GAME.open_shop,
    arg=[repair_widgets, slots_widgets],
)
game_info_btn = Button(
    dir + "\\Data\\textures\\buttons\\info",
    xy=[1001, 530],
    WIDTH_HEIGHT=[50, 50],
    sound=button_sound,
    text=["", WHITE],
    target=GAME.show_information,
)
game_pharmacy_btn = Button(
    dir + "\\Data\\textures\\buttons\\pharmacy",
    xy=[50, 190],
    WIDTH_HEIGHT=[50, 50],
    sound=button_sound,
    text=["", WHITE],
    target=GAME.show_pharmacy,
)
btn_group_game_table = pygame.sprite.Group(
    game_shop_btn,
    game_bank_btn,
    game_move_btn,
    game_trading_btn,
    game_home_btn,
    game_info_btn,
    game_self_shop_btn,
    game_pharmacy_btn,
)
# -------------------------Покупка
game_trade_btn = Button(
    dir + "\\Data\\textures\\buttons\\EUG_button",
    xy=[950, 600],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Назад", WHITE],
    target=GAME.go_back,
)
btn_group_trade = pygame.sprite.Group(game_trade_btn)
# -------------------------Мастерская
game_repair_btn = Button(
    dir + "\\Data\\textures\\buttons\\EUG_button",
    xy=[100, 600],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Починить", WHITE],
    target=GAME.repair_start,
    arg=[repair_widgets, slots_widgets],
)
game_sale_btn = Button(
    dir + "\\Data\\textures\\buttons\\EUG_button",
    xy=[300, 600],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Продать", WHITE],
    target=GAME.sale,
)
btn_group_repair_1 = pygame.sprite.Group(game_trade_btn)
btn_group_repair_2 = pygame.sprite.Group(game_repair_btn, game_sale_btn)
# -------------------------Починка
repair_btn = Button(
    dir + "\\Data\\textures\\buttons\\EUG_button",
    xy=[900, 600],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Починить", WHITE],
    target=GAME.repair_finish,
    arg=True,
)
game_repair_exit_btn = Button(
    dir + "\\Data\\textures\\buttons\\EUG_button",
    xy=[100, 600],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Отмена", WHITE],
    target=GAME.repair_finish,
    arg=False,
)
game_repair_info_show_btn = Button(
    dir + "\\Data\\textures\\buttons\\EUG_button",
    xy=[300, 600],
    WIDTH_HEIGHT=[220, 60],
    sound=button_sound,
    text=["Информация", WHITE],
    target=GAME.show_info,
)
btn_group_repair_game = pygame.sprite.Group(
    game_repair_exit_btn, repair_btn, game_repair_info_show_btn
)
# -------------------------Информация о починке
game_trade_repair_info_btn = Button(
    dir + "\\Data\\textures\\buttons\\EUG_button",
    xy=[950, 600],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Назад", WHITE],
    target=GAME.close_info,
)
btn_group_repair_info = pygame.sprite.Group(game_trade_repair_info_btn)
# -------------------------Свой магазин
btn_group_slots = pygame.sprite.Group(game_trade_btn)
game_slot_cancellation_btn = Button(
    dir + "\\Data\\textures\\buttons\\EUG_button",
    xy=[950, 600],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Отмена", WHITE],
    target=GAME.clear_chenges_slot,
)
game_slot_applay_btn = Button(
    dir + "\\Data\\textures\\buttons\\EUG_button",
    xy=[300, 600],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Готово", WHITE],
    target=GAME.applay_slot,
    arg=textbox_input_new_price,
)
btn_group_slots_chenge = pygame.sprite.Group(
    game_slot_cancellation_btn, game_slot_applay_btn
)
# -------------------------Банк
game_bank_exit_btn = Button(
    dir + "\\Data\\textures\\buttons\\bank_operations_btn",
    xy=[950, 600],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Назад", WHITE],
    target=GAME.go_back,
)
game_bank_get_10k_btn = Button(
    dir + "\\Data\\textures\\buttons\\bank_operations_btn",
    xy=[840, 150],
    WIDTH_HEIGHT=[450, 60],
    sound=button_sound,
    text=["Взять в кредит 10k", WHITE],
    target=GAME.pay_off,
    arg=10000,
)
game_bank_get_1k_btn = Button(
    dir + "\\Data\\textures\\buttons\\bank_operations_btn",
    xy=[840, 220],
    WIDTH_HEIGHT=[450, 60],
    sound=button_sound,
    text=["Взять в кредит 1k", WHITE],
    target=GAME.pay_off,
    arg=1000,
)
game_bank_get_stocks_btn = Button(
    dir + "\\Data\\textures\\buttons\\bank_operations_btn",
    xy=[125, 550],
    WIDTH_HEIGHT=[250, 60],
    sound=button_sound,
    text=["Купить акции", WHITE],
    target=GAME.by_stocks,
)
game_bank_sale_stocks_btn = Button(
    dir + "\\Data\\textures\\buttons\\bank_operations_btn",
    xy=[478, 550],
    WIDTH_HEIGHT=[250, 60],
    sound=button_sound,
    text=["Продать акции", WHITE],
    target=GAME.sale_stocks,
)
game_bank_pay_debt_1k_btn = Button(
    dir + "\\Data\\textures\\buttons\\bank_operations_btn",
    xy=[840, 360],
    WIDTH_HEIGHT=[450, 60],
    sound=button_sound,
    text=["Оплатить 1K", WHITE],
    target=GAME.pay_debt,
    arg=1000,
)
game_bank_pay_debt_10k_btn = Button(
    dir + "\\Data\\textures\\buttons\\bank_operations_btn",
    xy=[840, 290],
    WIDTH_HEIGHT=[450, 60],
    sound=button_sound,
    text=["Оплатить 10K", WHITE],
    target=GAME.pay_debt,
    arg=10000,
)
btn_group_bank = pygame.sprite.Group(
    game_bank_exit_btn,
    game_bank_get_10k_btn,
    game_bank_get_1k_btn,
    game_bank_get_stocks_btn,
    game_bank_sale_stocks_btn,
    game_bank_pay_debt_1k_btn,
    game_bank_pay_debt_10k_btn,
)
# -------------------------СЛЕД. ход
game_next_move = Button(
    dir + "\\Data\\textures\\buttons\\menu_btn",
    xy=[900, 600],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Продолжить", WHITE],
    target=GAME.completion_of_the_skip_a_move,
)
game_exit = Button(
    dir + "\\Data\\textures\\buttons\\menu_btn",
    xy=[174, 600],
    WIDTH_HEIGHT=[180, 60],
    sound=button_sound,
    text=["Выйти из игры", WHITE],
    target=GAME.exit_game,
)
btn_group_next_move = pygame.sprite.Group(game_next_move, game_exit)
# -------------------------Конец
game_last_exit = Button(
    dir + "\\Data\\textures\\buttons\\EUG_button",
    xy=[537, 600],
    WIDTH_HEIGHT=[1000, 60],
    sound=button_sound,
    text=["Покинуть этот мир", WHITE],
    target=GAME.exit_game,
)
last_btn_group = pygame.sprite.Group(game_last_exit)

# ---------------------------------------Создание товаров
standart_product_1 = Product(
    500,
    60,
    60000,
    300000,
    ["Игровой_пк", "Что-то_для_игр", "Пк_для_геймеров", "Пк_для_любителей_игр"],
)
standart_product_2 = Product(
    500,
    60,
    10000,
    29000,
    [
        "Старый_пк",
        "Допотопный_пк",
        "Офисный_компьютер",
        "Старый_ноут",
        "Разобранный_пк",
    ],
)
standart_product_3 = Product(
    500,
    60,
    1000,
    10000,
    [
        "Сломанный_пк",
        "Ненужный_компьютер",
        "Компьютер(много_зависает)",
        "ПК_на_металлолом",
    ],
)
standart_product_4 = Product(
    500,
    60,
    30000,
    80000,
    ["Обычный_компьютер", "Домашний_пк", "Новый_компьютер", "Компьютер_для_всей_семьи"],
)
standart_product_5 = Product(
    500,
    60,
    15000,
    35000,
    [
        "Ноутбук",
        "ЭВМ",
        "Шайтан-машина(лють_вообще:)",
        "Серверный_блок",
        "Мини-компьютер",
        "Бесшумный_ПК",
        "Школьный_компьютер",
        "Крутой_пк",
        "Стационарный_компьютер",
    ],
)
standart_product_6 = Product(
    500,
    60,
    1000,
    54000,
    [
        "Cовременный_пк",
        "Миниатюрный_компьютер",
        "Универсальный_ПК",
        "Ручной_компьютер",
        "Базовый_пк",
    ],
)
standart_product_7 = Product(
    500,
    60,
    300000,
    1000000,
    [
        "Квантовый_ПК",
        "Навигационный_компьютер",
        "Биологический_компьютер",
        "Боевой_компьютер",
    ],
)
standart_product_1.recover()
standart_product_2.recover()
standart_product_3.recover()
standart_product_4.recover()
standart_product_5.recover()
standart_product_6.recover()
standart_product_7.recover()

# ---------------------------------------Создание Лекарств
medicine = Medicine(500, 60, 287, 100, 10000)

# ------------------------------------Монстр
entity_group_hallucination = pygame.sprite.Group(hallucination)
screamer_group_hallucination = pygame.sprite.Group(screamer)

one_second_counter = 0

while GAME.is_running:
    if one_second_counter == 30:
        one_second_counter = 0
        every_second_function()
    events = pygame.event.get()
    clock.tick(FPS)

    video_background.drow_background()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            GAME.is_running = False

        elif (
            event.type == pygame.KEYDOWN
            and GAME.game_mode != "main-menu"
            and GAME.game_mode != "skip_a_move"
            and GAME.game_mode != "end"
        ):
            if event.key == pygame.K_SPACE:
                if not video_background.drow_holl:
                    video_background.drow_holl = True
                    bg_remowed = video_background.bg_now
                    game_mode_remowed = GAME.game_mode
                    GAME.game_mode = "holl"
                    video_background.bg_now = dir + "\\Data\\textures\\holl.mp4"

                    if hallucination.is_real and not hallucination.is_checked:
                        hallucination.is_checked = True
                        pygame.mixer.Sound.play(fear)
                        pygame.time.delay(30)
                        hallucination.timer = 5
                    elif not hallucination.is_real and not hallucination.is_checked:
                        pygame.mixer.Sound.play(threat_has_passed)
                        pygame.time.delay(30)
                else:
                    video_background.drow_holl = False
                    video_background.bg_now = bg_remowed
                    GAME.game_mode = game_mode_remowed

    if GAME.game_mode == "main-menu" and not video_background.drow_holl:
        global_text.print_text("Computer Scientist Simulator", 310, 50)
        btn_group_main_menu.update()
        btn_group_main_menu.draw(screen)

    elif GAME.game_mode == "game" and not video_background.drow_holl:
        main_text.print_text("День: " + str(GAME.DAY + 1), 850, 40)
        main_text.print_text("Сознание: " + str(GAME.mind_stage), 850, 60)
        btn_group_game_table.update()
        btn_group_game_table.draw(screen)

    elif GAME.game_mode == "trade" and not video_background.drow_holl:
        global_text.print_text("Сегодня в продаже", 380, 25)

        standart_product_1.draw(287, 100)
        standart_product_2.draw(287, 170)
        standart_product_3.draw(287, 240)
        standart_product_4.draw(287, 310)
        standart_product_5.draw(287, 380)
        standart_product_6.draw(287, 450)
        standart_product_7.draw(287, 520)

        btn_group_trade.update()
        btn_group_trade.draw(screen)

    elif GAME.game_mode == "warehouse" and not video_background.drow_holl:
        btn_group_repair_1.update()
        btn_group_repair_1.draw(screen)
        if not GAME.can_buy:
            main_text.print_text(
                f"В наличии компьютер: {GAME.current_computer_name}", 50, 50
            )
            main_text.print_text(f"Цена: {GAME.current_computer_price}₽", 50, 100)
            main_text.print_text(
                f"Поломки: {str(GAME.current_computer_status)}%", 50, 150
            )

            btn_group_repair_2.update()
            btn_group_repair_2.draw(screen)

    elif GAME.game_mode == "repair_pc" and not video_background.drow_holl:
        main_text.print_text("Минимальная версия: ", 650, 260)
        main_text.print_text("Максимальная версия: ", 650, 310)
        main_text.print_text("Дополнительная информация о ПК:", 50, 260)
        main_text.print_text("Улучшенное ядро", 50, 180)
        main_text.print_text("Ядро: " + GAME.core, 50, 310)
        main_text.print_text("Версия ПО: " + GAME.firmware_version, 50, 360)
        main_text.print_text("КП ПО: " + str(GAME.performance_factor_PC), 50, 410)
        main_text.print_text("Итоговая версия ПО:", 350, 150)
        main_text.print_text("Система охлаждения:", 650, 150)
        main_text.print_text("Итоговая версия ПО: " + textbox_2.getText(), 650, 360)

        try:
            temporary_performance_factor = (
                int(output_1.getText()) + int(output_2.getText())
            ) / int(textbox_2.getText())
            temporary_performance_factor = round(temporary_performance_factor, 3)
            main_text.print_text(
                "Итоговый КП ПО: " + str(temporary_performance_factor), 650, 410
            )
        except:
            main_text.print_text("Итоговый КП ПО: Н/В", 650, 410)

        output_1.setText(slider_1.getValue())
        output_2.setText(slider_2.getValue())
        btn_group_repair_game.update()
        btn_group_repair_game.draw(screen)

        pygame_widgets.update(events)

    elif (
        GAME.game_mode == "show_information_about_cores"
        and not video_background.drow_holl
    ):
        main_text.print_text("Ядра", 50, 10)
        main_text.print_text("1 -  46B1zdG0IG - МТ(60°C),  тип:  обычный", 50, 50)
        main_text.print_text("2 -  7Vio85Hf3s - МТ(89°C),  тип:  улучшенный", 50, 80)
        main_text.print_text("3 -  690UTBht4a - МТ(50°C),  тип:  обычный", 50, 110)
        main_text.print_text("4 -  xQP34iZ9b5 - МТ(100°C), тип:  улучшенный", 50, 140)
        main_text.print_text("5 -  D1a584cuyJ - МТ(65°C),  тип:  улучшенный", 50, 170)
        main_text.print_text("6 -  566KhI4oiq - МТ(78°C),  тип:  обычный", 50, 200)
        main_text.print_text("7 -  I2GW-Z83Fp - МТ(120°C), тип:  улучшенный", 50, 230)
        main_text.print_text("8 -  B-Tyv-QX7J - МТ(97°C),  тип:  улучшенный", 50, 260)
        main_text.print_text("9 -  Ivf-E_Xi0C - МТ(40°C),  тип:  улучшенный", 50, 290)
        main_text.print_text("10 - mKlAG-0eCD - МТ(74°C),  тип:  обычный", 50, 320)
        main_text.print_text("11 - wN-wXl5JzD - МТ(80°C),  тип:  обычный", 50, 350)
        main_text.print_text("12 - 4K-i9bkVh8 - МТ(59°C),  тип:  улучшенный", 50, 380)
        main_text.print_text("13 - I_Hp1wBmE1 - МТ(57°C),  тип:  улучшенный", 50, 410)

        main_text.print_text("Системы охлаждения", 587, 10)
        main_text.print_text("1 - v-u16metqa - МО(30°C), 5000₽", 587, 50)
        main_text.print_text("2 - v0-na8hoxk - МО(40°C), 4500₽", 587, 80)
        main_text.print_text("3 - i5x9-eziux - МО(60°C), 3000₽", 587, 110)
        main_text.print_text("4 - ke_urm_9l9 - МО(80°C), 1500₽", 587, 140)
        main_text.print_text("5 - 64ae62om-n - МО(100°C), 500₽", 587, 170)
        main_text.print_text("6 - c4-om4xmat - МО(54°C), 3500₽", 587, 200)
        main_text.print_text("7 - UIc0-vkftF - МО(70°C), 2000₽", 587, 230)
        main_text.print_text("8 - b9-jg6q2jV - МО(75°C), 1768₽", 587, 260)

        btn_group_repair_info.update()
        btn_group_repair_info.draw(screen)

    elif GAME.game_mode == "bank" and not video_background.drow_holl:
        global_text.print_text("Банк", center_WIDTH, 20)
        main_text.print_text("Ваш долг: " + str(GAME.DEBT) + " ₽", 850, 50)
        main_text.print_text("Стоимость акций: " + str(GAME.stocks_cost) + " ₽", 5, 85)

        screen.blit(GAME.stocks_plot.surf, (0, 116))

        btn_group_bank.update()
        btn_group_bank.draw(screen)

    elif GAME.game_mode == "skip_a_move" and not video_background.drow_holl:
        global_text.print_text("Это был славный день: " + str(GAME.DAY), 350, 25)
        big_text.print_text(
            "Заработано: " + str(int(round(GAME.received_per_turn, 0))) + " ₽", 350, 75
        )
        big_text.print_text(
            "Потрачено: " + str(int(round(GAME.spent_per_turn, 0))) + " ₽", 350, 125
        )
        big_text.print_text(
            "Итог: "
            + str(int(round(GAME.received_per_turn - GAME.spent_per_turn - 800, 0)))
            + " ₽",
            350,
            225,
        )
        big_text.print_text("Траты на себя: 800 ₽", 350, 175)

        btn_group_next_move.update()
        btn_group_next_move.draw(screen)

    elif GAME.game_mode == "shoping" and not video_background.drow_holl:
        main_text.print_text("Улучшения", 450, 25)
        main_text.print_text("Всего ОН: " + str(GAME.SKILLS), 490, 75)

        GAME.add_new_trading_slot.draw(322, 100, font=15)
        GAME.SKILL_BONUS_upgrade.draw(322, 170, font=15)
        GAME.repair_bonus_upgrade.draw(322, 240, font=15)
        GAME.bonus_sales_upgrade.draw(322, 310, font=15)

        btn_group_trade.update()
        btn_group_trade.draw(screen)

    elif GAME.game_mode == "show_information" and not video_background.drow_holl:
        btn_group_trade.update()
        btn_group_trade.draw(screen)

        global_text.print_text("Информация", 50, 10)
        main_text.print_text("Количество денег: " + str(GAME.MONEY) + " ₽", 50, 80)
        main_text.print_text(
            "Количество Очков Навыка: " + str(GAME.SKILLS) + "  ОН", 50, 110
        )
        main_text.print_text("День: " + str(GAME.DAY + 1), 50, 140)
        main_text.print_text("Бонус починки: " + str(GAME.repair_bonus), 50, 170)
        main_text.print_text(
            "Бонус продажи без починки: " + str(GAME.bonus_sales), 50, 200
        )
        main_text.print_text(
            "Бонус получения Очков Навыка: " + str(GAME.SKILL_BONUS), 50, 230
        )
        main_text.print_text("Кредит: " + str(GAME.DEBT) + " ₽", 50, 410)
        main_text.print_text(
            "Новый кредит можно взять через : "
            + str(10 - GAME.day_get_crdit)
            + " дня/дней",
            50,
            260,
        )
        if GAME.stocks:
            main_text.print_text(
                "Акции: Куплены за " + str(GAME.purchased_for) + " ₽", 50, 290
            )
        else:
            main_text.print_text("Акции: НЕТ", 50, 290)
        main_text.print_text(
            "Всего денег заработано: " + str(GAME.total_money_earned) + " ₽", 50, 320
        )
        main_text.print_text(
            "Всего денег потрачено: " + str(GAME.total_money_spent) + " ₽", 50, 350
        )
        main_text.print_text(
            "Всего компьютеров продано: " + str(GAME.total_sold), 50, 380
        )

    elif GAME.game_mode == "slots" and not video_background.drow_holl:
        global_text.print_text("Ваш магазин", 450, 25)

        if GAME.chenge_price[0]:
            btn_group_slots_chenge.update()
            btn_group_slots_chenge.draw(screen)
            pygame_widgets.update(events)
        else:
            btn_group_slots.update()
            btn_group_slots.draw(screen)
            for slot in GAME.slots_list:
                slot.draw()

    elif GAME.game_mode == "pharmacy" and not video_background.drow_holl:
        btn_group_trade.update()
        btn_group_trade.draw(screen)
        medicine.draw()

    elif GAME.game_mode == "holl":
        if hallucination.is_real and hallucination.entity != "":
            entity_group_hallucination.update()
            entity_group_hallucination.draw(screen)

    elif GAME.game_mode == "end":
        last_btn_group.update()
        last_btn_group.draw(screen)
        global_black_text.print_text("Computer Scientist Simulator", 310, 50)

    if (
        GAME.game_mode != "holl"
        and GAME.game_mode != "main-menu"
        and GAME.game_mode != "end"
    ):
        main_text.print_text("Ваш счёт: " + str(GAME.MONEY) + " ₽", 850, 20)

    if hallucination.is_real and hallucination.sain_veu <= 1:
        screen.blit(pygame.image.load(dir + "\\Data\\textures\\artefact.png"), (0, 0))
        hallucination.sain_veu += 1

    if screamer.is_scremming:
        screamer_group_hallucination.update()
        screamer_group_hallucination.draw(screen)

    MCT.check()
    pygame.display.update()
    one_second_counter = one_second_counter + 1

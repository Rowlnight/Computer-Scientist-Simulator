import pygame
import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.slider import Slider
from pygame_widgets.toggle import Toggle
from pygame_widgets.dropdown import Dropdown
import load_data


pygame.init()
main_font = load_data.get_fonts()
WHITE, BLACK, RED, GREEN, BLUE, YELLOW, GREY, GREY_GAME = load_data.get_colors()


def none():
    pass


def get_widgets(screen):
    core_types = [
        "46B1zdG0IG 60 False",
        "7Vio85Hf3s 89 True",
        "690UTBht4a 50 False",
        "xQP34iZ9b5 100 True",
        "D1a584cuyJ 65 True",
        "566KhI4oiq 78 False",
        "I2GW-Z83Fp 120 True",
        "B-Tyv-QX7J 97 True",
        "Ivf-E_Xi0C 40 True",
        "mKlAG-0eCD 74 False",
        "wN-wXl5JzD 80 False",
        "4K-i9bkVh8 59 True",
        "I_Hp1wBmE1 57 True",
    ]

    dropdown = Dropdown(
        screen,
        650,
        180,
        300,
        40,
        name="Система охлаждения",
        choices=[
            "v-u16metqa",
            "v0-na8hoxk",
            "i5x9-eziux",
            "ke_urm_9l9",
            "64ae62om-n",
            "c4-om4xmat",
            "UIc0-vkftF",
            "b9-jg6q2jV",
        ],
        borderRadius=3,
        colour=pygame.Color("grey"),
        values=[
            "20 4499",
            "40 2200",
            "60 1680",
            "80 1300",
            "100 1100",
            "54 1899",
            "70 1550",
            "75 1433",
        ],
        direction="down",
        textHAlign="left",
        font=pygame.font.Font(main_font, 20),
    )

    textbox_2 = TextBox(
        screen,
        350,
        180,
        280,
        40,
        fontSize=32,
        borderColour=BLACK,
        textColour=BLACK,
        onSubmit=none,
        radius=10,
        borderThickness=5,
        font=pygame.font.Font(main_font, 20),
    )

    slider_1 = Slider(
        screen,
        1000,
        50,
        40,
        550,
        min=1,
        max=100,
        step=1,
        vertical=True,
        handleRadius=15,
    )
    slider_2 = Slider(
        screen,
        100,
        50,
        800,
        40,
        min=1,
        max=100,
        step=1,
        vertical=False,
        handleRadius=15,
    )

    output_1 = TextBox(
        screen, 900, 250, 50, 50, fontSize=30, font=pygame.font.Font(main_font, 20)
    )
    output_2 = TextBox(
        screen, 900, 300, 50, 50, fontSize=30, font=pygame.font.Font(main_font, 20)
    )

    toggle = Toggle(screen, 270, 185, 50, 20, handleRadius=15, vertical=True)

    return (
        core_types,
        dropdown,
        textbox_2,
        slider_1,
        slider_2,
        output_1,
        output_2,
        toggle,
    )


def get_widgets_for_slots(screen):
    textbox_input_new_price = TextBox(
        screen,
        262,
        200,
        550,
        60,
        fontSize=32,
        borderColour=BLACK,
        textColour=BLACK,
        onSubmit=none,
        radius=10,
        borderThickness=5,
        font=pygame.font.Font(main_font, 20),
    )

    return textbox_input_new_price

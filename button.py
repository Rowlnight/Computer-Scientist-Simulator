import os
import pygame

pygame.init()
pygame.mixer.init()

dir = os.path.abspath(os.curdir)


class Button(pygame.sprite.Sprite):
    def __init__(
        self, dirrectory, xy, WIDTH_HEIGHT, sound, text, target=None, arg=None
    ):
        pygame.sprite.Sprite.__init__(self)
        self.target = target
        self.arg = arg
        self.x = xy[0]
        self.y = xy[1]
        self.sound = sound
        self.WIDTH = WIDTH_HEIGHT[0]
        self.HEIGHT = WIDTH_HEIGHT[1]

        self.images = []
        self.images_press = []
        for image in os.listdir(dirrectory):
            if "." in image:
                self.images.append(pygame.image.load(dirrectory + "\\" + image))

        for image in os.listdir(dirrectory + "\\on_press"):
            if "." in image:
                self.images_press.append(
                    pygame.image.load(dirrectory + "\\on_press\\" + image)
                )

        self.index = 0
        self.image = self.images[self.index]
        sur = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.rect = sur.get_rect(center=(self.x, self.y))

        font = pygame.font.Font(dir + "\\Data\\fonts\\main.ttf", 25)
        self.text_result = font.render(text[0], False, text[1])

    def update(self):
        point = pygame.mouse.get_pos()
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0

        if self.rect.collidepoint(point):
            self.image = self.images_press[self.index]

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if click[0] == 1 and MCT.CL_check:
                pygame.mixer.Sound.play(self.sound)
                pygame.time.delay(30)
                if self.arg is not None:
                    self.target(self.arg)
                else:
                    self.target()
        else:
            self.image = self.images[self.index]

        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        self.image.blit(
            self.text_result,
            self.text_result.get_rect(center=self.image.get_rect().center),
        )


class Mouse_click_control:
    def __init__(self):
        self.CL_check = True

    def check(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if click[0] == 1 and self.CL_check:
            self.CL_check = False
        if click[0] == 0:
            self.CL_check = True


MCT = Mouse_click_control()

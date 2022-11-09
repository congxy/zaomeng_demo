 # -*- coding: utf-8 -*
import pygame

class Alarm_light():
    def __init__(self,screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.img_alarm_light = pygame.image.load("./images/boss/range_red.png")
        self.img_blue_light_1 = pygame.image.load("./images/boss/range_blue_1.png")
        self.img_blue_light_2 = pygame.image.load("./images/boss/range_blue_2.png")
        self.image = self.img_alarm_light
        self.rect = self.img_alarm_light.get_rect()
        self.rect.bottom = self.screen_rect.bottom - 110
        self.rect.centerx = self.screen_rect.centerx

    def draw(self):
        '''绘制区域'''
        self.screen.blit(self.image, self.rect)



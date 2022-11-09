 # -*- coding: utf-8 -*
import pygame
from pygame.sprite import Sprite


class Stone(Sprite):
    '''一个对石头进行管理的类'''

    def __init__(self, ai_settings, screen, throw):
        '''在飞船所处的位置创建一个光波对象'''
        super().__init__()
        self.screen = screen
        self.screen_act = screen
        self.bearing = throw.bearing
        self.move = 0
        # 绘制不同旋转角度的石头
        self.img_stone_left_1 =  pygame.image.load("./images/stone_1.png")
        self.img_stone_left_2 = pygame.image.load("./images/stone_2.png")
        self.img_stone_left_3 = pygame.image.load("./images/stone_3.png")
        self.img_stone_left_4 = pygame.image.load("./images/stone_4.png")
        self.img_stone_right_1 =  pygame.image.load("./images/stone_4.png")
        self.img_stone_right_2 = pygame.image.load("./images/stone_3.png")
        self.img_stone_right_3 = pygame.image.load("./images/stone_2.png")
        self.img_stone_right_4 = pygame.image.load("./images/stone_1.png")
        self.image = self.img_stone_left_1
        # 创建一个光波,设置正确的位置
        self.rect = self.image.get_rect()
        self.speed_factor = ai_settings.bullet_speed_factor
        #石头位置的下限(超过这个下限就要被删除哦)
        self.min_bottom = self.screen_act.bottom-110
        #水平相关
        if self.bearing == False:
            #向右
            self.rect.centerx = float(throw.rect.left)
            self.speedx = 2.0
        else:
            # 向左飞
            self.rect.centerx = float(throw.rect.right)
            self.speedx = -2.0
        #垂直相关
        self.rect.centery = float(throw.rect.top)
        self.speedy = -2.0
        self.accelerate = 0.05

    def update(self):
        # 更新表示石头位置的小数值
        self.rect.centerx += self.speedx
        self.speedy += self.accelerate
        self.rect.centery += self.speedy
        self.move += 1
        if self.bearing == False:
            #向右
            if(self.move % 20 > 15):
                self.image = self.img_stone_right_1
            elif(self.move % 20 > 10):
                self.image = self.img_stone_right_2
            elif (self.move % 20 > 5):
                self.image = self.img_stone_right_3
            else:
                self.image = self.img_stone_right_4
        else:
            if(self.move % 20 > 15):
                self.image = self.img_stone_left_1
            elif(self.move % 20 > 10):
                self.image = self.img_stone_left_2
            elif (self.move % 20 > 5):
                self.image = self.img_stone_left_3
            else:
                self.image = self.img_stone_left_4
        self.draw_bullet()

    def draw_bullet(self):
        '''在屏幕上绘制光波'''
        #self.screen.blit(self.image, self.rect)
        pass

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''一个对猴子发射的光波进行管理的类'''
    
    def __init__(self,ai_settings,screen,houzi):
        '''在飞船所处的位置创建一个光波对象'''
        super().__init__()
        self.screen = screen
        self.bearing = houzi.bearing
        #绘制不同方向的光波
        if not self.bearing:
            self.image = pygame.image.load("./images/attack2.png")
        else:
            self.image = pygame.image.load("./images/attack3.png")
        #创建一个光波,设置正确的位置
        self.rect = self.image.get_rect()
        self.rect.centery = houzi.rect.centery-9
        if not self.bearing:
            self.rect.right = houzi.rect.right
        else:
            self.rect.left = houzi.rect.left
#       self.rect.width = 300
        #储存用小数点表示的光波位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.bullet_speed_factor
        self.speedy = 0
        self.bullet_accelerate = 0.04

    def update(self):
        if not self.bearing:
            '''向右光波子弹'''
            #更新表示光波位置的小数值
            self.x += self.speed_factor
        else:
            self.x -= self.speed_factor
        self.speedy += self.bullet_accelerate
        self.y += self.speedy
        #更新表示光波的rect的位置
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw_bullet(self):
        '''在屏幕上绘制光波'''
        self.screen.blit(self.image,self.rect)

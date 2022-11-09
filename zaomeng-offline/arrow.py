import pygame
from pygame.sprite import Sprite

class Arrow(Sprite):
    '''一个对猴子发射的光波进行管理的类'''
    
    def __init__(self,ai_settings,screen,boss,index = -1,houzi = -1):
        '''在飞船所处的位置创建一个光波对象'''
        super().__init__()
        self.screen = screen
        self.index = index
        self.target_pos = houzi
        self.bearing = boss.arrow_bearing
        self.img_up = pygame.image.load("./images/boss/arrow_up.png")
        self.img_down = pygame.image.load("./images/boss/arrow_down.png")
        self.img_left = pygame.image.load("./images/boss/arrow_left.png")
        self.img_right = pygame.image.load("./images/boss/arrow_right.png")
        self.image = self.img_left
        #创建一个箭,设置正确的位置
        self.rect = self.image.get_rect()
        if(self.index == 1):
            self.rect.centerx = boss.rect.centerx
            self.rect.centery = boss.rect.top
        elif(self.index == 2):
            self.rect.centerx = boss.rect.centerx+25
            self.rect.centery = boss.rect.top
        elif(self.index == 3):
            self.rect.centerx = boss.rect.centerx+50
            self.rect.centery = boss.rect.top
        else:
            self.rect.left = boss.rect.left
            self.rect.y = boss.rect.top + 75
        #储存用小数点表示的箭位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.arrow_speed_factor
        self.speed_y = 10
        self.acceleration=ai_settings.arrow_acceleration
        self.fly = 50
        
    def update(self,ai_settings):
        if(self.bearing == 4):
            '''向右放箭'''
            self.speed_factor += self.acceleration
            self.x += self.speed_factor
            self.image = self.img_right
        elif(self.bearing == 3):
            self.speed_factor += self.acceleration
            self.x -= self.speed_factor
            self.image = self.img_left
        elif(self.bearing == 1):
            self.speed_y -= self.acceleration
            self.y -= self.speed_y
            self.image = self.img_up
            if(self.rect.bottom < 0):
                self.bearing = 2
                self.speed_y = 10
                self.y = -200
                if(self.index == 1):
                    self.x = self.target_pos - 25
                elif(self.index == 2):
                    self.x = self.target_pos
                elif(self.index == 3):
                    self.x = self.target_pos + 25
        elif(self.bearing == 2):
            if(self.fly>0):
                self.fly -= 1
            else:
                self.speed_y += self.acceleration
                self.y += self.speed_y
                self.image = self.img_down

        #更新表示箭的rect的位置
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self):
        '''在屏幕上绘制光波'''
        self.screen.blit(self.image,self.rect)


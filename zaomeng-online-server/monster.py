 # -*- coding: utf-8 -*
import pygame
from blood import Blood

class Monster():
    def __init__(self, screen, ai_settings,start_pos=10000):
        '''forwar向右，backward向左'''
        self.forward = False
        self.backward = False
        '''方向,false向右，true向左'''
        self.bearing = False
        self.move = 0
        self.step = 1
        self.screen = screen
        self.screen_rect = screen
        self.ai_settings = ai_settings
        self.img_walk_right_1  = pygame.image.load("./images/monster_walk_right_1.png")
        self.img_walk_right_2 = pygame.image.load("./images/monster_walk_right_2.png")
        self.img_walk_right_3 = pygame.image.load("./images/monster_walk_right_3.png")
        self.img_walk_left_1  = pygame.image.load("./images/monster_walk_left_1.png")
        self.img_walk_left_2 = pygame.image.load("./images/monster_walk_left_2.png")
        self.img_walk_left_3 = pygame.image.load("./images/monster_walk_left_3.png")
        self.img_attack_left_1 = pygame.image.load("./images/monster_attack_left_1.png")
        self.img_attack_right_1 = pygame.image.load("./images/monster_attack_right_1.png")
        self.img_attack_left_2 = pygame.image.load("./images/monster_attack_left_2.png")
        self.img_attack_right_2 = pygame.image.load("./images/monster_attack_right_2.png")
        self.img_attack_left_3 = pygame.image.load("./images/monster_attack_left_3.png")
        self.img_attack_right_3 = pygame.image.load("./images/monster_attack_right_3.png")
        self.img_attack_right = pygame.image.load("./images/monster_attack_right.png")
        self.img_attack_left = pygame.image.load("./images/monster_attack_left.png")
        # 加载怪物图像并获取其外接矩形
        if(start_pos > self.screen_rect.centerx):
            self.image = pygame.image.load("./images/monster_walk_left_1.png")
        else:
            self.image = pygame.image.load("./images/monster_walk_right_1.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = self.screen_rect.bottom - 110
        if start_pos == 10000:
            self.rect.right = self.screen_rect.right
        else:
            self.rect.right = start_pos
        #怪物的攻击相关
        self.fight = 0
        self.fight_time_union = ai_settings.fight_time  #攻击动作帧
        self.fight_length = ai_settings.fight_length    #攻击半径
        self.force = ai_settings.monster_force
        # 加载怪物受伤的状态
        self.attacked = False
            #掉血持续时间（帧）
        self.attacked_time = ai_settings.attacked_time
        self.blood_class = Blood(screen,ai_settings)
        # 重置怪物的血量
        self.reset(ai_settings)

    def update(self,houzi,ai_settings):
        if(self.fight>0):
            if(self.fight>self.fight_time_union*1.5):
                if self.bearing == True:
                    self.image = self.img_attack_left_1
                else:
                    self.image = self.img_attack_right_1
            elif (self.fight>self.fight_time_union):
                if self.bearing == True:
                    self.image = self.img_attack_left_2
                else:
                    self.image = self.img_attack_right_2
            else:
                if self.bearing == True:
                    self.image = self.img_attack_left_3
                else:
                    self.image = self.img_attack_right_3
            self.fight -= 1
        else:
            if houzi.rect.centerx-self.fight_length/2 > self.rect.centerx:
                #猴子在怪物右边，怪物AI自动向右走
                self.forward = True
                self.backward = False
            elif houzi.rect.centerx+self.fight_length/2 < self.rect.centerx:
                self.forward = False
                self.backward = True
            else:
                self.forward = False
                self.backward = False
                self.bearing = houzi.rect.centerx < self.rect.centerx
                #开干！
                self.fight = self.fight_time_union * 3

            if self.keep_attacked == 0:
                '''根据按键移动怪物'''
                if self.forward and (self.rect.right < self.screen_rect.right):
                    self.rect.left += self.step
                    self.bearing = False
                    self.move += 1
                    if self.move % 30 < 10:
                        self.image = self.img_walk_right_1
                    elif self.move % 30 > 20:
                        self.image = self.img_walk_right_2
                    else:
                        self.image = self.img_walk_right_3
                # 左走
                if self.backward and (self.rect.left > 0):
                    self.rect.left -= self.step
                    self.bearing = True
                    self.move += 1
                    if self.move % 30 < 10:
                        self.image = self.img_walk_left_1
                    elif self.move % 30 < 20:
                        self.image = self.img_walk_left_2
                    else:
                        self.image = self.img_walk_left_3
            # 怪物受伤
            else:
                self.keep_attacked -= 1
                if self.forward == True:
                    self.image = self.img_attack_right
                else:
                    self.image = self.img_attack_left
        self.draw()
        self.blood_class.update_monster(self,ai_settings)

    def draw(self):
        '''绘制怪物'''
        #self.screen.blit(self.image, self.rect)
        pass

    def reset(self,ai_settings):
        self.blood = ai_settings.blood_background_monster_width / ai_settings.blood_monster_width
        #重置的时候就不要被打了
        self.keep_attacked = 0
        #重置的时候就不要攻击别人了
        self.fight = 0

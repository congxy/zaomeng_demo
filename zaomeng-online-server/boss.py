 # -*- coding: utf-8 -*
import pygame
from blood import Blood
from arrow import Arrow

class Boss():
    def __init__(self, screen, ai_settings):
        '''forwar向右，backward向左'''
        self.forward = False
        self.backward = False
        '''方向,false向右，true向左'''
        self.bearing = False
        '''1234对应箭的上下左右'''
        self.arrow_bearing = 3
        self.move = 0
        self.step = 2
        self.screen = screen
        self.screen_rect = screen
        self.ai_settings = ai_settings
        self.img_walk_right_1  = pygame.image.load("./images/boss/walk_right_1.png")
        self.img_walk_right_2 = pygame.image.load("./images/boss/walk_right_2.png")
        self.img_walk_left_1  = pygame.image.load("./images/boss/walk_left_1.png")
        self.img_walk_left_2 = pygame.image.load("./images/boss/walk_left_2.png")
        self.img_heng_attack_left_1 = pygame.image.load("./images/boss/attack_heng_left_1.png")
        self.img_heng_attack_right_1 = pygame.image.load("./images/boss/attack_heng_right_1.png")
        self.img_heng_attack_left_2 = pygame.image.load("./images/boss/attack_heng_left_2.png")
        self.img_heng_attack_right_2 = pygame.image.load("./images/boss/attack_heng_right_2.png")
        self.img_heng_attack_left_3 = pygame.image.load("./images/boss/attack_heng_left_3.png")
        self.img_heng_attack_right_3 = pygame.image.load("./images/boss/attack_heng_right_3.png")
        self.img_tian_attack_left_1 = pygame.image.load("./images/boss/attack_tian_left_1.png")
        self.img_tian_attack_right_1 = pygame.image.load("./images/boss/attack_tian_right_1.png")
        self.img_tian_attack_left_2 = pygame.image.load("./images/boss/attack_tian_left_2.png")
        self.img_tian_attack_right_2 = pygame.image.load("./images/boss/attack_tian_right_2.png")
        self.img_tian_attack_left_3 = pygame.image.load("./images/boss/attack_tian_left_3.png")
        self.img_tian_attack_right_3 = pygame.image.load("./images/boss/attack_tian_right_3.png")
        self.img_attack_left = pygame.image.load("./images/boss/attacked_left.png")
        self.img_attack_right = pygame.image.load("./images/boss/attacked_right.png")
        # 加载怪物图像并获取其外接矩形
        self.image = self.img_walk_left_1
        self.rect = self.image.get_rect()
        self.rect.bottom = self.screen_rect.bottom - 110
        self.rect.right = self.screen_rect.right
        #怪物的攻击相关
        self.fight = 0
        self.fight_time_union = ai_settings.fight_time*2  #攻击动作帧
        self.fight_length = 800    #攻击半径
        self.force = ai_settings.boss_force
        #boss那肯定得有两套技能啊！
        self.fight_type = 0
        # 加载怪物受伤的状态
        self.attacked = False
        #掉血动作持续时间（帧）
        self.attacked_time = 0
        self.blood_class = Blood(screen,ai_settings)
        # 重置怪物的血量
        self.reset(ai_settings)

    def update(self,houzi,ai_settings,arrows,screen):
        #攻击动作
        if(self.fight>0):
            if(self.fight_type %2 == 0):
                # 攻击动作（横向射箭）
                if(self.fight>self.fight_time_union*2.5):
                    if self.bearing == True:
                        self.image = self.img_heng_attack_left_1
                    else:
                        self.image = self.img_heng_attack_right_1
                elif (self.fight>self.fight_time_union*0.8):
                    if self.bearing == True:
                        self.image = self.img_heng_attack_left_2
                    else:
                        self.image = self.img_heng_attack_right_2
                else:
                    if(self.fight == (int)(self.fight_time_union*0.8)):
                        arrow = Arrow(ai_settings,screen,self)
                        arrows.add(arrow)
                    if self.bearing == True:
                        self.image = self.img_heng_attack_left_3
                    else:
                        self.image = self.img_heng_attack_right_3
                self.fight -= 1
            else:
                # 攻击动作（天上射箭）
                if(self.fight>self.fight_time_union*2.5):
                    if self.bearing == True:
                        self.image = self.img_tian_attack_left_1
                    else:
                        self.image = self.img_tian_attack_right_1
                elif (self.fight>self.fight_time_union*0.8):
                    if self.bearing == True:
                        self.image = self.img_tian_attack_left_2
                    else:
                        self.image = self.img_tian_attack_right_2
                else:
                    if(self.fight == (int)(self.fight_time_union*0.8)):
                        self.arrow_bearing = 1
                        arrow = Arrow(ai_settings,screen,self,1,houzi.rect.centerx)
                        arrows.add(arrow)
                        arrow = Arrow(ai_settings,screen,self,2,houzi.rect.centerx)
                        arrows.add(arrow)
                        arrow = Arrow(ai_settings,screen,self,3,houzi.rect.centerx)
                        arrows.add(arrow)
                    if self.bearing == True:
                        self.image = self.img_heng_attack_left_3
                    else:
                        self.image = self.img_heng_attack_right_3
                self.fight -= 1

        else:
            # 怪物受伤
            if (self.keep_attacked > 0):
                # self.fight = 0
                self.keep_attacked -= 1
                if self.forward == True:
                    self.image = self.img_attack_right
                else:
                    self.image = self.img_attack_left
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
                    if self.bearing == False:
                        self.arrow_bearing = 4
                    else:
                        self.arrow_bearing = 3
                    #开干！！！！！！！
                    self.fight = self.fight_time_union * 3
                    self.fight_type += 1

                if self.forward and (self.rect.right < self.screen_rect.right):
                    self.rect.left += self.step
                    self.bearing = False
                    self.arrow_bearing = 4
                    self.move += 1
                    if self.move % 4 < 2:
                        self.image = self.img_walk_right_1
                    else:
                        self.image = self.img_walk_right_2
                # 左走
                if self.backward and (self.rect.left > 0):
                    self.rect.left -= self.step
                    self.bearing = True
                    self.arrow_bearing = 3
                    self.move += 1
                    if self.move % 4 < 2:
                        self.image = self.img_walk_left_1
                    else:
                        self.image = self.img_walk_left_2
        self.draw()
        self.blood_class.update_boss(self,ai_settings)

    def draw(self):
        '''绘制怪物'''
        #self.screen.blit(self.image, self.rect)
        pass

    def reset(self,ai_settings):
        self.blood = ai_settings.blood_background_boss_width / ai_settings.blood_boss_width
        #重置的时候就不要被打了
        self.keep_attacked = 0
        #重置的时候就不要攻击别人了
        self.fight = 0

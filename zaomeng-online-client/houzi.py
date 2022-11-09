 # -*- coding: utf-8 -*
import pygame

class Houzi():
    def __init__(self,screen,ai_settings):
        self.forward = False
        self.backward = False
        self.down = False 
        '''方向'''
        self.bearing = False
        '''跳跃相关指示'''
        self.jump = False
        self.jump_up = False
        self.jump_down = False
        self.step = 2
        self.jump_step = 0.025
        self.jump_limit = 200
        self.move = 0 
        self.screen = screen
        self.ai_settings = ai_settings
        #受到攻击时动作持续时间
        self.attacked_time = 0
        #猴子的攻击力
        self.force = ai_settings.force
        #撞击
        self.last_state = ai_settings.last_state
        self.collision = ai_settings.collision
        #加载猴子图像并获取其外接矩形
        self.img_jingzhi_left = pygame.image.load("./images\houzi_jingzhi_left.png")
        self.img_jingzhi_right = pygame.image.load("./images\houzi_jingzhi_right.png")
        self.img_move_left2 = pygame.image.load("./images/houzi_move_left2.png")
        self.img_move_right2 = pygame.image.load("./images/houzi_move_right2.png")
        self.img_move_left = pygame.image.load("./images/houzi_move_left.png")
        self.img_attack_left = pygame.image.load("./images/houzi_attack_left.png")
        self.img_attack_right = pygame.image.load("./images/houzi_attack_right.png")
        self.img_down = pygame.image.load("./images/houzi_down.png")
        self.img_down_fan = pygame.image.load("./images/houzi_down_fan.png")
        self.img_jump = pygame.image.load("./images/houzi_jump.png")
        self.img_jump_fan = pygame.image.load("./images/houzi_jump_fan.png")
        self.image = self.img_jingzhi_left
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        #加载猴子受伤的状态
        self.attacked = False
        #记录起跳前位置
        self.jump_position = self.screen_rect.bottom-110
        self.blood = ai_settings.blood
        #重置、归位
        self.reset()
        
    def update(self,stairs):
        if stairs.moving:
            if(self.rect.left > 0):
                self.rect.centerx -= stairs.step
        else:
            if self.attacked_time == 0:
                '''根据按键移动猴子'''
                if self.rect.centerx < stairs.rect.left and self.rect.bottom <self.screen_rect.bottom-110 and not self.jump:
                    self.down = True
                if self.rect.centerx > stairs.rect.right and self.rect.bottom <self.screen_rect.bottom-110 and not self.jump:
                    self.down = True
                #右走
                if self.forward and (self.rect.right < self.screen_rect.right):
                    self.rect.left += self.step
                    self.bearing = False
                    self.move += 1
                    if self.move%20 < 10:
                        self.image = self.img_jingzhi_right
                    else:
                        self.image = self.img_move_right2
                #左走
                if self.backward and (self.rect.left > 0):
                    self.rect.left -= self.step
                    self.bearing = True
                    self.move += 1
                    if self.move%20 and self.move%20 < 10:
                        self.image = self.img_jingzhi_left
                    elif self.move%2 > 10:
                        self.image = self.img_move_left2
                    else:
                        self.image = self.img_move_left
                #下降
                if self.down and (self.rect.bottom < self.screen_rect.bottom-110) and not self.jump:
                    self.go_down(stairs)
                if self.jump:
                   self.jump_control(stairs)
            #猴子受伤
            else:
                self.attacked_time -= 1
                if self.bearing == False:
                    self.image = self.img_attack_right
                else:
                    self.image = self.img_attack_left
        self.draw()
            
    def draw(self):
        '''绘制猴子'''
        self.screen.blit(self.image,self.rect)  
        
    def jump_control(self,stairs):
        #跳跃_上升
        if (self.rect.bottom >= self.jump_position-self.jump_limit) and self.jump_up:
            self.rect.bottom -= 8-round(self.jump_step*(self.jump_position- self.rect.bottom))
            if self.bearing == False:
                self.image = self.img_jump
            else:
                self.image = self.img_jump_fan
        #上升到顶点？
        elif self.rect.bottom <= self.jump_position-self.jump_limit:
            self.jump_up = False
            self.jump_down = True
            self.rect.bottom += 8-round(self.jump_step*(self.jump_position- self.rect.bottom))
        #跳跃_下降
        elif (self.rect.bottom >= self.jump_position-self.jump_limit) and self.jump_down:
            self.go_down(stairs)
            #下降到台阶上?
            if (self.rect.bottom < stairs.rect.centery) and  (self.rect.bottom > stairs.rect.top+45) and (self.rect.centerx >= stairs.rect.left) and (self.rect.centerx <= stairs.rect.right):
                self.jump=False
                self.jump_down = False
                self.jump_position = self.rect.bottom
                if self.bearing == False:
                    self.image = self.img_jingzhi_right
                else:
                    self.image = self.img_jingzhi_left
            
    def go_down(self,stairs):
        '''用来描绘下降过程'''
        if self.down:
            #从梯子上下去
            self.rect.bottom += 5-round(0.022222*(self.jump_position- self.rect.bottom))
        else:
            self.rect.bottom += 8-round(self.jump_step*(self.jump_position- self.rect.bottom))
        if self.bearing == False:
            self.image = self.img_down
        else:
            self.image = self.img_down_fan

        #下降到地图低点?
        if self.rect.bottom >= self.screen_rect.bottom-110:
            self.jump = False
            self.down = False
            self.jump_down = False
            #更新起跳位置
            self.jump_position = self.screen_rect.bottom-110
            if self.bearing == False:
                self.image = self.img_jingzhi_right
            else:
                self.image = self.img_jingzhi_left
        
    def reset(self):
        self.rect.bottom = self.screen_rect.bottom-110
        self.rect.left = self.screen_rect.centerx
        self.attacked = False
        self.blood = 10
        self.image = self.img_jingzhi_left
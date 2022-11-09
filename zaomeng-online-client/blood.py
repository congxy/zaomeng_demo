 # -*- coding: utf-8 -*
import pygame

class Blood():
    def __init__(self,screen,ai_settings): 
        self.screen = screen
        self.screen_rect = screen.get_rect()
        #背景框的边框
        self.backback_rect = pygame.Rect(0,0,ai_settings.blood_background_width,ai_settings.blood_background_height)
        self.backback_monster_rect = pygame.Rect(0,0,ai_settings.blood_background_monster_width,ai_settings.blood_background_height)
        self.backback_boss_rect = pygame.Rect(0, 0, ai_settings.blood_background_boss_width,ai_settings.blood_background_height*2)
        self.backback_color = ai_settings.backback_color
        #在中心处创建一个血条背景框
        self.background_rect = pygame.Rect(0,0,ai_settings.blood_background_width,ai_settings.blood_background_height)
        self.background_monster_rect = pygame.Rect(0,0,ai_settings.blood_background_monster_width,ai_settings.blood_background_height)
        self.background_boss_rect = pygame.Rect(0,0,ai_settings.blood_background_boss_width,ai_settings.blood_background_height*2)
        self.background_color = ai_settings.blood_background_color
        #在中心处创建一个血条
        self.rect = pygame.Rect(0,0,ai_settings.blood_width*ai_settings.blood,ai_settings.blood_height)
        self.rect.centerx = ai_settings.screen_width/2
        self.rect.centery = ai_settings.screen_height/2
        self.color = ai_settings.blood_color

    def update(self,houzi,ai_settings):
        #血条背景框（就是个矩形，画起来很方便，不用blit）
        self.background_rect.bottom = houzi.rect.top
        self.background_rect.centerx = houzi.rect.centerx
        pygame.draw.rect(self.screen,self.background_color,self.background_rect)
        #血条
        self.rect = pygame.Rect(0,0,ai_settings.blood_width*houzi.blood,ai_settings.blood_height)
        self.rect.bottom = houzi.rect.top
        self.rect.right = self.background_rect.right
        pygame.draw.rect(self.screen,self.color,self.rect)

    def update_monster(self,monster,ai_settings):
        #血条边框
        self.backback_monster_rect.bottom = monster.rect.top
        self.backback_monster_rect.centerx = monster.rect.centerx
        pygame.draw.rect(self.screen, self.backback_color, self.backback_monster_rect,2)
        #血条背景框（就是个矩形，画起来很方便，不用blit）
        self.background_monster_rect.bottom = monster.rect.top
        self.background_monster_rect.centerx = monster.rect.centerx
        pygame.draw.rect(self.screen,self.background_color,self.background_monster_rect)
        #血条
        self.color = ai_settings.monster_blood_color
        self.rect = pygame.Rect(0,0,ai_settings.blood_width*monster.blood,ai_settings.blood_height)
        self.rect.bottom = monster.rect.top
        self.rect.right = self.background_monster_rect.right
        pygame.draw.rect(self.screen,self.color,self.rect)

    def update_boss(self,boss,ai_settings):
        #血条边框
        self.backback_boss_rect.centery = 80
        self.backback_boss_rect.centerx = self.screen_rect.centerx
        pygame.draw.rect(self.screen, self.backback_color, self.backback_boss_rect,2)
        #血条背景框（就是个矩形，画起来很方便，不用blit）
        self.background_boss_rect.centery = 80
        self.background_boss_rect.centerx = self.screen_rect.centerx
        pygame.draw.rect(self.screen,self.background_color,self.background_boss_rect)
        #血条
        self.color = ai_settings.boss_blood_color
        self.rect = pygame.Rect(0,0,ai_settings.blood_width*boss.blood,ai_settings.blood_height*2)
        self.rect.centery = 80
        self.rect.right = self.background_boss_rect.right
        pygame.draw.rect(self.screen,self.color,self.rect)
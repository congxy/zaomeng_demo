import pygame

class Stairs():
    def __init__(self,screen,ai_settings):
        self.screen = screen
        self.ai_settings = ai_settings
        '''加载台阶位置'''
        self.image = pygame.image.load("./images/stairs.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.step = 2
        #代表stairs在移动，一切动作的参考系都是这个staris
        self.moving = False
        self.reset()

    def draw(self):
        self.screen.blit(self.image,self.rect)

    def reset(self):
        self.rect.bottom = self.screen_rect.bottom-200
        self.rect.right = self.screen_rect.right-80

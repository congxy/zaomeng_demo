import pygame

class End_game():
    def __init__(self,screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.img_victor = pygame.image.load("./images/victor.png")
        self.img_fail = pygame.image.load("./images/fail.png")
        self.image = self.img_fail
        self.rect = self.image.get_rect()
        self.rect.centerx = 80
        self.rect.right = self.screen_rect.right-100

    def draw_fail(self):
        self.image = self.img_fail
        '''绘制区域'''
        self.screen.blit(self.image, self.rect)

    def draw_victor(self):
        self.image = self.img_victor
        '''绘制区域'''
        self.screen.blit(self.image, self.rect)
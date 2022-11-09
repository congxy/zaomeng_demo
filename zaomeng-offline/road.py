import pygame

class Roads():
    def __init__(self,screen,ai_settings):
        self.screen = screen
        self.ai_settings = ai_settings
        '''加载台阶位置'''
        self.image1 = pygame.image.load("./images/road.png")
        self.image2 = pygame.image.load("./images/road.png")
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()
        self.screen_rect = screen.get_rect()
        self.step = 2
        self.reset()

    def update(self,stairs):
        if(stairs.moving):
            self.rect1.right -= stairs.step
            self.rect2.right -= stairs.step
            if(self.rect1.right <= 0):
                self.rect1.left = self.screen_rect.right
            if(self.rect2.right <= 0):
                self.rect2.left = self.screen_rect.right
        self.draw()

    def draw(self):
        self.screen.blit(self.image1,self.rect1)
        self.screen.blit(self.image2,self.rect2)

    def reset(self):
        self.rect1.bottom = self.screen_rect.bottom-70
        self.rect1.right = self.screen_rect.right
        self.rect2.bottom = self.screen_rect.bottom-70
        self.rect2.left = self.screen_rect.right

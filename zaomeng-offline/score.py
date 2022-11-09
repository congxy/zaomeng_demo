import pygame.font

class Score():
    def __init__(self,ai_settings,screen,msg):
        '''初始化按钮的属性'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        #设置按钮的尺寸和其他属性
        self.width,self.height = 55,28
        self.score_color = (35,63,72)
        self.text_color = (246,234,197)
        self.font = pygame.font.SysFont('Arial',24)
        
        #创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.top = self.screen_rect.top
        self.rect.centerx = self.screen_rect.centerx+58
        #文本存一下
        self.msg = msg
        #按钮的标签只需创建一次
        self.prep_msg()

    def prep_msg(self):
        '''将msg渲染为图像，并使其在按钮上居中'''
        self.msg_image = self.font.render(self.msg,True,self.text_color,self.score_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_score(self):
        #绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.score_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
        
    def update(self,ai_settings):
        score = 10*ai_settings.arrow_number
        self.msg = "{:,}".format(score)
        self.prep_msg()
        self.draw_score()
 

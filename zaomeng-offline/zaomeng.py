import sys
import pygame
import os
from arrow import Arrow
from game_stats import GameStats
from button import Button
from score import Score
from settings import Settings
from houzi import Houzi
from monster import Monster
from throws import Throw
from blood import Blood
from stairs import Stairs
from road import Roads
from bullet import Bullet
from end_game import End_game
from boss import Boss
from pygame.sprite import Group
from alarm_light import Alarm_light

def run_game():
    pygame.init()
    pygame.mixer.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    '''游戏开始'''
    stats = GameStats(ai_settings)
    '''背景图片'''
    wallpaper_image = pygame.image.load("images\\beijing.png")
    '''攻击的光'''
    light_image = pygame.image.load("./images/light.png")
    '''受伤的光'''
    light_attacked_image = pygame.image.load("./images/light_attacked.png")
    '''创建台阶'''
    stairs = Stairs(screen,ai_settings)
    '''创建路'''
    road = Roads(screen,ai_settings)
    '''创建猴子'''
    houzi = Houzi(screen,ai_settings)
    '''创建怪物'''
    throws = []
    monsters = []
    #monsters.append(Monster(screen,ai_settings))
    #monsters.append(Monster(screen,ai_settings,100))
    '''创建Boss'''
    boss = Boss(screen,ai_settings)
    '''创建血条'''
    blood = Blood(screen,ai_settings)
    '''加载背景音乐'''
    pygame.mixer.music.load("./music/m.wav")
    '''创建光波编组'''
    bullets = Group()
    '''创建箭'''
    arrows = Group()
    '''创建箭的提示区'''
    alarm_light = Alarm_light(screen)
    '''创建石头'''
    stones = Group()
    '''创建开始按钮'''
    play_button = Button(ai_settings,screen,"play")
    '''创建boss名字'''
    boss_name = Button(ai_settings,screen,"general")
    '''创建积分板'''
    #score = Score(ai_settings,screen,"0")
    '''创建胜利/失败图标'''
    end_game = End_game(screen)
    '''游戏场景'''
    scene = [1]
    #设置游戏窗口名
    pygame.display.set_caption("西天取精-cxy")
    while True:
        check_event(houzi,monsters,throws,stairs,ai_settings,screen,bullets,stats,arrows,play_button,scene)
        #没按开始键
        if not stats.game_active:
            draw_wallpaper(screen,wallpaper_image)
            stairs.draw()
            road.draw()
            if(ai_settings.victor == 1):
                end_game.draw_fail()
            elif(ai_settings.victor == 2):
                end_game.draw_victor()
            for monster in monsters:
                monster.draw()
            houzi.draw()
            play_button.draw_button()
            blood.update(houzi,ai_settings)
        #开始游戏
        else:
            draw_wallpaper(screen,wallpaper_image)
            update_stairs(stairs,monsters,throws,screen,ai_settings,scene)
            road.update(stairs)
            if scene[0] == 1:
                for monster in monsters:
                    monster.update(houzi,ai_settings)
                # 检测怪物是否攻击到猴子了
                check_monster_houzi_attack(houzi, monsters, ai_settings, stats,blood)
                # 检测猴子与箭、光波与箭的碰撞
                check_collision(houzi, monsters, arrows, stones, bullets, ai_settings, stats,blood)
            elif scene[0] == 2:
                for throw in throws:
                    throw.update(houzi,ai_settings,stones,screen)
                update_stones(stones)
                # 检测猴子与箭、光波与箭的碰撞
                check_collision(houzi, throws, arrows, stones, bullets, ai_settings, stats,blood)
            elif scene[0] == 3:
                boss.update(houzi, ai_settings, arrows, screen)
                update_arrows(arrows,ai_settings,screen)
                check_collision_boss(houzi, boss, arrows,bullets, ai_settings, stats,blood)
                boss_name.draw_boss()

            houzi.update(stairs)
            #加载血条
            blood.update(houzi,ai_settings)
            update_bullets(bullets)
            #光
            update_light(ai_settings,light_image,houzi,screen,arrows,alarm_light)
            check_music(ai_settings)

        #显示积分板
        #score.update(ai_settings)
        update_screen(screen,ai_settings)
        
def check_event(houzi,monsters,throws,stairs,ai_settings,screen,bullets,stats,arrows,play_button,scene):
    #监视鼠标和键盘事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            reset_game(stats, arrows, bullets, ai_settings, houzi, stairs, monsters, throws, scene, screen)
        elif event.type == pygame.KEYDOWN:
            keydown_events(event,houzi,stairs,ai_settings,screen,bullets,stats)
        elif event.type == pygame.KEYUP:
            keyup_events(event,houzi)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stairs,stats,play_button,mouse_x,mouse_y,arrows,bullets,houzi,monsters,throws,scene)

def keydown_events(event,houzi,stairs,ai_settings,screen,bullets,stats):
    '''猴子按下按键后的对策'''
    if event.key == pygame.K_RIGHT:
        houzi.forward = True
    elif event.key == pygame.K_LEFT: 
        houzi.backward = True
    elif event.key == pygame.K_DOWN: 
        if (houzi.rect.bottom < stairs.rect.centery) and (houzi.rect.bottom > stairs.rect.top+45):
            houzi.down = True
    elif event.key == pygame.K_UP and stats.game_active:
        if not houzi.down:
            houzi.jump = True
        if not houzi.jump_down == True:
            houzi.jump_up = True
    #背景音乐键
    elif event.key == pygame.K_j:
        ai_settings.music_on = True
    elif event.key == pygame.K_k:
        ai_settings.music_on = False 
    #发射攻击光波
    elif event.key == pygame.K_SPACE:
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings,screen,houzi)
            bullets.add(new_bullet)
            ai_settings.light = 8 #放光的延时
    #退出按键
    elif event.key == pygame.K_q:
        sys.exit()
    #重置游戏按键
    elif event.key == pygame.K_r:
        stats.game_active = False
        # 打开光标
        pygame.mouse.set_visible(True)

def keyup_events(event,houzi):
    '''抬起按键后的对策'''
    ###不抬按键就一直走##
    if event.key == pygame.K_RIGHT:
        houzi.forward = False
    elif event.key == pygame.K_LEFT: 
        houzi.backward = False

def check_play_button(ai_settings,screen,stairs,stats,play_button,mouse_x,mouse_y,arrows,bullets,houzi,monsters,throws,scene):
    '''在玩家单击play按钮时开始新游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        reset_game(stats,arrows,bullets,ai_settings,houzi,stairs,monsters,throws,scene,screen)

def reset_game(stats,arrows,bullets,ai_settings,houzi,stairs,monsters,throws,scene,screen):
    # 隐藏光标
    pygame.mouse.set_visible(False)
    stats.game_active = True
    # 清空光波列表和箭列表
    arrows.empty()
    bullets.empty()
    # 重新加载设置
    ai_settings.reset()
    # 猴子归位
    houzi.reset()
    # 梯子归位
    stairs.reset()
    # 怪物归位
    monsters.clear()
    throws.clear()
    monsters.append(Monster(screen, ai_settings))
    monsters.append(Monster(screen, ai_settings, 100))
    # 场景归位
    scene[0] = 1

def draw_wallpaper(screen,wallpaper_image):
    '''画贴纸'''
    wallpaper_rect = wallpaper_image.get_rect()
    screen_rect = screen.get_rect()
    wallpaper_rect.centerx = screen_rect.centerx
    wallpaper_rect.bottom = screen_rect.bottom
    '''绘制贴纸'''
    screen.blit(wallpaper_image,wallpaper_rect)
    
def check_music(ai_settings):
    if ai_settings.music_on:
        if pygame.mixer.music.get_busy()==False:
            pygame.mixer.music.play()
    #可能会有一点占内存！！！
    else:
        pygame.mixer.music.fadeout(500)
        
def update_screen(screen,ai_settings):
    pygame.display.flip()
    
def update_bullets(bullets):
    for bullet in bullets.sprites():
        #更新子弹位置并绘制
        bullet.update()
        bullet.draw_bullet()
    #删除已消失子弹
    for bullet in  bullets.copy():
        if bullet.rect.left >=1100 or bullet.rect.right <0 or bullet.rect.bottom > 580-110:
            bullets.remove(bullet)

def update_stones(stones):
    for stone in stones.sprites():
        #更新石头位置并绘制
        stone.update()
    #删除已消失的石头
    for stone in  stones.copy():
        if stone.rect.top > stone.min_bottom:
            stones.remove(stone)

def update_light(ai_settings,light_image,houzi,screen,arrows,alarm_light):
    if ai_settings.light:
        #光相关 找到猴子的眼睛
        light_rect = light_image.get_rect()
        light_rect.centerx = houzi.rect.right-34
        light_rect.centery = houzi.rect.top+50
        screen.blit(light_image,light_rect)
        ai_settings.light -= 1

    for arrow in arrows:
        if(arrow.bearing == 1 or arrow.bearing == 2):
            alarm_light.image = alarm_light.img_alarm_light
            alarm_light.rect.centerx = arrow.target_pos
            alarm_light.draw()

def update_arrows(arrows,ai_settings,screen):
    for arrow in arrows.sprites():
        #更新箭的位置
        arrow.update(ai_settings)
        arrow.draw()
    #删除已消失箭
    for arrow in arrows.copy():
        if arrow.rect.left > ai_settings.screen_width or arrow.rect.right < 0\
                or arrow.rect.top > ai_settings.screen_height:
            arrows.remove(arrow)

def update_stairs(stairs,monsters,throws,screen,ai_settings,scene):
    if (len(monsters) == 0 and scene[0] == 1):
        if (stairs.rect.centerx > stairs.screen_rect.right / 2):
            stairs.rect.centerx -= stairs.step
            stairs.moving = True
        else:
            stairs.moving = False
            scene[0] = 2
            # 添加新怪物
            throws.append(Throw(screen, ai_settings))
            throws.append(Throw(screen, ai_settings, 100))
    elif(len(throws) == 0 and scene[0] == 2):
        if (stairs.rect.centerx > stairs.screen_rect.right / 5):
            stairs.rect.centerx -= stairs.step
            stairs.moving = True
        else:
            stairs.moving = False
            scene[0] = 3

    stairs.draw()

def check_collision(houzi,monsters,arrows,stones,bullets,ai_settings,stats,blood):
    #判断猴子与箭的碰撞,在houzi.update()中自动更新
    if pygame.sprite.spritecollideany(houzi,arrows) or pygame.sprite.spritecollideany(houzi,stones):
        houzi.attacked = True
        houzi.attacked_time = ai_settings.attacked_time / 5
        for stone in stones:
            if (pygame.sprite.collide_rect(houzi, stone)):
                houzi.bearing = not stone.bearing
    else:
        houzi.attacked = False
    #判断猴子是否相撞一次(防止串糖葫芦一直掉血)
    if ai_settings.last_state != houzi.attacked:
        ai_settings.collision += 1
        if ai_settings.collision%2 ==0:
            if ai_settings.blood > 0:
                ai_settings.blood -= 1
            else:
                ai_settings.blood = 0
                # 加载血条
                blood.update(houzi, ai_settings)
                #游戏失败
                stats.game_active = False
                ai_settings.victor = 1
                #打开光标
                pygame.mouse.set_visible(True)
    ai_settings.last_state = houzi.attacked

    #判断猴子的光波与怪物的碰撞
    check_collision_light_monster(houzi,monsters,bullets)

    #判断光波与箭的碰撞,并自动删除
    pygame.sprite.groupcollide(bullets,arrows,True,True)

def check_monster_houzi_attack(houzi,monsters,ai_settings,stats,blood):
    for monster in monsters:
        if (monster.fight == ai_settings.attacked_time/2):
            if abs(monster.rect.centerx-houzi.rect.centerx) <= monster.fight_length and monster.rect.bottom == houzi.rect.bottom:
                houzi.attacked = True
                houzi.attacked_time = ai_settings.attacked_time/2
                if ai_settings.blood - ai_settings.monster_force > 0:
                    ai_settings.blood -= ai_settings.monster_force
                else:
                    ai_settings.blood = 0
                    # 加载血条
                    blood.update(houzi, ai_settings)
                    # 游戏失败
                    stats.game_active = False
                    ai_settings.victor = 1
                    # 打开光标
                    pygame.mouse.set_visible(True)

def check_collision_light_monster(houzi,monsters,bullets):
    #判断猴子的光波与怪物（猩猩/投石怪）的碰撞
    for monster in monsters.copy():
        if pygame.sprite.spritecollideany(monster, bullets):
            monster.keep_attacked = monster.attacked_time
            for bullet in bullets.copy():
                if(pygame.sprite.collide_rect(monster,bullet)):
                    bullets.remove(bullet)
                    #怪物的掉血
                    if monster.blood-houzi.force > 0:
                        monster.blood -= houzi.force
                    else:
                        # 怪物死了
                        monsters.remove(monster)

def check_collision_boss(houzi, boss, arrows,bullets, ai_settings, stats,blood):
    #判断猴子与箭的碰撞,在houzi.update()中自动更新
    if pygame.sprite.spritecollideany(houzi,arrows):
        houzi.attacked = True
        houzi.attacked_time = ai_settings.attacked_time / 5
        for arrow in arrows:
            if (pygame.sprite.collide_rect(houzi, arrow)):
                if(arrow.bearing == 3):
                    houzi.bearing = False
                else:
                    houzi.bearing = True
    else:
        houzi.attacked = False
    #判断猴子是否相撞一次(防止串糖葫芦一直掉血)
    if ai_settings.last_state != houzi.attacked:
        ai_settings.collision += 1
        if ai_settings.collision%2 ==0:
            if ai_settings.blood - boss.force > 0:
                ai_settings.blood -= boss.force
            else:
                #把残血显示出来
                ai_settings.blood = 0
                # 加载血条
                blood.update(houzi, ai_settings)
                #游戏失败
                stats.game_active = False
                ai_settings.victor = 1
                #打开光标
                pygame.mouse.set_visible(True)
    ai_settings.last_state = houzi.attacked

    #判断猴子的光波与boss的撞击
    if pygame.sprite.spritecollideany(boss, bullets):
        boss.keep_attacked = boss.attacked_time
        for bullet in bullets.copy():
            if (pygame.sprite.collide_rect(boss, bullet)):
                bullets.remove(bullet)
                # 怪物的掉血
                if boss.blood - houzi.force > 0:
                    boss.blood -= houzi.force
                else:
                    # 游戏胜利
                    stats.game_active = False
                    ai_settings.victor = 2
                    # 打开光标
                    pygame.mouse.set_visible(True)

run_game()

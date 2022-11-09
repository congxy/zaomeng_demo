 # -*- coding: utf-8 -*
import socket
import _thread
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
from stones import Stone
from alarm_light import Alarm_light
import time

server_ip = '000.000.000.000'
data = ''
def rev_data():
    global data
    while True:
        try:
            temp = sk.recv(1024)
            data = str(temp, 'utf8')
            print(time.time())
        except ConnectionResetError:
            print('-' * 10 + '服务器歇逼了' + '-' * 10)
            sys.exit()

def run_game():
    #pygame初始化
    pygame.init()
    pygame.mixer.init()

    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    '''游戏开始'''
    stats = GameStats(ai_settings)
    '''背景图片'''
    wallpaper_image = pygame.image.load("images\\beijing.png")
    '''攻击的光'''
    light_image = pygame.image.load("./images/light.png")
    '''受伤的光'''
    light_attacked_image = pygame.image.load("./images/light_attacked.png")
    '''创建台阶'''
    stairs = Stairs(screen, ai_settings)
    '''创建路'''
    road = Roads(screen, ai_settings)
    '''创建猴子'''
    houzi = Houzi(screen, ai_settings)
    hou2 = Houzi(screen, ai_settings)
    '''创建怪物'''
    throws1 = Throw(screen, ai_settings)
    throws2 = Throw(screen, ai_settings)
    throws = [throws1,throws2]
    monster1 = Monster(screen,ai_settings)
    monster2 = Monster(screen,ai_settings)
    monsters = [monster1,monster2]
    '''创建Boss'''
    boss = Boss(screen, ai_settings)
    '''创建血条'''
    blood = Blood(screen, ai_settings)
    '''加载背景音乐'''
    pygame.mixer.music.load("./music/m.wav")
    '''创建光波编组'''
    bullet1 = Bullet(ai_settings,screen,houzi)
    bullet2 = Bullet(ai_settings, screen, houzi)
    bullet3 = Bullet(ai_settings, screen, houzi)
    bullet4 = Bullet(ai_settings, screen, houzi)
    bullet5 = Bullet(ai_settings, screen, houzi)
    bullets = Group(bullet1,bullet2,bullet3,bullet4,bullet5)
    '''创建箭'''
    arrow1 = Arrow(ai_settings,screen,boss)
    arrow2 = Arrow(ai_settings, screen, boss)
    arrow3 = Arrow(ai_settings, screen, boss)
    arrow4 = Arrow(ai_settings, screen, boss)
    arrows = Group(arrow1,arrow2,arrow3,arrow4)
    '''创建箭的提示区'''
    alarm_light = Alarm_light(screen)
    '''创建石头'''
    stone1 = Stone(ai_settings, screen, throws1)
    stone2 = Stone(ai_settings, screen, throws1)
    stones = Group(stone1,stone2)
    '''创建开始按钮'''
    play_button = Button(ai_settings, screen, "play")
    '''创建boss名字'''
    boss_name = Button(ai_settings, screen, "general")
    '''创建积分板'''
    # score = Score(ai_settings,screen,"0")
    '''创建胜利/失败图标'''
    end_game = End_game(screen)
    '''游戏场景'''
    scene = [1]
    # 设置游戏窗口名
    pygame.display.set_caption("西天取精-cxy")
    _thread.start_new_thread(rev_data, ())
    while True:
        send_msg = check_event(sk,houzi, monsters, throws, stairs, ai_settings, screen, bullets, stats, arrows, play_button, scene)
        #print(data,'\n')
        d = data.split('*')
        draw_wallpaper(screen, wallpaper_image)
        for i in range((int)(len(d)/4)):
            if d[i*4] == '1':
                houzi.rect.x = float(d[i*4+1])
                houzi.rect.y = float(d[i*4+2])
                if d[i*4+3] == '1':
                    houzi.image = houzi.img_jingzhi_left
                elif d[i*4+3] == '2':
                    houzi.image = houzi.img_jingzhi_right
                elif d[i*4+3] == '3':
                    houzi.image = houzi.img_move_left2
                elif d[i*4+3] == '4':
                    houzi.image = houzi.img_move_right2
                elif d[i*4+3] == '5':
                    houzi.image = houzi.img_move_left
                elif d[i*4+3] == '6':
                    houzi.image = houzi.img_attack_left
                elif d[i*4+3] == '7':
                    houzi.image = houzi.img_attack_right
                elif d[i*4+3] == '8':
                    houzi.image = houzi.img_down
                elif d[i*4+3] == '9':
                    houzi.image = houzi.img_down_fan
                elif d[i*4+3] == '10':
                    houzi.image = houzi.img_jump
                elif d[i*4+3] == '11':
                    houzi.image = houzi.img_jump_fan
                houzi.draw()
            elif d[i*4] == '2':
                stairs.rect.x = float(d[i*4+1])
                stairs.rect.y = float(d[i*4+2])
                stairs.draw()
            elif d[i*4] == '3':
                road.rect1.x = float(d[i*4+1])
                road.rect1.y = float(d[i*4+2])
                road.draw1()
            elif d[i * 4] == '4':
                road.rect2.x = float(d[i*4+1])
                road.rect2.y = float(d[i*4+2])
                road.draw2()
            elif d[i*4] == '5':
                monster1.rect.x = float(d[i*4+1])
                monster1.rect.y = float(d[i*4+2])
                if d[i*4+3] == '1':
                    monster1.image = monster1.img_walk_right_1
                elif d[i*4+3] == '2':
                    monster1.image = monster1.img_walk_right_2
                elif d[i*4+3] == '3':
                    monster1.image = monster1.img_walk_right_3
                elif d[i*4+3] == '4':
                    monster1.image = monster1.img_walk_left_1
                elif d[i*4+3] == '5':
                    monster1.image = monster1.img_walk_left_2
                elif d[i*4+3] == '6':
                    monster1.image = monster1.img_walk_left_3
                elif d[i*4+3] == '7':
                    monster1.image = monster1.img_attack_left_1
                elif d[i*4+3] == '8':
                    monster1.image = monster1.img_attack_right_1
                elif d[i*4+3] == '9':
                    monster1.image = monster1.img_attack_left_2
                elif d[i*4+3] == '10':
                    monster1.image = monster1.img_attack_right_2
                elif d[i*4+3] == '11':
                    monster1.image = monster1.img_attack_left_3
                elif d[i*4+3] == '12':
                    monster1.image = monster1.img_attack_right_3
                elif d[i*4+3] == '13':
                    monster1.image = monster1.img_attack_right
                elif d[i*4+3] == '14':
                    monster1.image = monster1.img_attack_left
                monster1.draw()
            elif d[i*4] == '6':
                monster2.rect.x = float(d[i*4+1])
                monster2.rect.y = float(d[i*4+2])
                if d[i*4+3] == '1':
                    monster2.image = monster2.img_walk_right_1
                elif d[i*4+3] == '2':
                    monster2.image = monster2.img_walk_right_2
                elif d[i*4+3] == '3':
                    monster2.image = monster2.img_walk_right_3
                elif d[i*4+3] == '4':
                    monster2.image = monster2.img_walk_left_1
                elif d[i*4+3] == '5':
                    monster2.image = monster2.img_walk_left_2
                elif d[i*4+3] == '6':
                    monster2.image = monster2.img_walk_left_3
                elif d[i*4+3] == '7':
                    monster2.image = monster2.img_attack_left_1
                elif d[i*4+3] == '8':
                    monster2.image = monster2.img_attack_right_1
                elif d[i*4+3] == '9':
                    monster2.image = monster2.img_attack_left_2
                elif d[i*4+3] == '10':
                    monster2.image = monster2.img_attack_right_2
                elif d[i*4+3] == '11':
                    monster2.image = monster2.img_attack_left_3
                elif d[i*4+3] == '12':
                    monster2.image = monster2.img_attack_right_3
                elif d[i*4+3] == '13':
                    monster2.image = monster2.img_attack_right
                elif d[i*4+3] == '14':
                    monster2.image = monster2.img_attack_left
                monster2.draw()
            elif d[i * 4] == '7':
                throws1.rect.x = float(d[i * 4 + 1])
                throws1.rect.y = float(d[i * 4 + 2])
                if d[i * 4 + 3] == '1':
                    throws1.image = throws1.img_walk_right_1
                elif d[i * 4 + 3] == '2':
                    throws1.image = throws1.img_walk_right_2
                elif d[i * 4 + 3] == '3':
                    throws1.image = throws1.img_walk_left_1
                elif d[i * 4 + 3] == '4':
                    throws1.image = throws1.img_walk_left_2
                elif d[i * 4 + 3] == '5':
                    throws1.image = throws1.img_attack_left_1
                elif d[i * 4 + 3] == '6':
                    throws1.image = throws1.img_attack_right_1
                elif d[i * 4 + 3] == '7':
                    throws1.image = throws1.img_attack_left_2
                elif d[i * 4 + 3] == '8':
                    throws1.image = throws1.img_attack_right_2
                elif d[i * 4 + 3] == '9':
                    throws1.image = throws1.img_attack_left_3
                elif d[i * 4 + 3] == '10':
                    throws1.image = throws1.img_attack_right_3
                elif d[i * 4 + 3] == '11':
                    throws1.image = throws1.img_attack_right
                elif d[i * 4 + 3] == '12':
                    throws1.image = throws1.img_attack_left
                throws1.draw()
            elif d[i * 4] == '8':
                throws2.rect.x = float(d[i * 4 + 1])
                throws2.rect.y = float(d[i * 4 + 2])
                if d[i * 4 + 3] == '1':
                    throws2.image = throws2.img_walk_right_1
                elif d[i * 4 + 3] == '2':
                    throws2.image = throws2.img_walk_right_2
                elif d[i * 4 + 3] == '3':
                    throws2.image = throws2.img_walk_left_1
                elif d[i * 4 + 3] == '4':
                    throws2.image = throws2.img_walk_left_2
                elif d[i * 4 + 3] == '5':
                    throws2.image = throws2.img_attack_left_1
                elif d[i * 4 + 3] == '6':
                    throws2.image = throws2.img_attack_right_1
                elif d[i * 4 + 3] == '7':
                    throws2.image = throws2.img_attack_left_2
                elif d[i * 4 + 3] == '8':
                    throws2.image = throws2.img_attack_right_2
                elif d[i * 4 + 3] == '9':
                    throws2.image = throws2.img_attack_left_3
                elif d[i * 4 + 3] == '10':
                    throws2.image = throws2.img_attack_right_3
                elif d[i * 4 + 3] == '11':
                    throws2.image = throws2.img_attack_right
                elif d[i * 4 + 3] == '12':
                    throws2.image = throws2.img_attack_left
                throws2.draw()
            elif d[i * 4] == '9':
                stone1.rect.x = float(d[i * 4 + 1])
                stone1.rect.y = float(d[i * 4 + 2])
                if d[i * 4 + 3] == '1':
                    stone1.image = stone1.img_stone_left_1
                elif d[i * 4 + 3] == '2':
                    stone1.image = stone1.img_stone_left_2
                elif d[i * 4 + 3] == '3':
                    stone1.image = stone1.img_stone_left_3
                elif d[i * 4 + 3] == '4':
                    stone1.image = stone1.img_stone_left_4
                elif d[i * 4 + 3] == '5':
                    stone1.image = stone1.img_stone_right_1
                elif d[i * 4 + 3] == '6':
                    stone1.image = stone1.img_stone_right_2
                elif d[i * 4 + 3] == '7':
                    stone1.image = stone1.img_stone_right_3
                elif d[i * 4 + 3] == '8':
                    stone1.image = stone1.img_stone_right_4
                stone1.draw_bullet()
            elif d[i * 4] == '10':
                stone2.rect.x = float(d[i * 4 + 1])
                stone2.rect.y = float(d[i * 4 + 2])
                if d[i * 4 + 3] == '1':
                    stone2.image = stone2.img_stone_left_1
                elif d[i * 4 + 3] == '2':
                    stone2.image = stone2.img_stone_left_2
                elif d[i * 4 + 3] == '3':
                    stone2.image = stone2.img_stone_left_3
                elif d[i * 4 + 3] == '4':
                    stone2.image = stone2.img_stone_left_4
                elif d[i * 4 + 3] == '5':
                    stone2.image = stone2.img_stone_right_1
                elif d[i * 4 + 3] == '6':
                    stone2.image = stone2.img_stone_right_2
                elif d[i * 4 + 3] == '7':
                    stone2.image = stone2.img_stone_right_3
                elif d[i * 4 + 3] == '8':
                    stone2.image = stone2.img_stone_right_4
                stone2.draw_bullet()
            elif d[i * 4] == '13':
                boss.rect.x = float(d[i * 4 + 1])
                boss.rect.y = float(d[i * 4 + 2])
                if d[i * 4 + 3] == '1':
                    boss.image = boss.img_walk_right_1
                elif d[i * 4 + 3] == '2':
                    boss.image = boss.img_walk_right_2
                elif d[i * 4 + 3] == '3':
                    boss.image = boss.img_walk_left_1
                elif d[i * 4 + 3] == '4':
                    boss.image = boss.img_walk_left_2
                elif d[i * 4 + 3] == '5':
                    boss.image = boss.img_heng_attack_left_1
                elif d[i * 4 + 3] == '6':
                    boss.image = boss.img_heng_attack_right_1
                elif d[i * 4 + 3] == '7':
                    boss.image = boss.img_heng_attack_left_2
                elif d[i * 4 + 3] == '8':
                    boss.image = boss.img_heng_attack_right_2
                elif d[i * 4 + 3] == '9':
                    boss.image = boss.img_heng_attack_left_3
                elif d[i * 4 + 3] == '10':
                    boss.image = boss.img_heng_attack_right_3
                elif d[i * 4 + 3] == '11':
                    boss.image = boss.img_tian_attack_left_1
                elif d[i * 4 + 3] == '12':
                    boss.image = boss.img_tian_attack_right_1
                elif d[i * 4 + 3] == '13':
                    boss.image = boss.img_tian_attack_left_2
                elif d[i * 4 + 3] == '14':
                    boss.image = boss.img_tian_attack_right_2
                elif d[i * 4 + 3] == '15':
                    boss.image = boss.img_tian_attack_left_3
                elif d[i * 4 + 3] == '16':
                    boss.image = boss.img_tian_attack_right_3
                elif d[i * 4 + 3] == '17':
                    boss.image = boss.img_attack_left
                elif d[i * 4 + 3] == '18':
                    boss.image = boss.img_attack_right
                boss.draw()
            elif d[i * 4] == '14':
                arrow1.rect.x = float(d[i * 4 + 1])
                arrow1.rect.y = float(d[i * 4 + 2])
                if d[i * 4 + 3] == '1':
                    arrow1.image = arrow1.img_up
                elif d[i * 4 + 3] == '2':
                    arrow1.image = arrow1.img_down
                elif d[i * 4 + 3] == '3':
                    arrow1.image = arrow1.img_left
                elif d[i * 4 + 3] == '4':
                    arrow1.image = arrow1.img_right
                arrow1.draw()
            elif d[i * 4] == '15':
                arrow2.rect.x = float(d[i * 4 + 1])
                arrow2.rect.y = float(d[i * 4 + 2])
                if d[i * 4 + 3] == '1':
                    arrow2.image = arrow2.img_up
                elif d[i * 4 + 3] == '2':
                    arrow2.image = arrow2.img_down
                elif d[i * 4 + 3] == '3':
                    arrow2.image = arrow2.img_left
                elif d[i * 4 + 3] == '4':
                    arrow2.image = arrow2.img_right
                arrow2.draw()
            elif d[i * 4] == '16':
                arrow3.rect.x = float(d[i * 4 + 1])
                arrow3.rect.y = float(d[i * 4 + 2])
                if d[i * 4 + 3] == '1':
                    arrow3.image = arrow3.img_up
                elif d[i * 4 + 3] == '2':
                    arrow3.image = arrow3.img_down
                elif d[i * 4 + 3] == '3':
                    arrow3.image = arrow3.img_left
                elif d[i * 4 + 3] == '4':
                    arrow3.image = arrow3.img_right
                arrow3.draw()
            elif d[i * 4] == '17':
                arrow4.rect.x = float(d[i * 4 + 1])
                arrow4.rect.y = float(d[i * 4 + 2])
                if d[i * 4 + 3] == '1':
                    arrow4.image = arrow4.img_up
                elif d[i * 4 + 3] == '2':
                    arrow4.image = arrow4.img_down
                elif d[i * 4 + 3] == '3':
                    arrow4.image = arrow4.img_left
                elif d[i * 4 + 3] == '4':
                    arrow4.image = arrow4.img_right
                arrow4.draw()
            elif d[i * 4] == '18':
                bullet1.rect.x = float(d[i * 4 + 1])
                bullet1.rect.y = float(d[i * 4 + 2])
                if d[i*4+3] == '1':
                    bullet1.image = bullet1.img_2
                else:
                    bullet1.image = bullet1.img_3
                bullet1.draw_bullet()
            elif d[i * 4] == '19':
                bullet2.rect.x = float(d[i * 4 + 1])
                bullet2.rect.y = float(d[i * 4 + 2])
                if d[i*4+3] == '1':
                    bullet2.image = bullet2.img_2
                else:
                    bullet2.image = bullet2.img_3
                bullet2.draw_bullet()
            elif d[i * 4] == '20':
                bullet3.rect.x = float(d[i * 4 + 1])
                bullet3.rect.y = float(d[i * 4 + 2])
                if d[i*4+3] == '1':
                    bullet3.image = bullet3.img_2
                else:
                    bullet3.image = bullet3.img_3
                bullet3.draw_bullet()
            elif d[i * 4] == '21':
                bullet4.rect.x = float(d[i * 4 + 1])
                bullet4.rect.y = float(d[i * 4 + 2])
                if d[i*4+3] == '1':
                    bullet4.image = bullet4.img_2
                else:
                    bullet4.image = bullet4.img_3
                bullet4.draw_bullet()
            elif d[i * 4] == '22':
                bullet5.rect.x = float(d[i * 4 + 1])
                bullet5.rect.y = float(d[i * 4 + 2])
                if d[i*4+3] == '1':
                    bullet5.image = bullet5.img_2
                else:
                    bullet5.image = bullet5.img_3
                bullet5.draw_bullet()
            elif d[i * 4] == '23':
                alarm_light.rect.x = float(d[i*4+1])
                alarm_light.rect.y = float(d[i*4+2])
                alarm_light.draw()
            elif d[i * 4] == '24':
                end_game.rect.x = float(d[i*4+1])
                end_game.rect.y = float(d[i*4+2])
                if d[i*4+3] == '1':
                    end_game.image = end_game.img_victor
                else:
                    end_game.image = end_game.img_fail
            elif d[i * 4] == '25':
                play_button.draw_button()
            elif d[i * 4] == '26':
                houzi.blood = float(d[i*4+1])
                blood.update(houzi,ai_settings)
            elif d[i * 4] == '27':
                monster1.blood = float(d[i*4+1])
                monster1.blood_class.update_monster(monster1,ai_settings)
            elif d[i * 4] == '28':
                monster2.blood = float(d[i*4+1])
                monster2.blood_class.update_monster(monster2,ai_settings)
            elif d[i * 4] == '29':
                throws1.blood = float(d[i*4+1])
                throws1.blood_class.update_monster(throws1,ai_settings)
            elif d[i * 4] == '30':
                throws2.blood = float(d[i*4+1])
                throws2.blood_class.update_monster(throws2,ai_settings)
            elif d[i * 4] == '31':
                boss.blood = float(d[i*4+1])
                boss.blood_class.update_boss(boss,ai_settings)
            elif d[i*4] == '32':
                hou2.rect.x = float(d[i*4+1])
                hou2.rect.y = float(d[i*4+2])
                if d[i*4+3] == '1':
                    hou2.image = hou2.img_jingzhi_left
                elif d[i*4+3] == '2':
                    hou2.image = hou2.img_jingzhi_right
                elif d[i*4+3] == '3':
                    hou2.image = hou2.img_move_left2
                elif d[i*4+3] == '4':
                    hou2.image = hou2.img_move_right2
                elif d[i*4+3] == '5':
                    hou2.image = hou2.img_move_left
                elif d[i*4+3] == '6':
                    hou2.image = hou2.img_attack_left
                elif d[i*4+3] == '7':
                    hou2.image = hou2.img_attack_right
                elif d[i*4+3] == '8':
                    hou2.image = hou2.img_down
                elif d[i*4+3] == '9':
                    hou2.image = hou2.img_down_fan
                elif d[i*4+3] == '10':
                    hou2.image = hou2.img_jump
                elif d[i*4+3] == '11':
                    hou2.image = hou2.img_jump_fan
                hou2.draw()
            elif d[i*4] == '33':
                hou2.blood = float(d[i*4+1])
                blood.update(hou2,ai_settings)
        if(send_msg == ''):
            send_msg = 'o'
        elif send_msg != 'o':
            print(str(send_msg))
        update_screen(screen, ai_settings)
        sk.send(bytes(str(send_msg), 'utf8'))


def check_event(sk,houzi, monsters, throws, stairs, ai_settings, screen, bullets, stats, arrows, play_button, scene):
    # 监视鼠标和键盘事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            return '0'
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            reset_game(stats, arrows, bullets, ai_settings, houzi, stairs, monsters, throws, scene, screen)
        elif event.type == pygame.KEYDOWN:
            return keydown_events(sk,event, houzi, stairs, ai_settings, screen, bullets, stats)
        elif event.type == pygame.KEYUP:
            return keyup_events(sk,event, houzi,bullets,ai_settings,screen,stats)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            return check_play_button(sk,ai_settings, screen, stairs, stats, play_button, mouse_x, mouse_y, arrows, bullets, houzi,
                              monsters, throws, scene)
    return 'o'


def keydown_events(sk,event, houzi, stairs, ai_settings, screen, bullets, stats):
    '''猴子按下按键后的对策'''
    if event.key == pygame.K_RIGHT:
        return 'r'
    elif event.key == pygame.K_LEFT:
        return 'l'
    elif event.key == pygame.K_DOWN:
        return 'd'
    elif event.key == pygame.K_UP:
        return 'u'

    # 背景音乐键
    elif event.key == pygame.K_j:
        ai_settings.music_on = True
    elif event.key == pygame.K_k:
        ai_settings.music_on = False
    # 退出按键
    elif event.key == pygame.K_q:
        return '0'
        sys.exit()

    # 重置游戏按键
    elif event.key == pygame.K_r:
        stats.game_active = False
        # 打开光标
        pygame.mouse.set_visible(True)


def keyup_events(sk,event, houzi,bullets,ai_settings,screen,stats):
    '''抬起按键后的对策'''
    ###不抬按键就一直走##
    if event.key == pygame.K_RIGHT:
        return 'R'
    elif event.key == pygame.K_LEFT:
        return 'L'
        # 发射攻击光波
    elif event.key == pygame.K_SPACE:
        return 'k'



def check_play_button(sk,ai_settings, screen, stairs, stats, play_button, mouse_x, mouse_y, arrows, bullets, houzi,
                      monsters, throws, scene):
    '''在玩家单击play按钮时开始新游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        reset_game(stats, arrows, bullets, ai_settings, houzi, stairs, monsters, throws, scene, screen)

        print("send 1")
        return '1'

def reset_game(stats, arrows, bullets, ai_settings, houzi, stairs, monsters, throws, scene, screen):
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


def draw_wallpaper(screen, wallpaper_image):
    '''画贴纸'''
    wallpaper_rect = wallpaper_image.get_rect()
    screen_rect = screen.get_rect()
    wallpaper_rect.centerx = screen_rect.centerx
    wallpaper_rect.bottom = screen_rect.bottom
    '''绘制贴纸'''
    screen.blit(wallpaper_image, wallpaper_rect)


def check_music(ai_settings):
    if ai_settings.music_on:
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
    # 可能会有一点占内存！！！
    else:
        pygame.mixer.music.fadeout(500)


def update_screen(screen, ai_settings):
    pygame.display.flip()


def update_bullets(bullets):
    for bullet in bullets.sprites():
        # 更新子弹位置并绘制
        bullet.update()
        bullet.draw_bullet()
    # 删除已消失子弹
    for bullet in bullets.copy():
        if bullet.rect.left >= 1100 or bullet.rect.right < 0 or bullet.rect.bottom > 580 - 110:
            bullets.remove(bullet)


def update_stones(stones):
    for stone in stones.sprites():
        # 更新石头位置并绘制
        stone.update()
    # 删除已消失的石头
    for stone in stones.copy():
        if stone.rect.top > stone.min_bottom:
            stones.remove(stone)


def update_light(ai_settings, light_image, houzi, screen, arrows, alarm_light):
    if ai_settings.light:
        # 光相关 找到猴子的眼睛
        light_rect = light_image.get_rect()
        light_rect.centerx = houzi.rect.right - 34
        light_rect.centery = houzi.rect.top + 50
        screen.blit(light_image, light_rect)
        ai_settings.light -= 1

    for arrow in arrows:
        if (arrow.bearing == 1 or arrow.bearing == 2):
            alarm_light.image = alarm_light.img_alarm_light
            alarm_light.rect.centerx = arrow.target_pos
            alarm_light.draw()


def update_arrows(arrows, ai_settings, screen):
    for arrow in arrows.sprites():
        # 更新箭的位置
        arrow.update(ai_settings)
        arrow.draw()
    # 删除已消失箭
    for arrow in arrows.copy():
        if arrow.rect.left > ai_settings.screen_width or arrow.rect.right < 0 \
                or arrow.rect.top > ai_settings.screen_height:
            arrows.remove(arrow)


def update_stairs(stairs, monsters, throws, screen, ai_settings, scene):
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
    elif (len(throws) == 0 and scene[0] == 2):
        if (stairs.rect.centerx > stairs.screen_rect.right / 5):
            stairs.rect.centerx -= stairs.step
            stairs.moving = True
        else:
            stairs.moving = False
            scene[0] = 3

    stairs.draw()


def check_collision(houzi, monsters, arrows, stones, bullets, ai_settings, stats, blood):
    # 判断猴子与箭的碰撞,在houzi.update()中自动更新
    if pygame.sprite.spritecollideany(houzi, arrows) or pygame.sprite.spritecollideany(houzi, stones):
        houzi.attacked = True
        houzi.attacked_time = ai_settings.attacked_time / 5
        for stone in stones:
            if (pygame.sprite.collide_rect(houzi, stone)):
                houzi.bearing = not stone.bearing
    else:
        houzi.attacked = False
    # 判断猴子是否相撞一次(防止串糖葫芦一直掉血)
    if ai_settings.last_state != houzi.attacked:
        ai_settings.collision += 1
        if ai_settings.collision % 2 == 0:
            if ai_settings.blood > 0:
                ai_settings.blood -= 1
            else:
                ai_settings.blood = 0
                # 加载血条
                blood.update(houzi, ai_settings)
                # 游戏失败
                stats.game_active = False
                ai_settings.victor = 1
                # 打开光标
                pygame.mouse.set_visible(True)
    ai_settings.last_state = houzi.attacked

    # 判断猴子的光波与怪物的碰撞
    check_collision_light_monster(houzi, monsters, bullets)

    # 判断光波与箭的碰撞,并自动删除
    pygame.sprite.groupcollide(bullets, arrows, True, True)


def check_monster_houzi_attack(houzi, monsters, ai_settings, stats, blood):
    for monster in monsters:
        if (monster.fight == ai_settings.attacked_time / 2):
            if abs(
                    monster.rect.centerx - houzi.rect.centerx) <= monster.fight_length and monster.rect.bottom == houzi.rect.bottom:
                houzi.attacked = True
                houzi.attacked_time = ai_settings.attacked_time / 2
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


def check_collision_light_monster(houzi, monsters, bullets):
    # 判断猴子的光波与怪物（猩猩/投石怪）的碰撞
    for monster in monsters.copy():
        if pygame.sprite.spritecollideany(monster, bullets):
            monster.keep_attacked = monster.attacked_time
            for bullet in bullets.copy():
                if (pygame.sprite.collide_rect(monster, bullet)):
                    bullets.remove(bullet)
                    # 怪物的掉血
                    if monster.blood - houzi.force > 0:
                        monster.blood -= houzi.force
                    else:
                        # 怪物死了
                        monsters.remove(monster)


def check_collision_boss(houzi, boss, arrows, bullets, ai_settings, stats, blood):
    # 判断猴子与箭的碰撞,在houzi.update()中自动更新
    if pygame.sprite.spritecollideany(houzi, arrows):
        houzi.attacked = True
        houzi.attacked_time = ai_settings.attacked_time / 5
        for arrow in arrows:
            if (pygame.sprite.collide_rect(houzi, arrow)):
                if (arrow.bearing == 3):
                    houzi.bearing = False
                else:
                    houzi.bearing = True
    else:
        houzi.attacked = False
    # 判断猴子是否相撞一次(防止串糖葫芦一直掉血)
    if ai_settings.last_state != houzi.attacked:
        ai_settings.collision += 1
        if ai_settings.collision % 2 == 0:
            if ai_settings.blood - boss.force > 0:
                ai_settings.blood -= boss.force
            else:
                # 把残血显示出来
                ai_settings.blood = 0
                # 加载血条
                blood.update(houzi, ai_settings)
                # 游戏失败
                stats.game_active = False
                ai_settings.victor = 1
                # 打开光标
                pygame.mouse.set_visible(True)
    ai_settings.last_state = houzi.attacked

    # 判断猴子的光波与boss的撞击
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

# 连接服务器
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("等待连接服务器...")
try:
    sk.connect((server_ip, 79))
    #sk.connect(('127.0.0.1', 79))
    print("连接服务器成功!")
except ConnectionRefusedError:
    print('-' * 10 + '服务器未上线，或者不存在' + '-' * 10)
    exit()

run_game()


sk.close()
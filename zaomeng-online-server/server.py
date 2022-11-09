 # -*- coding: utf-8 -*
import socket
import _thread as thread
import sys
import pygame
import os
from arrow import Arrow
from game_stats import GameStats
from button import Button
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
from screen import Screen
from pygame.sprite import Group
from alarm_light import Alarm_light


def rec_data1():
    global data1
    try:
        temp = connect1.recv(1024)
        return(str(temp, 'utf8'))
    except:
        print('-' * 10 + 'client1 offline' + '-' * 10)
        sys.exit()

def rec_data2():
    global data2
    try:
        temp = connect2.recv(1024)
        return (str(temp, 'utf8'))
    except:
        print('-' * 10 + 'client2 offline' + '-' * 10)
        sys.exit()

def run_game():
    pygame.init()
    #pygame.mixer.init()
    ai_settings = Settings()
    screen = Screen()
    '''游戏开始'''
    stats = GameStats(ai_settings)
    '''背景图片'''
    wallpaper_image = pygame.image.load("./images/beijing.png")
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
    throws = []
    monsters = []
    # monsters.append(Monster(screen,ai_settings))
    # monsters.append(Monster(screen,ai_settings,100))
    '''创建Boss'''
    boss = Boss(screen, ai_settings)
    '''创建血条'''
    blood = Blood(screen, ai_settings)
    '''创建光波编组'''
    bullets = Group()
    '''创建箭'''
    arrows = Group()
    '''创建箭的提示区'''
    alarm_light = Alarm_light(screen)
    '''创建石头'''
    stones = Group()
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
    pygame.display.set_caption("server-cxy")
    #让每个操作只反馈一次
    last_data1 = ''
    last_data2 = ''
    thread.start_new_thread(rec_data1, ())
    thread.start_new_thread(rec_data2, ())
    while True:
        data1 = rec_data1()
        data2 = rec_data2()
        print(data1,'---')
        print(data2,'---')
        for rev_data1 in data1:
            #print(rev_data1)
            if( rev_data1 == '1'):
                reset_game(stats, arrows, bullets, ai_settings, houzi,hou2, stairs, monsters, throws, scene, screen,boss)
            if(rev_data1 == '0'):
                sys.exit()
            elif (rev_data1 == 'r'):
                houzi.forward = True
            elif (rev_data1 == 'l'):
                houzi.backward = True
            elif (rev_data1 == 'd'):
                if (houzi.rect.bottom < stairs.rect.centery) and (houzi.rect.bottom > stairs.rect.top + 45):
                    houzi.down = True
            elif (rev_data1 == 'u'):
                if stats.game_active:
                    if not houzi.down:
                        houzi.jump = True
                    if not houzi.jump_down == True:
                        houzi.jump_up = True
            elif (rev_data1 == 'k'):
                if len(bullets) < ai_settings.bullets_allowed:
                    new_bullet = Bullet(ai_settings, screen, houzi)
                    bullets.add(new_bullet)
                    ai_settings.light = 8  # 放光的延时
            elif(rev_data1 == 'R'):
                houzi.forward = False
            elif(rev_data1 == 'L'):
                houzi.backward = False

        for rev_data2 in data2:
            #print(rev_data1)
            if( rev_data2 == '1') :
                reset_game(stats, arrows, bullets, ai_settings, houzi,hou2, stairs, monsters, throws, scene, screen,boss)
            if(rev_data2 == '0'):
                sys.exit()
            elif (rev_data2 == 'r'):
                hou2.forward = True
            elif (rev_data2 == 'l'):
                hou2.backward = True
            elif (rev_data2 == 'd'):
                if (hou2.rect.bottom < stairs.rect.centery) and (hou2.rect.bottom > stairs.rect.top + 45):
                    hou2.down = True
            elif (rev_data2 == 'u'):
                if stats.game_active:
                    if not hou2.down:
                        hou2.jump = True
                    if not hou2.jump_down == True:
                        hou2.jump_up = True
            elif (rev_data2 == 'k'):
                if len(bullets) < ai_settings.bullets_allowed:
                    new_bullet = Bullet(ai_settings, screen, hou2)
                    bullets.add(new_bullet)
                    ai_settings.light = 8  # 放光的延时
            elif(rev_data2 == 'R'):
                hou2.forward = False
            elif(rev_data2 == 'L'):
                hou2.backward = False

        #check_event(houzi, monsters, throws, stairs, ai_settings, screen, bullets, stats, arrows, play_button, scene)
        trans_data = ''
        # 没按开始键
        if not stats.game_active:
            draw_wallpaper(screen, wallpaper_image)
            #starits
            stairs.draw()
            trans_data +='2'+'*'+str(stairs.rect.x)+'*'+str(stairs.rect.y)+'*'+'0'+'*'
            #road
            road.draw()
            trans_data +='3'+'*'+str(road.rect1.x)+'*'+str(road.rect1.y)+'*'+'0'+'*'
            trans_data +='4'+'*'+ str(road.rect2.x)+'*'+str(road.rect2.y)+'*'+'0'+'*'
            if (ai_settings.victor == 1):
                end_game.draw_fail()
                trans_data += '24'+'*'+str(end_game.rect.x)+'*'+str(end_game.rect.y)+'*'+'2'+'*'
            elif (ai_settings.victor == 2):
                end_game.draw_victor()
                trans_data += '24' + '*' + str(end_game.rect.x) + '*' + str(end_game.rect.y) + '*' + '1'+'*'
            for i in range(len(monsters)):
                monsters[i].draw()
                trans_data += str(5+i) + '*' + str(monsters[i].rect.x) + '*' + str(monsters[i].rect.y) + '*'
                if monsters[i].image == monsters[i].img_walk_right_1:
                    trans_data += '1'+'*'
                elif monsters[i].image == monsters[i].img_walk_right_2:
                    trans_data += '2'+'*'
                elif monsters[i].image == monsters[i].img_walk_right_3:
                    trans_data += '3'+'*'
                elif monsters[i].image == monsters[i].img_walk_left_1:
                    trans_data += '4'+'*'
                elif monsters[i].image == monsters[i].img_walk_left_2:
                    trans_data += '5'+'*'
                elif monsters[i].image == monsters[i].img_walk_left_3:
                    trans_data += '6'+'*'
                elif monsters[i].image == monsters[i].img_attack_left_1:
                    trans_data += '7'+'*'
                elif monsters[i].image == monsters[i].img_attack_right_1:
                    trans_data += '8'+'*'
                elif monsters[i].image == monsters[i].img_attack_left_2:
                    trans_data += '9'+'*'
                elif monsters[i].image == monsters[i].img_attack_right_2:
                    trans_data += '10'+'*'
                elif monsters[i].image == monsters[i].img_attack_left_3:
                    trans_data += '11'+'*'
                elif monsters[i].image == monsters[i].img_attack_right_3:
                    trans_data += '12'+'*'
                elif monsters[i].image == monsters[i].img_attack_right:
                    trans_data += '13'+'*'
                elif monsters[i].image == monsters[i].img_attack_left:
                    trans_data += '14'+'*'
                trans_data += str(i+27)+'*'+str(monsters[i].blood)+'*'+'-1'+'*'+'-1'+'*'

            #猴子
            houzi.draw()
            trans_data += '1' + '*' + str(houzi.rect.x) + '*' + str(houzi.rect.y) + '*'
            if (houzi.image == houzi.img_jingzhi_left):
                trans_data += '1' + '*'
            elif houzi.image == houzi.img_jingzhi_right:
                trans_data += '2' + '*'
            elif houzi.image == houzi.img_move_left2:
                trans_data += '3' + '*'
            elif houzi.image == houzi.img_move_right2:
                trans_data += '4' + '*'
            elif houzi.image == houzi.img_move_left:
                trans_data += '5' + '*'
            elif houzi.image == houzi.img_attack_left:
                trans_data += '6' + '*'
            elif houzi.image == houzi.img_attack_right:
                trans_data += '7' + '*'
            elif houzi.image == houzi.img_down:
                trans_data += '8' + '*'
            elif houzi.image == houzi.img_down_fan:
                trans_data += '9' + '*'
            elif houzi.image == houzi.img_jump:
                trans_data += '10' + '*'
            elif houzi.image == houzi.img_jump_fan:
                trans_data += '11' + '*'
            #绘制猴2
            hou2.draw()
            trans_data += '32' + '*' + str(hou2.rect.x) + '*' + str(hou2.rect.y) + '*'
            if (hou2.image == hou2.img_jingzhi_left):
                trans_data += '1' + '*'
            elif hou2.image == hou2.img_jingzhi_right:
                trans_data += '2' + '*'
            elif hou2.image == hou2.img_move_left2:
                trans_data += '3' + '*'
            elif hou2.image == hou2.img_move_right2:
                trans_data += '4' + '*'
            elif hou2.image == hou2.img_move_left:
                trans_data += '5' + '*'
            elif hou2.image == hou2.img_attack_left:
                trans_data += '6' + '*'
            elif hou2.image == hou2.img_attack_right:
                trans_data += '7' + '*'
            elif hou2.image == hou2.img_down:
                trans_data += '8' + '*'
            elif hou2.image == hou2.img_down_fan:
                trans_data += '9' + '*'
            elif hou2.image == hou2.img_jump:
                trans_data += '10' + '*'
            elif hou2.image == hou2.img_jump_fan:
                trans_data += '11' + '*'

            play_button.draw_button()
            trans_data += '25' + '*' + '0' + '*' + '0' + '*' +'0'+'*'
            blood.update(houzi, ai_settings)
            trans_data += '26'+ '*' + str(houzi.blood)+'*'+'0'+'*'+'0'+'*'
            blood.update(hou2, ai_settings)
            trans_data += '33' + '*' + str(hou2.blood) + '*' + '0' + '*' + '0' + '*'
        # 开始游戏
        else:
            draw_wallpaper(screen, wallpaper_image)
            #stairs
            update_stairs(stairs, monsters, throws, screen, ai_settings, scene)
            trans_data += '2' + '*' + str(stairs.rect.x) + '*' + str(stairs.rect.y) + '*' + '0' + '*'

            road.update(stairs)
            trans_data +='3'+'*'+str(road.rect1.x)+'*'+str(road.rect1.y)+'*'+'0'+'*'
            trans_data +='4'+'*'+ str(road.rect2.x)+'*'+str(road.rect2.y)+'*'+'0'+'*'
            if scene[0] == 1:
                for i in range(len(monsters)):
                    monsters[i].update(houzi, ai_settings)
                    trans_data += str(5 + i) + '*' + str(monsters[i].rect.x) + '*' + str(monsters[i].rect.y) + '*'
                    if monsters[i].image == monsters[i].img_walk_right_1:
                        trans_data += '1' + '*'
                    elif monsters[i].image == monsters[i].img_walk_right_2:
                        trans_data += '2' + '*'
                    elif monsters[i].image == monsters[i].img_walk_right_3:
                        trans_data += '3' + '*'
                    elif monsters[i].image == monsters[i].img_walk_left_1:
                        trans_data += '4' + '*'
                    elif monsters[i].image == monsters[i].img_walk_left_2:
                        trans_data += '5' + '*'
                    elif monsters[i].image == monsters[i].img_walk_left_3:
                        trans_data += '6' + '*'
                    elif monsters[i].image == monsters[i].img_attack_left_1:
                        trans_data += '7' + '*'
                    elif monsters[i].image == monsters[i].img_attack_right_1:
                        trans_data += '8' + '*'
                    elif monsters[i].image == monsters[i].img_attack_left_2:
                        trans_data += '9' + '*'
                    elif monsters[i].image == monsters[i].img_attack_right_2:
                        trans_data += '10' + '*'
                    elif monsters[i].image == monsters[i].img_attack_left_3:
                        trans_data += '11' + '*'
                    elif monsters[i].image == monsters[i].img_attack_right_3:
                        trans_data += '12' + '*'
                    elif monsters[i].image == monsters[i].img_attack_right:
                        trans_data += '13' + '*'
                    elif monsters[i].image == monsters[i].img_attack_left:
                        trans_data += '14' + '*'
                    trans_data += str(i + 27) + '*' + str(monsters[i].blood) + '*' + '-1' + '*' + '-1' + '*'

                # 检测怪物是否攻击到猴子了
                check_monster_houzi_attack(houzi, monsters, ai_settings, stats, blood)
                check_monster_houzi_attack(hou2, monsters, ai_settings, stats, blood)
                # 检测猴子与箭、光波与箭的碰撞
                check_collision(houzi, monsters, arrows, stones, bullets, ai_settings, stats, blood)
                check_collision(hou2, monsters, arrows, stones, bullets, ai_settings, stats, blood)
            elif scene[0] == 2:
                for i in range(len(throws)):
                    throws[i].update(houzi, ai_settings, stones, screen)
                    trans_data += str(7+i) + '*' + str(throws[i].rect.x) + '*' + str(throws[i].rect.y) + '*'
                    if throws[i].image == throws[i].img_walk_right_1:
                        trans_data += '1'+'*'
                    elif throws[i].image == throws[i].img_walk_right_2:
                        trans_data += '2'+'*'
                    elif throws[i].image == throws[i].img_walk_left_1:
                        trans_data += '3'+'*'
                    elif throws[i].image == throws[i].img_walk_left_2:
                        trans_data += '4'+'*'
                    elif throws[i].image == throws[i].img_attack_left_1:
                        trans_data += '5'+'*'
                    elif throws[i].image == throws[i].img_attack_right_1:
                        trans_data += '6'+'*'
                    elif throws[i].image == throws[i].img_attack_left_2:
                        trans_data += '7'+'*'
                    elif throws[i].image == throws[i].img_attack_right_2:
                        trans_data += '8'+'*'
                    elif throws[i].image == throws[i].img_attack_left_3:
                        trans_data += '9'+'*'
                    elif throws[i].image == throws[i].img_attack_right_3:
                        trans_data += '10'+'*'
                    elif throws[i].image == throws[i].img_attack_right:
                        trans_data += '11'+'*'
                    elif throws[i].image == throws[i].img_attack_left:
                        trans_data += '12'+'*'
                    trans_data += str(i + 29) + '*' + str(throws[i].blood) + '*' + '0' + '*' + '0' + '*'

                update_stones(stones)
                index = 0
                for stone in stones.sprites():
                    trans_data += str(9 + index) + '*' + str(stone.rect.x) + '*' + str(stone.rect.y) + '*'
                    # 绘制不同方向的光波
                    if stone.image == stone.img_stone_left_1:
                        trans_data += '1' + '*'
                    elif stone.image == stone.img_stone_left_2:
                        trans_data += '2' + '*'
                    elif stone.image == stone.img_stone_left_3:
                        trans_data += '3' + '*'
                    elif stone.image == stone.img_stone_left_4:
                        trans_data += '4' + '*'
                    elif stone.image == stone.img_stone_right_1:
                        trans_data += '5' + '*'
                    elif stone.image == stone.img_stone_right_2:
                        trans_data += '6' + '*'
                    elif stone.image == stone.img_stone_right_3:
                        trans_data += '7' + '*'
                    elif stone.image == stone.img_stone_right_4:
                        trans_data += '8' + '*'
                    index += 1
                # 检测猴子与箭、光波与箭的碰撞
                check_collision(houzi, throws, arrows, stones, bullets, ai_settings, stats, blood)
                check_collision(hou2, throws, arrows, stones, bullets, ai_settings, stats, blood)
            elif scene[0] == 3:
                boss.update(houzi, ai_settings, arrows, screen)
                trans_data += str(13) + '*' + str(boss.rect.x) + '*' + str(boss.rect.y) + '*'
                if boss.image == boss.img_walk_right_1:
                    trans_data += '1'+'*'
                elif boss.image == boss.img_walk_right_2:
                    trans_data += '2'+'*'
                elif boss.image == boss.img_walk_left_1:
                    trans_data += '3'+'*'
                elif boss.image == boss.img_walk_left_2:
                    trans_data += '4'+'*'
                elif boss.image == boss.img_heng_attack_left_1:
                    trans_data += '5'+'*'
                elif boss.image == boss.img_heng_attack_right_1:
                    trans_data += '6'+'*'
                elif boss.image == boss.img_heng_attack_left_2:
                    trans_data += '7'+'*'
                elif boss.image == boss.img_heng_attack_right_2:
                    trans_data += '8'+'*'
                elif boss.image == boss.img_heng_attack_left_3:
                    trans_data += '9'+'*'
                elif boss.image == boss.img_heng_attack_right_3:
                    trans_data += '10'+'*'
                elif boss.image == boss.img_tian_attack_left_1:
                    trans_data += '11'+'*'
                elif boss.image == boss.img_tian_attack_right_1:
                    trans_data += '12'+'*'
                elif boss.image == boss.img_tian_attack_left_2:
                    trans_data += '13'+'*'
                elif boss.image == boss.img_tian_attack_right_2:
                    trans_data += '14'+'*'
                elif boss.image == boss.img_tian_attack_left_3:
                    trans_data += '15'+'*'
                elif boss.image == boss.img_tian_attack_right_3:
                    trans_data += '16'+'*'
                elif boss.image == boss.img_attack_left:
                    trans_data += '17'+'*'
                elif boss.image == boss.img_attack_right:
                    trans_data += '18'+'*'
                trans_data += str(31) + '*' + str(boss.blood) + '*' + '0' + '*' + '0' + '*'
                update_arrows(arrows, ai_settings, screen)
                index = 0
                for arrow in arrows.sprites():
                    trans_data += str(14 + index) + '*' + str(arrow.rect.x) + '*' + str(arrow.rect.y) + '*'
                    # 绘制不同方向的光波
                    if arrow.image == arrow.img_up:
                        trans_data += '1' + '*'
                    elif arrow.image == arrow.img_down:
                        trans_data += '2' + '*'
                    elif arrow.image == arrow.img_left:
                        trans_data += '3' + '*'
                    elif arrow.image == arrow.img_right :
                        trans_data += '4' + '*'
                    index += 1
                check_collision_boss(houzi, boss, arrows, bullets, ai_settings, stats, blood)
                check_collision_boss(hou2, boss, arrows, bullets, ai_settings, stats, blood)
                boss_name.draw_boss()

            #猴子
            houzi.update(stairs)
            trans_data += '1' + '*' + str(houzi.rect.x) + '*' + str(houzi.rect.y) + '*'
            if (houzi.image == houzi.img_jingzhi_left):
                trans_data += '1' + '*'
            elif houzi.image == houzi.img_jingzhi_right:
                trans_data += '2' + '*'
            elif houzi.image == houzi.img_move_left2:
                trans_data += '3' + '*'
            elif houzi.image == houzi.img_move_right2:
                trans_data += '4' + '*'
            elif houzi.image == houzi.img_move_left:
                trans_data += '5' + '*'
            elif houzi.image == houzi.img_attack_left:
                trans_data += '6' + '*'
            elif houzi.image == houzi.img_attack_right:
                trans_data += '7' + '*'
            elif houzi.image == houzi.img_down:
                trans_data += '8' + '*'
            elif houzi.image == houzi.img_down_fan:
                trans_data += '9' + '*'
            elif houzi.image == houzi.img_jump:
                trans_data += '10' + '*'
            elif houzi.image == houzi.img_jump_fan:
                trans_data += '11' + '*'
            #猴2
            hou2.update(stairs)
            trans_data += '32' + '*' + str(hou2.rect.x) + '*' + str(hou2.rect.y) + '*'
            if (hou2.image == hou2.img_jingzhi_left):
                trans_data += '1' + '*'
            elif hou2.image == hou2.img_jingzhi_right:
                trans_data += '2' + '*'
            elif hou2.image == hou2.img_move_left2:
                trans_data += '3' + '*'
            elif hou2.image == hou2.img_move_right2:
                trans_data += '4' + '*'
            elif hou2.image == hou2.img_move_left:
                trans_data += '5' + '*'
            elif hou2.image == hou2.img_attack_left:
                trans_data += '6' + '*'
            elif hou2.image == hou2.img_attack_right:
                trans_data += '7' + '*'
            elif hou2.image == hou2.img_down:
                trans_data += '8' + '*'
            elif hou2.image == hou2.img_down_fan:
                trans_data += '9' + '*'
            elif hou2.image == hou2.img_jump:
                trans_data += '10' + '*'
            elif hou2.image == hou2.img_jump_fan:
                trans_data += '11' + '*'

            # 加载血条
            blood.update(houzi, ai_settings)
            trans_data += '26' + '*' + str(houzi.blood) + '*' + '0' + '*' + '0' + '*'
            blood.update(hou2, ai_settings)
            trans_data += '33' + '*' + str(hou2.blood) + '*' + '0' + '*' + '0' + '*'
            update_bullets(bullets)
            #加载子弹
            index = 0
            for bullet in bullets.sprites():
                trans_data += str(18+index) + '*' + str(bullet.rect.x) + '*' + str(bullet.rect.y) + '*'
                # 绘制不同方向的光波
                if not bullet.bearing:
                    trans_data += '1' + '*'
                else:
                    trans_data += '2' + '*'
                index += 1
            # 光
            update_light(ai_settings, light_image, houzi, screen, arrows, alarm_light)
            update_light(ai_settings, light_image, hou2, screen, arrows, alarm_light)
            for arrow in arrows.sprites():
                if(arrow.bearing == 1 or arrow.bearing == 2):
                    trans_data += '23' + '*' + str(alarm_light.rect.x) + '*' + str(alarm_light.rect.y) + '*' + '0'
            #check_music(ai_settings)

        update_screen(screen, ai_settings)
        connect1.send(bytes(trans_data, 'utf8'))
        connect2.send(bytes(trans_data, 'utf8'))
        #print(trans_data)

def check_event(houzi, monsters, throws, stairs, ai_settings, screen, bullets, stats, arrows, play_button, scene,boss):
    # 监视鼠标和键盘事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            reset_game(stats, arrows, bullets, ai_settings, houzi, stairs, monsters, throws, scene, screen)
        elif event.type == pygame.KEYDOWN:
            keydown_events(event, houzi, stairs, ai_settings, screen, bullets, stats)
        elif event.type == pygame.KEYUP:
            keyup_events(event, houzi)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stairs, stats, play_button, mouse_x, mouse_y, arrows, bullets, houzi,
                              monsters, throws, scene,boss)


def keydown_events(event, houzi, stairs, ai_settings, screen, bullets, stats):
    '''猴子按下按键后的对策'''
    if event.key == pygame.K_RIGHT:
        houzi.forward = True
    elif event.key == pygame.K_LEFT:
        houzi.backward = True
    elif event.key == pygame.K_DOWN:
        if (houzi.rect.bottom < stairs.rect.centery) and (houzi.rect.bottom > stairs.rect.top + 45):
            houzi.down = True
    elif event.key == pygame.K_UP and stats.game_active:
        if not houzi.down:
            houzi.jump = True
        if not houzi.jump_down == True:
            houzi.jump_up = True
    # 背景音乐键
    elif event.key == pygame.K_j:
        ai_settings.music_on = True
    elif event.key == pygame.K_k:
        ai_settings.music_on = False
        # 发射攻击光波
    elif event.key == pygame.K_SPACE:
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, houzi)
            bullets.add(new_bullet)
            ai_settings.light = 8  # 放光的延时
    # 退出按键
    elif event.key == pygame.K_q:
        sys.exit()
    # 重置游戏按键
    elif event.key == pygame.K_r:
        stats.game_active = False
        # 打开光标
        #pygame.mouse.set_visible(True)


def keyup_events(event, houzi):
    '''抬起按键后的对策'''
    ###不抬按键就一直走##
    if event.key == pygame.K_RIGHT:
        houzi.forward = False
    elif event.key == pygame.K_LEFT:
        houzi.backward = False


def check_play_button(ai_settings, screen, stairs, stats, play_button, mouse_x, mouse_y, arrows, bullets, houzi,
                      monsters, throws, scene,boss):
    '''在玩家单击play按钮时开始新游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        reset_game(stats, arrows, bullets, ai_settings, houzi,houzi, stairs, monsters, throws, scene, screen,boss)


def reset_game(stats, arrows, bullets, ai_settings, houzi,hou2, stairs, monsters, throws, scene, screen,boss):
    # 隐藏光标
    #pygame.mouse.set_visible(False)
    stats.game_active = True
    # 清空光波列表和箭列表
    arrows.empty()
    bullets.empty()
    # 重新加载设置
    ai_settings.reset()
    # 猴子归位
    houzi.reset()
    hou2.reset()
    boss.reset(ai_settings)
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
    pass
    '''绘制贴纸'''
    #screen.blit(wallpaper_image, wallpaper_rect)


def check_music(ai_settings):
    if ai_settings.music_on:
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
    # 可能会有一点占内存！！！
    else:
        pygame.mixer.music.fadeout(500)


def update_screen(screen, ai_settings):
    #pygame.display.flip()
    pass


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
        #screen.blit(light_image, light_rect)
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
    if houzi.last_state != houzi.attacked:
        houzi.collision += 1
        if houzi.collision % 2 == 0:
            if houzi.blood > 0:
                houzi.blood -= 1
            else:
                houzi.blood = 0
                # 加载血条
                blood.update(houzi, ai_settings)
                # 游戏失败
                stats.game_active = False
                ai_settings.victor = 1
                # 打开光标
                #pygame.mouse.set_visible(True)
    houzi.last_state = houzi.attacked

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
                if houzi.blood - ai_settings.monster_force > 0:
                    houzi.blood -= ai_settings.monster_force
                else:
                    houzi.blood = 0
                    # 加载血条
                    blood.update(houzi, ai_settings)
                    # 游戏失败
                    stats.game_active = False
                    ai_settings.victor = 1
                    # 打开光标
                    #pygame.mouse.set_visible(True)


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
    if houzi.last_state != houzi.attacked:
        houzi.collision += 1
        if houzi.collision % 2 == 0:
            if houzi.blood - boss.force > 0:
                houzi.blood -= boss.force
            else:
                # 把残血显示出来
                houzi.blood = 0
                # 加载血条
                blood.update(houzi, ai_settings)
                # 游戏失败
                stats.game_active = False
                ai_settings.victor = 1
                # 打开光标
                #pygame.mouse.set_visible(True)
    houzi.last_state = houzi.attacked

    # 判断猴子的光波与boss的撞击
    if pygame.sprite.spritecollideany(boss, bullets):
        boss.keep_attacked = boss.attacked_time/6
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
                    #pygame.mouse.set_visible(True)

sk=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address=('',79)
sk.bind(address)
sk.listen(-1)

print('等待客户端链接' + '.' * 20)
connect1, client1 = sk.accept()
print(str(client1)+'上线')
connect2, client2 = sk.accept()
print(str(client2)+'上线')
run_game()

sk.close()

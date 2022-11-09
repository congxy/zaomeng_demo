 # -*- coding: utf-8 -*
class Settings():
    '''基本设置'''

    def __init__(self):
        self.screen_width = 1100
        self.screen_height = 580
        self.bg_color = (230, 230, 230)
        self.music_on = False
        self.music_off = False
        # 放光的延时
        self.light = 0
        # 光波设置
        self.bullets_allowed = 3
        self.bullet_speed_factor = 6.4
        # 相撞判断
        self.collision = 0
        self.last_state = True
        # 箭设置
        self.arrows_allowed = 0
        self.arrow_speed_factor = 20
        # 箭的加速度
        self.arrow_acceleration = 2.0
        # 血条背景框
        self.blood_background_height = 12
        self.blood_background_width = 100
        self.blood_background_monster_width = 50
        self.blood_background_boss_width = 500
        self.blood_background_color = (192, 192, 192)
        # 血条
        self.blood_height = 12
        self.blood_width = 10
        self.blood_color = (255, 0, 0)
        self.blood_monster_height = 12
        self.blood_monster_width = 10
        self.blood_boss_height = 12
        self.blood_boss_width = 10
        self.monster_blood_color = (255, 165, 0)
        self.boss_blood_color = (255, 0, 0)
        # 血条的边框
        self.backback_color = (0, 0, 0)
        # 攻击力
        self.monster_force = 2
        self.throw_force = 1
        self.boss_force = 5
        self.force = 1
        # 怪物被攻击的冷冻时间（帧）
        self.attacked_time = 6
        self.attacked_boss_time = 2
        # 怪物攻击的冷却时间（帧）
        self.fight_time = 6
        # 怪物攻击半径
        self.fight_length = 30
        # 重置
        self.reset()
        # 上一次的成功失败状态,0代表没有状态，1代表失败，2代表成功
        self.victor = 0

    def reset(self):
        # 重启游戏后的设置
        # 生命值
        self.blood = 10
        # 已躲过箭的数量（记录的得分用）
        self.arrow_number = 0

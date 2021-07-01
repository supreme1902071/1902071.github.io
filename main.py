import pygame
import sys
import traceback
from pygame.locals import *
import MyPlane
import enemy
import bullet
import supply
import pygame
from random import *

pygame.init() # 初始化 display 模块
pygame.mixer.init() # 初始化音乐(混合音)

bg_size = width, height = 480, 700 #背景大小
screen = pygame.display.set_mode(bg_size) # 初始化一个准备显示的窗口或屏幕
pygame.display.set_caption("飞机大战 -- 一人 Demo") # 设置标题

background = pygame.image.load("images/background.png").convert()

BLACK = (0, 0, 0)  # 敌机血槽颜色
GREEN = (0, 255, 0)
RED = (255, 0 , 0)
WHITE = (255, 255 ,255)

# 载入游戏音乐
pygame.mixer.music.load('sound/game_music.ogg')
pygame.mixer.music.set_volume(0.2)

bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)

bomb_sound = pygame.mixer.Sound('sound/use_bomb.wav')
bomb_sound.set_volume(0.2)

supply_sound = pygame.mixer.Sound('sound/supply.wav')
supply_sound.set_volume(0.2)

get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
get_bomb_sound.set_volume(0.2)

get_bullet_sound = pygame.mixer.Sound('sound/get_bullet.wav')
get_bullet_sound.set_volume(0.2)

upgrade_sound = pygame.mixer.Sound('sound/upgrade.wav')
upgrade_sound.set_volume(0.2)

enemy3_fly_sound = pygame.mixer.Sound('sound/enemy3_flying.wav')
enemy3_fly_sound.set_volume(0.6)

enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.2)

enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
enemy2_down_sound.set_volume(0.2)

enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.2)

me_down_sound = pygame.mixer.Sound('sound/me_down.wav')
me_down_sound.set_volume(0.2)

def add_small_enemies(group1, group2, num): # 创建小飞机函数
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size) # 创建一个小飞机对象
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num): # 创建中飞机函数
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size) # 创建一个中飞机对象
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1, group2, num): # 创建大飞机函数
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size) # 创建一个大飞机对象
        group1.add(e3)
        group2.add(e3)

def inc_speed(target, inc): # 每个对象都增加相应的速度
    for each in target:
        each.speed += inc

def main():
    pygame.mixer.music.play(-1) #加载背景音乐

    # 生成我方飞机
    me = MyPlane.MyPlane(bg_size)

    enemies = pygame.sprite.Group() # 所有敌机都放在enemies序列中

    # 生成敌方小飞机
    small_enemies = pygame.sprite.Group() # 所有小敌机都放在small_enemies序列中
    add_small_enemies(small_enemies, enemies, 15) #添加敌机小飞机函数,初始添加15个


    # 生成敌方中飞机
    mid_enemies = pygame.sprite.Group() # 所有中敌机都放在mid_enemies序列中
    add_mid_enemies(mid_enemies, enemies, 5) #添加敌机中飞机函数,初始添加5个

    # 生成敌方大飞机
    big_enemies = pygame.sprite.Group() # 所有大敌机都放在big_enemies序列中
    add_big_enemies(big_enemies, enemies, 2) #添加敌机大飞机函数,初始添加2个

    # 生成普通子弹
    bullet1 = []  # 子弹序列
    bullet1_index = 0 #子弹索引
    BULLET1_NUM = 4 # 12帧的速度, 4个子弹占据整个画面的80%
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop)) # midtop 出现在飞机中央

    # 生成超级子弹
    bullet2 = []  # 子弹序列
    bullet2_index = 0 #子弹索引
    BULLET2_NUM = 8 # 12帧的速度, 8个子弹占据整个画面的80%
    for i in range(BULLET2_NUM):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery))) # 左边子弹
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery))) # 右边子弹

    clock = pygame.time.Clock() #延时变量

    # 中弹图片索引
    e1_destroy_index = 0  # 小型敌机
    e2_destroy_index = 0  # 中型敌机
    e3_destroy_index = 0  # 大型敌机
    me_destroy_index = 0  # 我方敌机

    # 统计得分
    score = 0 # 大型飞机10000分，中型飞机6000分， 小型飞机1000分
    score_font = pygame.font.Font("font/font.ttf",36)  # 加载font.ttf字体, 尺寸为36像素

    # 标志是否暂停游戏
    paused = False
    paused_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha() # 加载鼠标未点击暂停健
    paused_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha() # 加载鼠标点击暂停健
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()# 加载鼠标未点击恢复健
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()# 加载鼠标点击恢复健
    paused_rect = paused_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10 # 初始化显示位置
    paused_image = paused_nor_image #初始化图片，为鼠标未点击暂停健

    # 设置难度级别
    level = 1

    # 全屏炸弹
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha() #建立炸弹图片的对象
    bomb_rect = bomb_image.get_rect() # 得到其宽度
    bomb_font = pygame.font.Font("font/font.ttf", 48) #设置其字体

    # 每30秒发放一个补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT  # 用户自定义事件
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)  # 30 * 1000ms = 30s ，即30s一个补给

    # 超级子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT  + 1 # +1 和 USERVENT 区别开

    # 标志是否使用超级子弹
    is_double_bullet = False

    # 解除我方无敌状态定时器
    INVINCIBLE_TIME = USEREVENT + 2

    # 生命数量
    life_image = pygame.image.load('images/life.png').convert_alpha() # 加载图片
    life_rect = life_image.get_rect() # 获取图片的尺寸
    life_num = 3 # 初始化生命上限

    # 用于阻止重复打开记录文件
    recorded = False

    # 游戏结束画面
    gameover_font = pygame.font.Font("font/font.TTF", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    # 炸弹数量初始为3
    bomb_num = 3

    # 用于切换我方飞机图片，以形成动态效果
    switch_image = True

    # 用于我方飞机切换延时, 使飞机尾气更加流畅
    delay = 100

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN: # 如果检测到鼠标按下
                if event.button == 1 and paused_rect.collidepoint(event.pos): # 检测鼠标是否点击，并且在暂停健内
                    paused = not paused # paused变量改变
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0) # 补给暂停， 0为取消自定义事件
                        pygame.mixer.music.pause() # 背景音乐暂停
                        pygame.mixer.pause() # 音效暂停
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000) # 恢复补给
                        pygame.mixer.music.unpause() # 恢复背景音乐
                        pygame.mixer.unpause()  # 恢复音效

            elif event.type == MOUSEMOTION: # 如果鼠标放在图片上

                if paused_rect.collidepoint(event.pos):
                    if paused:      # 如果是放在图片上，则图片颜色加深
                        paused_image = resume_pressed_image # 如果paused是True，则显示resume图标
                    else:
                        paused_image = paused_pressed_image # 否则显示paused图标
                else:
                    if paused:      # 如果不是放在图片上，则不加深颜色
                        paused_image = resume_nor_image
                    else:
                        paused_image = paused_nor_image
            elif event.type == KEYDOWN: # 如果有按键按下
                if event.key == K_SPACE: # 如果是空格健
                    if bomb_num:
                        bomb_num -= 1    # 炸弹数-1
                        bomb_sound.play()# 播放爆炸声音
                        for each in enemies: # 每一个敌人底部大于0，都摧毁
                            if each.rect.bottom > 0:
                                each.active = False
            elif event.type == SUPPLY_TIME:   # 如果触发了补给发放事件
                supply_sound.play()
                if choice([True, False]): # 二者中随机选择一个
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type == DOUBLE_BULLET_TIME: # 如果触发了超级子弹事件
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0) # 停止超级子弹事件

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0) # 取消计时器

        # 根据用户得分增加难度
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play() # 播放升级难度的音乐
            # 增加3架小型敌机, 2架中型敌机和1架大型敌机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)

            # 提升小型敌机的速度
            inc_speed(target=small_enemies, inc=1)

        elif level == 2 and score > 300000:
            level = 3
            upgrade_sound.play()
            # 增加5架小型敌机, 3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)

            # 提升小型敌机的速度
            inc_speed(target=small_enemies, inc=1)
            inc_speed(target=mid_enemies, inc=1)

        elif level == 3 and score > 600000:
            level = 4
            upgrade_sound.play()
            # 增加5架小型敌机, 3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)

            # 提升小型敌机的速度
            inc_speed(target=small_enemies, inc=1)
            inc_speed(target=mid_enemies, inc=1)

        elif level == 4 and score > 1000000:
            level = 5
            upgrade_sound.play()
            # 增加5架小型敌机, 3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)

            # 提升小型敌机的速度
            inc_speed(target=small_enemies, inc=1)
            inc_speed(target=mid_enemies, inc=1)
            inc_speed(target=big_enemies, inc=1)


        screen.blit(background, (0, 0))

        if life_num and not paused:

            # 检测用户的键盘操作
            key_pressed = pygame.key.get_pressed() # 返回一个所有按键布尔值的序列

            if key_pressed[K_w] or key_pressed[K_UP]: #按下w或方向上
                me.moveUp()

            if key_pressed[K_s] or key_pressed[K_DOWN]: #按下s或方向下
                me.moveDown()

            if key_pressed[K_a] or key_pressed[K_LEFT]: #按下a或方向左
                me.moveLeft()

            if key_pressed[K_d] or key_pressed[K_RIGHT]: #按下d或方向右
                me.moveRight()


            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:     # 如果生成了炸弹补给
                bomb_supply.move()     # 向下移动
                screen.blit(bomb_supply.image, bomb_supply.rect) # 显示炸弹补给
                if pygame.sprite.collide_mask(bomb_supply, me):  # 检测飞机是否碰到炸弹补给
                    get_bomb_sound.play() # 播放获得炸弹补给的音乐
                    if bomb_num < 3: # 如果炸弹补给数量小于3
                        bomb_num += 1# 数量 +1
                    bomb_supply.active = False # 补给消失


            # 绘制超级子弹补给并检测是否获得
            if bullet_supply.active:     # 如果生成了子弹补给
                bullet_supply.move()     # 向下移动
                screen.blit(bullet_supply.image, bullet_supply.rect) # 显示子弹补给
                if pygame.sprite.collide_mask(bullet_supply, me):  # 检测飞机是否碰到子弹补给
                    get_bullet_sound.play() # 播放获得子弹补给的音乐
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,18 * 1000) # 持续时间18s
                    bullet_supply.active = False # 补给消失


            # 发射子弹
            if not(delay % 10):
                bullet_sound.play() # 播放子弹声音
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery)) # 子弹是一对的,所以要+1
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM



            # 检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect) # 绘制子弹
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask) # 检测被击中的敌机
                    if enemy_hit:
                        b.active = False # 子弹失效
                        for e in enemy_hit: # 敌机摧毁
                            if e in mid_enemies or e in big_enemies:  # 如果是中型飞机或者大型飞机
                                e.hit = True
                                e.energy -= 1 # 血量-1
                                if e.energy == 0: # 血量为0
                                    e.active = False # 摧毁
                            else:
                                e.active = False  # 小型飞机直接摧毁


            # 绘制大型敌机
            for each in big_enemies:
                if each.active:  # 如果生存就绘制
                    each.move()  # 大飞机向下移动
                    if each.hit :  #被子弹击中

                        screen.blit(each.image_hit, each.rect)# 绘制被击中的画面
                        each.hit = False  # 击中标志转为False
                    else :
                        if switch_image: # 动态展示大飞机，来回切换
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, # 绘制一个血槽,在敌机上方5个像素的位置,像素为2
                                         (each.rect.left, each.rect.top - 5),
                                         (each.rect.right, each.rect.top - 5),
                                         2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                         (each.rect.left, each.rect.top - 5),
                                         (each.rect.left + each.rect.width * energy_remain, # 长度为血量的比例
                                          each.rect.top - 5),
                                         2)

                    if each.rect.bottom == -50:  # 快进入时播放背景音乐
                        enemy3_fly_sound.play(-1) # 循环播放音效
                else: # 否则毁灭
                    if not (delay % 3): #每隔三帧
                        if e3_destroy_index == 0: # 保证摧毁音乐只播放一次
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6  # 摧毁图片切换到下一张
                        if e3_destroy_index == 0:  # 播放完一套以后,重新创建
                            enemy3_fly_sound.stop()
                            score += 10000
                            each.reset()

            # 绘制中型敌机
            for each in mid_enemies:
                if each.active: # 如果生存就绘制
                    each.move()
                    if each.hit: # 被子弹击中
                        screen.blit(each.image_hit, each.rect)# 绘制被击中的画面
                        each.hit = False  # 击中标志转为False
                    else:
                        screen.blit(each.image, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, # 绘制一个血槽,在敌机上方5个像素的位置,像素为2
                                         (each.rect.left, each.rect.top - 5),
                                         (each.rect.right, each.rect.top - 5),
                                         2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                         (each.rect.left, each.rect.top - 5),
                                         (each.rect.left + each.rect.width * energy_remain, # 长度为血量的比例
                                          each.rect.top - 5),
                                         2)
                else: # 否则毁灭

                    if not (delay % 3): #每隔三帧
                        if e2_destroy_index == 0: # 保证摧毁音乐只播放一次
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4  # 摧毁图片切换到下一张
                        if e2_destroy_index == 0:  # 播放完一套以后,重新创建
                            score += 6000
                            each.reset()


            # 绘制小型敌机
            for each in small_enemies:
                if each.active: # 如果生存就绘制
                    each.move()
                    screen.blit(each.image, each.rect)
                else: # 否则毁灭

                    if not (delay % 3): #每隔三帧
                        if e1_destroy_index == 0: # 保证摧毁音乐只播放一次
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4  # 摧毁图片切换到下一张
                        if e1_destroy_index == 0:  # 播放完一套以后,重新创建
                            score += 1000
                            each.reset()

            # 检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)  # 检测我方飞机是否和敌机发生碰撞,返回碰撞的敌机对象  检测碰撞的方法pygame.sprite.collide_mask(检测非透明)
            if enemies_down and not me.invincible: # 相撞并且我方飞机不是无敌状态
                me.active = False  # 我方飞机摧毁
                for each in enemies_down: # 敌方飞机摧毁
                    each.active = False


            # 绘制我方飞机
            if me.active: # 如果我方飞机生存
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:  # 否则毁灭

                if not (delay % 3): #每隔三帧
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(each.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4  # 摧毁图片切换到下一张
                    if me_destroy_index == 0:  # 播放完一套以后,重新创建
                        life_num -= 1 # 生命数-1
                        me.reset() # 重建我方飞机
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000) # 三秒的无敌时间


            # 绘制全屏炸弹数量
            bomb_text = bomb_font.render("* %d" % bomb_num, True, WHITE) # 将bomb_num渲染成surface对象,True 表示关闭抗锯齿, WHITE表示对象颜色
            text_rect = bomb_text.get_rect()  # 获取对象形状
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height)) # 绘制图片
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height)) # 绘制字体

            # 绘制剩余生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, \
                    (width - 10 - (i + 1) * life_rect.width, \
                    height - 10 - life_rect.height))

            # 绘制得分
            score_text = score_font.render('Score : %d' % score, True, WHITE)
            screen.blit(score_text, (10, 5))
            

        # 绘制游戏结束画面
        elif life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()

            # 停止全部音效
            pygame.mixer.stop()

            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)

            if not recorded:
                recorded =True
                # 读取历史最高分
                with open('record.txt', 'r') as f:
                    record_score = int(f.read())

                # 判断是否高于历史最高分
                if score > record_score:
                    with open('record.txt', 'w') as f:
                        f.write(str(score))


            # 绘制结束界面
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))

            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                                 (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                 (width - gameover_text2_rect.width) // 2, \
                                 gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                             (width - again_rect.width) // 2, \
                             gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                                (width - again_rect.width) // 2, \
                                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                   again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main()
                # 如果用户点击“结束游戏”
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                     gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()


        # 绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        # 切换图片
        if not(delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip() # 更新整个待显示的  Surface 对象到屏幕上

        clock.tick(60)   # 设置延时为60帧

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass   # 如果是正常退出，则不执行
    except:
        traceback.print_exc()
        pygame.quit()
        input() # 否则输出错误，并等待用户输入

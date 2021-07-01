import pygame
from random import * # 创建随机数模块

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):  # 构造函数，传入对象和背景大小
        
        pygame.sprite.Sprite.__init__(self) # 调用父类(Sprite)的构造函数

        self.image = pygame.image.load("images/enemy1.png").convert_alpha() # 创建图像

        # 加载摧毁图片
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("images/enemy1_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy1_down2.png").convert_alpha(), \
            pygame.image.load("images/enemy1_down3.png").convert_alpha(), \
            pygame.image.load("images/enemy1_down4.png").convert_alpha() \
            ])

        self.rect = self.image.get_rect() # 获取具有图像尺寸的矩形对象

        self.width, self.height = bg_size[0], bg_size[1] # 矩形的长和宽赋初值
        
        self.speed = 3 # 敌机的速度

        self.active = True #表示当前飞机存活或摧毁

        self.rect.left, self.rect.top = \
                        randint(0, self.width - self.rect.width), \
                        randint(-5 * self.height, 0) # 随机敌机的位置，高度为负数，一开始未显示成在界面中，但是已经生成

        self.mask = pygame.mask.from_surface(self.image) # 取对象图片中非透明部分
        

    def move(self): # 敌机移动函数
        if self.rect.top < self.height: # 未到底部就一直向下走
            self.rect.top += self.speed
        else :
            self.reset()# 否则出界，重新初始化


    def reset(self): # 敌机重新初始化函数
        self.active = True
        self.rect.left, self.rect.top = \
                        randint(0, self.width - self.rect.width), \
                        randint(-5 * self.height, 0) # 随机敌机的位置，高度为负数，一开始未显示成在界面中，但是已经生成
        

class MidEnemy(pygame.sprite.Sprite):
    energy = 8 # 中型飞机的血量

    
    def __init__(self, bg_size):  # 构造函数，传入对象和背景大小
        
        pygame.sprite.Sprite.__init__(self) # 调用父类(Sprite)的构造函数

        self.image = pygame.image.load("images/enemy2.png").convert_alpha() # 创建图像

        # 加载被击中时的图片
        self.image_hit = pygame.image.load("images/enemy2_hit.png").convert_alpha()
        
        # 加载摧毁图片
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("images/enemy2_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy2_down2.png").convert_alpha(), \
            pygame.image.load("images/enemy2_down3.png").convert_alpha(), \
            pygame.image.load("images/enemy2_down4.png").convert_alpha() \
            ])

        self.rect = self.image.get_rect() # 获取具有图像尺寸的矩形对象

        self.width, self.height = bg_size[0], bg_size[1] # 矩形的长和宽赋初值
        
        self.speed = 2 # 敌机的速度

        self.active = True #表示当前飞机存活或摧毁

        self.rect.left, self.rect.top = \
                        randint(0, self.width - self.rect.width), \
                        randint(-10 * self.height, -self.height) # 随机敌机的位置，高度为负数，不会一开始就出现中型敌机

        self.mask = pygame.mask.from_surface(self.image) # 取对象图片中非透明部分

        self.energy = MidEnemy.energy  # 初始化血量

        self.hit = False #检测是否被击中
        
    def move(self):
        if self.rect.top < self.height: # 未到底部就一直向下走
            self.rect.top += self.speed
        else :
            self.reset()# 否则出界，重新初始化


    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy  # 初始化血量
        self.rect.left, self.rect.top = \
                        randint(0, self.width - self.rect.width), \
                        randint(-10 * self.height, -self.height) # 随机敌机的位置，高度为负数，不会一开始就出现中型敌机
         

class BigEnemy(pygame.sprite.Sprite):

    energy = 20
    
    def __init__(self, bg_size):  # 构造函数，传入对象和背景大小
        
        pygame.sprite.Sprite.__init__(self) # 调用父类(Sprite)的构造函数

        self.image1 = pygame.image.load("images/enemy3_n1.png").convert_alpha() # 创建图像
        self.image2 = pygame.image.load("images/enemy3_n2.png").convert_alpha() # 创建图像

        # 加载被击中时的图片
        self.image_hit = pygame.image.load("images/enemy3_hit.png").convert_alpha()
        
        # 加载摧毁图片
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("images/enemy3_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down2.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down3.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down4.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down5.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down6.png").convert_alpha() \
            ])

        self.rect = self.image1.get_rect() # 获取具有图像尺寸的矩形对象

        self.width, self.height = bg_size[0], bg_size[1] # 矩形的长和宽赋初值
        
        self.speed = 1 # 敌机的速度

        self.active = True #表示当前飞机存活或摧毁

        self.rect.left, self.rect.top = \
                        randint(0, self.width - self.rect.width), \
                        randint(-15 * self.height, -5 * self.height) # 随机敌机的位置，高度为负数，不会一开始就出现中型敌机

        self.mask = pygame.mask.from_surface(self.image1) # 取对象图片中非透明部分

        self.energy = BigEnemy.energy # 初始化血量

        self.hit = False #检测是否被击中
        
    def move(self):
        if self.rect.top < self.height: # 未到底部就一直向下走
            self.rect.top += self.speed
        else :
            self.reset()# 否则出界，重新初始化


    def reset(self):
        self.active = True
        self.energy = BigEnemy.energy # 初始化血量
        self.rect.left, self.rect.top = \
                        randint(0, self.width - self.rect.width), \
                        randint(-15 * self.height, -5 * self.height) # 随机敌机的位置，高度为负数，不会一开始就出现中型敌机

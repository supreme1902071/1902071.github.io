import pygame

class MyPlane(pygame.sprite.Sprite): # 继承 pygame.sprite.Sprite 类
    def __init__(self, bg_size):  # 构造函数，传入对象和背景大小

        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("images/me1.png").convert_alpha() # 创建图像1
        self.image2 = pygame.image.load("images/me2.png").convert_alpha() # 创建图像2
        # convert方法的作用是使用更改的像素格式创建Surface的新副本
        # 使用所需的像素格式创建曲面的新副本。 新表面将采用适合于以每像素alpha快速blitting到给定格式的格式

        # 加载摧毁图片
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("images/me_destroy_1.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_2.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_3.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_4.png").convert_alpha() \
            ])

        self.rect = self.image1.get_rect() # 获取具有图像尺寸的矩形对象

        self.width, self.height = bg_size[0], bg_size[1] # 矩形的长和宽赋初值


        # 飞机位置初始化 最底行，中心列
        self.rect.left, self.rect.top = \
                        (self.width - self.rect.width) // 2, \
                        self.height - self.rect.height - 60 # 60 用于最下方的武器

        self.speed = 10 # 飞机速度初始化为10

        self.active = True #表示当前飞机存活或摧毁

        self.invincible = False # 表示飞机是否无敌

        self.mask = pygame.mask.from_surface(self.image1) # 取对象图片中非透明部分

    def moveUp(self): #向上走
        if self.rect.top > 0: # 飞机顶部没过背景顶部
            self.rect.top -= self.speed # 飞机高度 - speed
        else:
            self.rect.top = 0 # 否则出界，在最顶上


    def moveDown(self): #向下走
        if self.rect.bottom < self.height - 60: # 飞机底部没过背景底部
            self.rect.top += self.speed # 飞机宽度 + speed
        else:
            self.rect.bottom = self.height - 60 # 否则出界，在最底部

    def moveLeft(self): #向左走
        if self.rect.left > 0: # 飞机左部没过背景左部
            self.rect.left -= self.speed # 飞机高度 - speed
        else:
            self.rect.left = 0 # 否则出界，在最左边

    def moveRight(self): #向右走
        if self.rect.right < self.width: # 飞机右部没过背景右部
            self.rect.left += self.speed # 飞机宽度 + speed
        else:
            self.rect.right = self.width # 否则出界，在最右边
    def reset(self):
        # 飞机位置初始化 最底行，中心列
        self.rect.left, self.rect.top = \
                        (self.width - self.rect.width) // 2, \
                        self.height - self.rect.height - 60 # 60 用于最下方的武器
        self.active = True
        self.invincible = True # 重生以后，飞机有三秒的无敌时间

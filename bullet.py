import pygame

class Bullet1(pygame.sprite.Sprite): # 继承 pygame.sprite.Sprite 类
    def __init__(self, position):  # 构造函数，传入对象和背景大小
        
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/bullet1.png").convert_alpha() # 创建图像
        self.rect = self.image.get_rect() # 获取具有图像尺寸的矩形对象
        self.rect.left, self.rect.top = position # 子弹位置
        self.speed = 12  # 子弹速度
        self.active = True # 子弹存活
        self.mask = pygame.mask.from_surface(self.image) # 取对象图片中非透明部分
        
    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.active = False

    
    def reset(self, position):
        self.rect.left, self.rect.top = position # 子弹位置
        self.active = True   # 子弹存活

class Bullet2(pygame.sprite.Sprite): # 继承 pygame.sprite.Sprite 类
    def __init__(self, position):  # 构造函数，传入对象和背景大小
        
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/bullet2.png").convert_alpha() # 创建图像
        self.rect = self.image.get_rect() # 获取具有图像尺寸的矩形对象
        self.rect.left, self.rect.top = position # 子弹位置
        self.speed = 12  # 子弹速度
        self.active = True # 子弹存活
        self.mask = pygame.mask.from_surface(self.image) # 取对象图片中非透明部分
        
    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.active = False

    
    def reset(self, position):
        self.rect.left, self.rect.top = position # 子弹位置
        self.active = True   # 子弹存活

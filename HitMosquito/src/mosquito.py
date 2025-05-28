import pygame
import random
import time

class Mosquito:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.speed = 1
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.alive = True
        
        # 动画相关属性
        self.is_open = True  # 翅膀状态
        self.animation_timer = time.time()  # 动画计时器
        self.animation_interval = 0.2  # 动画间隔（秒）
        
    def update(self, screen_width, screen_height):
        """更新蚊子位置和动画状态"""
        if not self.alive:
            return
            
        # 更新位置
        self.x += self.speed * self.direction_x
        self.y += self.speed * self.direction_y
        
        # 边界检查
        if self.x <= 0 or self.x >= screen_width - self.width:
            self.direction_x *= -1
        if self.y <= 0 or self.y >= screen_height - self.height:
            self.direction_y *= -1
            
        # 更新动画状态
        current_time = time.time()
        if current_time - self.animation_timer >= self.animation_interval:
            self.is_open = not self.is_open  # 切换翅膀状态
            self.animation_timer = current_time
            
    def draw(self, screen):
        """绘制蚊子"""
        if not self.alive:
            return
            
        # 临时使用矩形代替蚊子图片
        pygame.draw.rect(screen, (0, 0, 0), 
                        (self.x, self.y, self.width, self.height))
                        
    def check_hit(self, pos):
        """检查是否被击中"""
        if not self.alive:
            return False
            
        mouse_x, mouse_y = pos
        # 增加碰撞检测范围，使击中更容易
        hit_margin = 10
        return (self.x - hit_margin <= mouse_x <= self.x + self.width + hit_margin and 
                self.y - hit_margin <= mouse_y <= self.y + self.height + hit_margin) 
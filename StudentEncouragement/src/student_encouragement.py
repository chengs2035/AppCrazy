import pygame
import random
import os
import sys
from collections import deque
import time

class PopupWindow:
    def __init__(self, text, x, y, bg_color, text_color, font, is_vertical=False):
        self.text = text
        self.x = x
        self.y = y
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = font
        self.alpha = 100
        self.fade_speed = 5 # 设置为每秒5帧
        self.life_time = 0
        self.max_life_time = 200  # 显示时间（帧数）
        self.is_vertical = is_vertical
        
        # 计算窗口大小
        if self.is_vertical:
            # 竖向文字，每个字符单独渲染
            char_height = self.font.get_height()
            self.width = char_height + 40
            self.height = len(text) * char_height + 40
        else:
            # 横向文字
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.width = text_surface.get_width() + 40
            self.height = text_surface.get_height() + 40
        
        # 创建窗口表面
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
    def update(self):
        if self.life_time < self.max_life_time:
            if self.alpha < 255:
                self.alpha += self.fade_speed
            self.life_time += 1
        else:
            if self.alpha > 0:
                self.alpha -= self.fade_speed
            else:
                return False
        return True

    def draw(self, screen):
        # 清空表面
        self.surface.fill((0, 0, 0, 0))
        
        # 绘制阴影
        shadow_surface = pygame.Surface((self.width + 4, self.height + 4), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 100), (0, 0, self.width + 4, self.height + 4), border_radius=10)
        screen.blit(shadow_surface, (self.x - 2, self.y - 2))
        
        # 绘制窗口背景
        pygame.draw.rect(self.surface, (*self.bg_color, self.alpha), (0, 0, self.width, self.height), border_radius=10)
        pygame.draw.rect(self.surface, (*self.text_color, self.alpha), (0, 0, self.width, self.height), 2, border_radius=10)
        
        if self.is_vertical:
            # 竖向渲染文字
            char_height = self.font.get_height()
            for i, char in enumerate(self.text):
                char_surface = self.font.render(char, True, self.text_color)
                char_surface.set_alpha(self.alpha)
                char_rect = char_surface.get_rect(center=(self.width // 2, 20 + i * char_height))
                self.surface.blit(char_surface, char_rect)
        else:
            # 横向渲染文字
            text_surface = self.font.render(self.text, True, self.text_color)
            text_surface.set_alpha(self.alpha)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
            self.surface.blit(text_surface, text_rect)
        
        # 将窗口绘制到屏幕上
        screen.blit(self.surface, (self.x, self.y))

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class StudentEncouragementApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("妈祖保佑加油站V1.0")
        
        # 获取屏幕信息
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h
        
        # 设置全屏窗口
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        
        # 加载资源
        self.load_resources()
        
        # 初始化变量
        self.clock = pygame.time.Clock()
        self.running = True
        self.popup_windows = []
        self.is_running = False
        self.progress = 0
        self.total_windows = 2000
        self.current_window = 0
        
        # 创建按钮
        button_font = pygame.font.Font("simhei.ttf", 24)
        self.button = Button(
            self.screen_width // 2 - 150,  # 调整按钮位置
            self.screen_height // 2,
            300, 50,
            "立刻马上让妈祖给你加油！",
            button_font,
            (255, 0, 0),
            (200, 0, 0)
        )
        
        # 创建标题字体
        self.title_font = pygame.font.Font("simhei.ttf", 36)
        
        # 创建副标题字体（更大的字体）
        self.subtitle_font = pygame.font.Font("simhei.ttf", 48)
        
        # 创建弹出框字体
        self.popup_font = pygame.font.Font("simhei.ttf", 20)
        
        # 背景颜色组合
        self.bg_colors = [
            (230, 243, 255),  # 浅蓝色
            (240, 248, 255),  # 爱丽丝蓝
            (245, 245, 245),  # 白色
            (255, 240, 245),  # 淡粉色
            (240, 255, 240),  # 蜜瓜绿
            (255, 250, 205),  # 柠檬黄
            (245, 245, 220),  # 米色
            (224, 255, 255),  # 淡青色
            (255, 228, 225),  # 淡红色
        ]
        
        # 文字颜色组合
        self.text_colors = [
            (139, 0, 0),    # 深红色
            (0, 100, 0),    # 深绿色
            (75, 0, 130),   # 靛蓝色
            (139, 69, 19),  # 棕色
            (128, 0, 128),  # 紫色
            (0, 0, 128),    # 深蓝色
            (139, 0, 139),  # 深紫色
        ]

    def load_resources(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            resources_dir = os.path.join(os.path.dirname(current_dir), 'resources')
            
            # 加载妈祖图片
            image_path = os.path.join(resources_dir, 'safer.png')
            self.mazu_image = pygame.image.load(image_path)
            self.mazu_image = pygame.transform.scale(self.mazu_image, (128, 395))
            
            # 加载鼓励语
            encouragements_file = os.path.join(resources_dir, 'encouragements.txt')
            with open(encouragements_file, 'r', encoding='utf-8') as f:
                self.encouragements = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"加载资源失败: {e}")
            self.encouragements = [
                "加油！你是最棒的！",
                "相信自己，你一定能行！",
                "你的努力一定会得到回报！",
            ]

    def start_encouragement(self):
        if not self.is_running:
            self.is_running = True
            self.current_window = 0
            self.popup_windows.clear()

    def update(self):
        if self.is_running and self.current_window < self.total_windows:
            # 创建新的弹出窗口
            text = f"{random.choice(self.encouragements)}"
            x = random.randint(0, self.screen_width - 200)
            y = random.randint(0, self.screen_height - 100)
            bg_color = random.choice(self.bg_colors)
            text_color = random.choice(self.text_colors)
            
            # 随机选择文字方向
            is_vertical = random.choice([True, False])
            
            self.popup_windows.append(
                PopupWindow(text, x, y, bg_color, text_color, self.popup_font, is_vertical)
            )
            
            self.current_window += 1
            self.progress = (self.current_window / self.total_windows) * 100
            
            if self.current_window >= self.total_windows:
                self.is_running = False

        # 更新所有弹出窗口
        self.popup_windows = [window for window in self.popup_windows if window.update()]

    def draw(self):
        # 绘制背景
        self.screen.fill((135, 206, 235))  # 浅蓝色背景
        
        # 绘制标题
        title_surface = self.title_font.render("妈祖保佑，高考加油", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_surface, title_rect)
        
        # 绘制妈祖图片
        if hasattr(self, 'mazu_image'):
            self.screen.blit(self.mazu_image, (self.screen_width // 3 - 150, self.screen_height // 3 - 50))
        
        # 绘制按钮
        self.button.draw(self.screen)
        
        # 绘制副标题（在按钮下方）
        subtitle_text = "一起为高考生加油吧！"
        # 创建文字阴影
        shadow_surface = self.subtitle_font.render(subtitle_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.screen_width // 2 + 2, self.screen_height // 2 + 80))
        self.screen.blit(shadow_surface, shadow_rect)
        
        # 绘制主文字
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, (255, 215, 0))  # 金色
        subtitle_rect = subtitle_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 78))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # 绘制进度条
        if self.is_running:
            progress_width = int(self.screen_width * 0.8)
            progress_x = (self.screen_width - progress_width) // 2
            pygame.draw.rect(self.screen, (200, 200, 200), (progress_x, self.screen_height - 50, progress_width, 20))
            current_progress = int(progress_width * (self.progress / 100))
            pygame.draw.rect(self.screen, (0, 255, 0), (progress_x, self.screen_height - 50, current_progress, 20))
            
            # 绘制进度文本
            progress_text = f"已加油: {self.current_window}/{self.total_windows}"
            progress_surface = self.popup_font.render(progress_text, True, (0, 0, 0))
            progress_rect = progress_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 80))
            self.screen.blit(progress_surface, progress_rect)
        
        # 绘制所有弹出窗口
        for window in self.popup_windows:
            window.draw(self.screen)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # 按ESC退出
                        self.running = False
                elif self.button.handle_event(event):
                    self.start_encouragement()
            
            self.update()
            self.draw()
            self.clock.tick(60) # 设置为每秒60帧
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = StudentEncouragementApp()
    app.run() 
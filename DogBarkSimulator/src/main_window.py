import pygame
import tkinter as tk
from tkinter import filedialog
import os
import random
import time
import hashlib

class MainWindow:
    def __init__(self):
        # 初始化Pygame
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        pygame.mixer.init()
        
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("狗叫模拟器")
        
        # 初始化颜色
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.LIGHT_BLUE = (173, 216, 230)
        self.DARK_BLUE = (0, 0, 139)
        self.LIGHT_GREEN = (144, 238, 144)
        self.DARK_GREEN = (34, 139, 34)
        self.LIGHT_PINK = (255, 182, 193)
        self.DARK_PINK = (219, 112, 147)
        
        # 加载背景图片
        try:
            background_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                         'assets', 'images', 'background.png')
            self.background = pygame.image.load(background_path)
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except Exception as e:
            print(f"加载背景图片时出错：{str(e)}")
            self.background = None
        
        # 初始化字体
        try:
            font_names = [
                "Microsoft YaHei",
                "SimHei",
                "SimSun",
                "NSimSun",
                "FangSong",
                "KaiTi",
                "WenQuanYi Micro Hei",
                "WenQuanYi Zen Hei",
                "Noto Sans CJK SC",
                "PingFang SC",
                "STHeiti",
                "Hiragino Sans GB"
            ]
            
            self.font = None
            for font_name in font_names:
                try:
                    self.font = pygame.font.SysFont(font_name, 36)
                    test_text = self.font.render("测试", True, self.BLACK)
                    if test_text.get_width() > 0:
                        break
                except:
                    continue
            
            if self.font is None:
                self.font = pygame.font.Font(None, 36)
                print("警告：未找到支持中文的字体，将使用默认字体")
        except Exception as e:
            print(f"初始化字体时出错：{str(e)}")
            self.font = pygame.font.Font(None, 36)
        
        # 用户输入
        self.name = ""
        self.selected_image = None
        self.image_path = None
        
        # 创建输入框
        self.input_rect = pygame.Rect(300, 400, 200, 40)
        self.input_active = False
        
        # 创建按钮
        self.select_image_button = pygame.Rect(300, 300, 200, 50)
        self.start_button = pygame.Rect(300, 500, 200, 50)
        
        # 加载默认狗图片
        self.dog_image = None
        self.dog_rect = None
        
        # 动画相关
        self.animation_time = 0
        self.button_hover = None
        
        # 狗叫相关
        self.is_barking = False
        self.last_bark_time = 0
        self.bark_interval = 2  # 叫叫间隔（秒）
        self.bark_sounds = []
        self.load_bark_sounds()
    
    def get_md5(self, text):
        """计算文本的MD5值"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def get_sound_index(self, md5_value):
        """根据MD5值选择音效索引"""
        if not self.bark_sounds:
            return 0
        # 将MD5值转换为整数
        md5_int = int(md5_value, 16)
        # 使用取模运算确保索引在有效范围内
        return md5_int % len(self.bark_sounds)
    
    def load_bark_sounds(self):
        try:
            sound_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'sounds')
            self.bark_sounds = []
            for file in os.listdir(sound_dir):
                if file.endswith('.mp3'):
                    sound_path = os.path.join(sound_dir, file)
                    self.bark_sounds.append(sound_path)
        except Exception as e:
            print(f"加载音效时出错：{str(e)}")
    
    def play_bark_sound(self):
        if self.bark_sounds and self.name:
            try:
                # 计算输入内容的MD5值
                md5_value = self.get_md5(self.name)
                # 根据MD5值选择音效
                sound_index = self.get_sound_index(md5_value)
                sound_path = self.bark_sounds[sound_index]
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"播放音效时出错：{str(e)}")
    
    def draw_background(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            # 如果背景图片加载失败，使用渐变背景作为后备方案
            for y in range(self.height):
                ratio = y / self.height
                color = (
                    int(self.LIGHT_BLUE[0] * (1 - ratio) + self.DARK_BLUE[0] * ratio),
                    int(self.LIGHT_BLUE[1] * (1 - ratio) + self.DARK_BLUE[1] * ratio),
                    int(self.LIGHT_BLUE[2] * (1 - ratio) + self.DARK_BLUE[2] * ratio)
                )
                pygame.draw.line(self.screen, color, (0, y), (self.width, y))
    
    def draw_button(self, rect, text, hover=False):
        # 绘制按钮阴影
        shadow_rect = rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (100, 100, 100), shadow_rect, border_radius=10)
        
        # 绘制按钮主体
        if hover:
            color = self.LIGHT_GREEN
        else:
            color = self.LIGHT_PINK
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        
        # 绘制按钮边框
        pygame.draw.rect(self.screen, self.DARK_PINK, rect, 2, border_radius=10)
        
        # 绘制按钮文字
        text_surface = self.font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.input_active = True
                else:
                    self.input_active = False
                
                if self.select_image_button.collidepoint(event.pos):
                    self.select_image()
                
                if self.start_button.collidepoint(event.pos):
                    if self.name or self.image_path:
                        self.is_barking = not self.is_barking
                        if not self.is_barking:
                            self.last_bark_time = 0
                            pygame.mixer.music.stop()
            
            if event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        self.name += event.unicode
        
        # 更新按钮悬停状态
        mouse_pos = pygame.mouse.get_pos()
        self.button_hover = None
        if self.select_image_button.collidepoint(mouse_pos):
            self.button_hover = "select"
        elif self.start_button.collidepoint(mouse_pos):
            self.button_hover = "start"
        
        # 处理狗叫
        if self.is_barking:
            current_time = time.time()
            if current_time - self.last_bark_time >= self.bark_interval:
                self.play_bark_sound()
                self.last_bark_time = current_time
        
        return True
    
    def select_image(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            self.selected_image = pygame.image.load(file_path)
            self.selected_image = pygame.transform.scale(self.selected_image, (200, 200))
    
    def draw(self):
        # 绘制背景
        self.draw_background()
        
        # 绘制标题
        title = self.font.render("狗叫模拟器", True, self.WHITE)
        title_rect = title.get_rect(center=(self.width // 2, 50))
        self.screen.blit(title, title_rect)
        
        # 绘制输入框
        pygame.draw.rect(self.screen, self.WHITE, self.input_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.DARK_BLUE if self.input_active else self.GRAY, 
                        self.input_rect, 2, border_radius=5)
        text_surface = self.font.render(self.name, True, self.BLACK)
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        
        # 绘制按钮
        self.draw_button(self.select_image_button, "选择图片", 
                        self.button_hover == "select")
        self.draw_button(self.start_button, "停止叫" if self.is_barking else "开始叫", 
                        self.button_hover == "start")
        
        # 绘制选中的图片
        if self.selected_image:
            # 添加图片阴影
            shadow_rect = self.selected_image.get_rect(center=(self.width // 2, 200))
            shadow_rect.x += 3
            shadow_rect.y += 3
            shadow_surface = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 128))
            self.screen.blit(shadow_surface, shadow_rect)
            
            # 绘制图片
            image_rect = self.selected_image.get_rect(center=(self.width // 2, 200))
            self.screen.blit(self.selected_image, image_rect)
            
            # 如果正在叫，显示"汪汪！"
            if self.is_barking:
                bark_text = self.font.render("汪汪！", True, self.BLACK)
                bark_rect = bark_text.get_rect(center=(self.width // 2, 250))
                self.screen.blit(bark_text, bark_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            running = self.handle_events()
            self.draw()
            clock.tick(30)  # 限制帧率为30FPS
        
        pygame.quit() 
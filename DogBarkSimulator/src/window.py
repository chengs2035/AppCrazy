import os
import pygame
import tkinter as tk
from tkinter import filedialog
from constants import *
from utils import init_font, load_sounds, get_md5, get_sound_index, get_asset_path

class MainWindow:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        
        # 初始化字体
        self.font = init_font()
        
        # 初始化背景
        self.background = None
        try:
            background_path = get_asset_path('images', 'background.png')
            if os.path.exists(background_path):
                self.background = pygame.image.load(background_path)
                self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            print(f"加载背景图片时出错：{str(e)}")
        
        # 初始化输入框
        self.input_text = ""
        self.input_active = False
        self.input_rect = pygame.Rect(INPUT_X, INPUT_Y, INPUT_WIDTH, INPUT_HEIGHT)
        
        # 初始化按钮
        self.select_button = pygame.Rect(SELECT_BUTTON_X, SELECT_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.bark_button = pygame.Rect(BARK_BUTTON_X, BARK_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        # 初始化图片
        self.dog_image = None
        self.image_rect = pygame.Rect(IMAGE_X, IMAGE_Y, IMAGE_SIZE, IMAGE_SIZE)
        
        # 初始化音效
        self.bark_sounds = load_sounds(get_asset_path('sounds', ''))
        
        # 初始化叫状态
        self.is_barking = False
        self.bark_timer = 0
        self.bark_interval = BARK_INTERVAL
        
        # 初始化输入法
        self.ime_window = None
        self.init_ime()
    
    def init_ime(self):
        """初始化输入法窗口"""
        try:
            self.ime_window = tk.Tk()
            self.ime_window.withdraw()
        except Exception as e:
            print(f"初始化输入法时出错：{str(e)}")
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 处理输入框点击
                if self.input_rect.collidepoint(event.pos):
                    self.input_active = True
                    if self.ime_window:
                        self.ime_window.deiconify()
                else:
                    self.input_active = False
                    if self.ime_window:
                        self.ime_window.withdraw()
                
                # 处理选择图片按钮点击
                if self.select_button.collidepoint(event.pos):
                    self.select_image()
                
                # 处理叫按钮点击
                if self.bark_button.collidepoint(event.pos):
                    self.is_barking = not self.is_barking
                    if not self.is_barking:
                        pygame.mixer.music.stop()
            
            if event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == pygame.K_RETURN:
                        self.input_active = False
                        if self.ime_window:
                            self.ime_window.withdraw()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode
        
        # 更新叫状态
        if self.is_barking:
            current_time = pygame.time.get_ticks()
            if current_time - self.bark_timer > self.bark_interval:
                self.play_bark_sound()
                self.bark_timer = current_time
        
        return True
    
    def select_image(self):
        """选择图片"""
        try:
            file_path = filedialog.askopenfilename(
                title="选择图片",
                filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif")]
            )
            if file_path:
                self.dog_image = pygame.image.load(file_path)
                self.dog_image = pygame.transform.scale(self.dog_image, (IMAGE_SIZE, IMAGE_SIZE))
        except Exception as e:
            print(f"加载图片时出错：{str(e)}")
    
    def play_bark_sound(self):
        """播放叫声音效"""
        if not self.bark_sounds:
            return
        
        try:
            # 根据输入文本的MD5值选择音效
            md5_value = get_md5(self.input_text)
            sound_index = get_sound_index(md5_value, len(self.bark_sounds))
            sound_path = self.bark_sounds[sound_index]
            
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"播放音效时出错：{str(e)}")
    
    def draw(self):
        """绘制界面"""
        # 绘制背景
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(WHITE)
        
        # 绘制标题
        title = self.font.render("狗狗叫模拟器", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        # 绘制输入框
        pygame.draw.rect(self.screen, GRAY if self.input_active else WHITE, self.input_rect)
        pygame.draw.rect(self.screen, BLACK, self.input_rect, 2)
        text_surface = self.font.render(self.input_text, True, BLACK)
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        
        # 绘制按钮
        self.draw_button(self.select_button, "选择图片")
        self.draw_button(self.bark_button, "停止叫" if self.is_barking else "开始叫")
        
        # 绘制图片
        if self.dog_image:
            self.screen.blit(self.dog_image, self.image_rect)
        else:
            pygame.draw.rect(self.screen, GRAY, self.image_rect)
            text = self.font.render("请选择图片", True, BLACK)
            text_rect = text.get_rect(center=self.image_rect.center)
            self.screen.blit(text, text_rect)
        
        # 绘制叫状态
        if self.is_barking:
            bark_text = self.font.render("汪汪！", True, BLACK)
            bark_rect = bark_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
            self.screen.blit(bark_text, bark_rect)
        
        pygame.display.flip()
    
    def draw_button(self, rect, text):
        """绘制按钮"""
        # 绘制阴影
        shadow_rect = rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(self.screen, SHADOW_COLOR, shadow_rect)
        
        # 绘制按钮
        pygame.draw.rect(self.screen, BUTTON_COLOR, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 2)
        
        # 绘制文字
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def run(self):
        """运行主循环"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            self.draw()
            clock.tick(FPS)
        
        pygame.quit()
        if self.ime_window:
            self.ime_window.destroy() 
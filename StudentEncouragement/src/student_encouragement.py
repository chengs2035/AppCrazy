import pygame
import random
import os
import sys
from collections import deque
import time

class PopupWindow:
    def __init__(self, text, x, y, bg_color, text_color, font, display_mode=0, move_speed=0):
        self.text = text
        self.x = x
        self.y = y
        self.bg_color = bg_color
        self.text_color = text_color
        self.display_mode = display_mode  # 0: 横向, 1: 竖向, 2: 45度角
        self.move_speed = move_speed  # 移动速度，0表示不移动
        
        # 随机字体大小（基础大小52px ± 10px）
        self.font_size = random.randint(42, 62)
        self.font = pygame.font.Font("simhei.ttf", self.font_size)
        
        self.alpha = 150  # 提高初始透明度
        self.fade_speed = 15  # 加快淡入淡出速度
        self.life_time = 0
        self.max_life_time = 50  # 减少显示时间
        self.is_moving = move_speed > 0  # 标记是否为移动弹窗
        
        # 预渲染文字表面
        self.text_surface = self.font.render(text, True, (0, 0, 0))
        
        # 计算窗口大小
        if self.display_mode == 1:  # 竖向
            # 竖向文字，每个字符单独渲染
            char_height = self.font.get_height()
            base_width = char_height + 40
            base_height = len(text) * char_height + 40
            # 随机调整窗口大小（±10px）
            self.width = base_width + random.randint(-10, 10)
            self.height = base_height + random.randint(-10, 10)
        elif self.display_mode == 2:  # 45度角
            # 使用预渲染的文字表面
            text_width = self.text_surface.get_width()
            text_height = self.text_surface.get_height()
            # 计算旋转后的实际占用空间
            rotated_width = int((text_width + text_height) * 0.707)  # cos(45°) ≈ 0.707
            rotated_height = int((text_width + text_height) * 0.707)
            base_width = rotated_width + 40
            base_height = rotated_height + 40
            # 随机调整窗口大小（±10px）
            self.width = base_width + random.randint(-10, 10)
            self.height = base_height + random.randint(-10, 10)
        else:  # 横向
            # 使用预渲染的文字表面
            base_width = self.text_surface.get_width() + 40
            base_height = self.text_surface.get_height() + 40
            # 随机调整窗口大小（±10px）
            self.width = base_width + random.randint(-10, 10)
            self.height = base_height + random.randint(-10, 10)
        
        # 创建窗口表面
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # 预渲染窗口背景
        self.bg_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.bg_surface, (*self.bg_color, 255), (0, 0, self.width, self.height), border_radius=10)
        pygame.draw.rect(self.bg_surface, (*self.text_color, 255), (0, 0, self.width, self.height), 2, border_radius=10)
        
    def update(self):
        if self.is_moving:
            # 移动弹窗：只检查是否移出屏幕
            self.x += 50
            # 如果窗口完全移出屏幕右侧，则结束生命周期
            if self.x > pygame.display.get_surface().get_width():
                return False
            # 确保透明度为最大
            if self.alpha < 255:
                self.alpha = 255
        else:
            # 非移动弹窗：使用原有的生命周期管理
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
        
        # 绘制预渲染的背景
        self.surface.blit(self.bg_surface, (0, 0))
        
        if self.display_mode == 1:  # 竖向
            # 竖向渲染文字
            char_height = self.font.get_height()
            for i, char in enumerate(self.text):
                char_surface = self.font.render(char, True, self.text_color)
                char_surface.set_alpha(self.alpha)
                char_rect = char_surface.get_rect(center=(self.width // 2, 20 + i * char_height))
                self.surface.blit(char_surface, char_rect)
        elif self.display_mode == 2:  # 45度角
            # 使用预渲染的文字表面
            text_surface = self.text_surface.copy()
            text_surface.set_alpha(self.alpha)
            # 旋转文字
            rotated_text = pygame.transform.rotate(text_surface, 45)
            # 计算居中位置，考虑旋转后的偏移
            text_rect = rotated_text.get_rect(center=(self.width // 2, self.height // 2))
            # 微调位置以确保文字完全居中
            text_rect.x += (self.width - rotated_text.get_width()) // 2
            text_rect.y += (self.height - rotated_text.get_height()) // 2
            self.surface.blit(rotated_text, text_rect)
        else:  # 横向
            # 使用预渲染的文字表面
            text_surface = self.text_surface.copy()
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
        pygame.display.set_caption("妈祖保佑，高考加油")
        
        # 获取屏幕信息
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h
        
        # 设置全屏窗口
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        
        # 加载字体
        self.font = pygame.font.Font(None, 68)  # 增大字体
        self.popup_font = pygame.font.Font(None, 52)  # 增大弹出窗口字体
        
        # 设置颜色
        self.bg_color = (240, 248, 255)  # 淡蓝色背景
        self.button_color = (100, 149, 237)  # 淡蓝色按钮
        self.button_hover_color = (65, 105, 225)  # 深蓝色悬停
        self.text_color = (25, 25, 112)  # 深蓝色文字
        
        # 设置按钮
        button_width = 400  # 增大按钮宽度
        button_height = 100  # 增大按钮高度
        self.start_button = pygame.Rect(
            (self.screen_width - button_width) // 2,
            self.screen_height // 2,
            button_width,
            button_height
        )
        
        # 设置进度条
        self.progress = 0
        progress_width = int(self.screen_width * 0.8)
        progress_x = (self.screen_width - progress_width) // 2
        self.progress_bar = pygame.Rect(progress_x, self.screen_height - 100, progress_width, 40)  # 增大进度条尺寸
        
        # 设置弹出窗口
        self.popup_windows = []
        self.current_window = 0
        self.total_windows = 1000
        self.windows_per_frame = 2  # 减少每帧生成的弹窗数量
        self.max_windows = 200  # 限制最大同时存在的弹窗数量
        self.is_running = False
        self.move_speed = 5  # 设置移动速度
        self.cleared_at_5_percent = False  # 标记是否已经清除过弹窗
        
        # 设置鼓励语
        self.encouragements = [
            "加油！", "你是最棒的！", "继续努力！", "相信自己！",
            "坚持就是胜利！", "不要放弃！", "你一定能行！", "保持专注！",
            "向前冲！", "永不放弃！", "追求卓越！", "超越自我！",
            "勇往直前！", "创造奇迹！", "突破极限！", "追求梦想！"
        ]
        
        # 设置颜色
        self.bg_colors = [
            (255, 182, 193),  # 浅粉色
            (173, 216, 230),  # 浅蓝色
            (144, 238, 144),  # 浅绿色
            (255, 218, 185),  # 浅橙色
            (221, 160, 221),  # 浅紫色
            (255, 228, 196),  # 浅黄色
            (176, 224, 230),  # 浅青色
            (255, 192, 203)   # 浅红色
        ]
        
        self.text_colors = [
            (25, 25, 112),    # 深蓝色
            (85, 107, 47),    # 深绿色
            (139, 69, 19),    # 深棕色
            (72, 61, 139),    # 深紫色
            (128, 0, 0),      # 深红色
            (0, 100, 0),      # 深绿色
            (47, 79, 79),     # 深青色
            (85, 26, 139)     # 深紫色
        ]
        
        # 加载资源
        self.load_resources()
        
        # 初始化变量
        self.clock = pygame.time.Clock()
        self.running = True
        self.popup_windows = []
        self.is_running = False
        self.progress = 0
        self.total_windows = 5000  # 增加总窗口数量
        self.current_window = 0
        self.windows_per_frame = 2  # 每帧生成的窗口数量
        
        # 创建按钮
        button_font = pygame.font.Font("simhei.ttf", 24)
        self.button = Button(
            self.screen.get_width() // 2 - 150,
            self.screen.get_height() // 2,
            300, 50,
            "立刻马上让妈祖给你加油！",
            button_font,
            (255, 0, 0),
            (200, 0, 0)
        )
        
        # 创建标题字体
        self.title_font = pygame.font.Font("simhei.ttf", 80)
        
        # 创建副标题字体（更大的字体）
        self.subtitle_font = pygame.font.Font("simhei.ttf", 80)
        
        # 创建弹出框字体
        self.popup_font = pygame.font.Font("simhei.ttf", 16)  # 减小字体大小
        
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

    def get_random_position(self):
        # 如果进度超过5%，则从左侧生成
        if self.progress >= 5:
            # 随机选择左侧的y坐标
            y = random.randint(50, self.screen_height - 50)
            # 从屏幕左侧开始
            x = -100  # 从屏幕外开始
            return x, y
        
        # 否则使用原来的随机位置生成
        grid_size = 150  # 增大网格大小以适应全屏
        # 计算可用的网格数量
        cols = (self.screen_width - 1) // grid_size
        rows = (self.screen_height - 2) // grid_size
        
        # 随机选择一个网格
        col = random.randint(0, cols - 1)
        row = random.randint(0, rows - 1)
        
        # 在网格内随机位置
        x = col * grid_size + random.randint(10, grid_size - 10)
        y = row * grid_size + random.randint(10, grid_size - 10)
        
        return x, y

    def clear_all_windows(self):
        """清除所有现有的弹窗"""
        self.popup_windows.clear()
        self.cleared_at_5_percent = True

    def update(self):
        if self.is_running and self.current_window < self.total_windows:
            # 检查是否达到5%进度且未清除过弹窗
            if self.progress >= 5 and not self.cleared_at_5_percent:
                self.clear_all_windows()
            
            # 每帧创建多个窗口，但不超过最大限制
            for _ in range(self.windows_per_frame):
                if self.current_window >= self.total_windows:
                    break
                    
                # 如果当前弹窗数量达到上限，停止生成新的
                if len(self.popup_windows) >= self.max_windows:
                    break
                    
                # 创建新的弹出窗口
                text = f"{random.choice(self.encouragements)}"
                x, y = self.get_random_position()
                bg_color = random.choice(self.bg_colors)
                text_color = random.choice(self.text_colors)
                
                # 随机选择显示模式 (0: 横向, 1: 竖向, 2: 45度角)
                display_mode = random.randint(0, 1)
                
                # 根据进度决定是否添加移动速度
                move_speed = self.move_speed if self.progress >= 5 else 0
                
                self.popup_windows.append(
                    PopupWindow(text, x, y, bg_color, text_color, self.popup_font, display_mode, move_speed)
                )
                
                self.current_window += 1
                self.progress = (self.current_window / self.total_windows) * 100
            
            if self.current_window >= self.total_windows:
                self.is_running = False

        # 更新所有弹出窗口，并移除已经结束的窗口
        self.popup_windows = [window for window in self.popup_windows if window.update()]

    def draw(self):
        # 绘制背景
        self.screen.fill(self.bg_color)
        
        # 绘制标题
        
        title_surface = self.title_font.render("妈祖保佑，高考加油", True, self.text_color)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 100))
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
        shadow_rect = shadow_surface.get_rect(center=(self.screen_width // 2 + 2, self.screen_height // 2 + 100))
        self.screen.blit(shadow_surface, shadow_rect)
        
        # 绘制主文字
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, (255, 215, 0))  # 金色
        subtitle_rect = subtitle_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 98))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # 绘制进度条
        if self.is_running:
            # 绘制进度条背景
            pygame.draw.rect(self.screen, (200, 200, 200), self.progress_bar, border_radius=10)
            # 绘制进度条填充
            current_progress = int(self.progress_bar.width * (self.progress / 100))
            progress_fill = pygame.Rect(self.progress_bar.x, self.progress_bar.y, current_progress, self.progress_bar.height)
            pygame.draw.rect(self.screen, (0, 255, 0), progress_fill, border_radius=10)
            
            # 绘制进度文本
            progress_text = f"已加油: {self.current_window}/{self.total_windows}"
            progress_surface = self.popup_font.render(progress_text, True, self.text_color)
            progress_rect = progress_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 150))
            self.screen.blit(progress_surface, progress_rect)
        
        # 绘制所有弹出窗口
        for window in self.popup_windows:
            window.draw(self.screen)
        
        # 更新显示
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
            self.clock.tick(30) # 设置为每秒60帧
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = StudentEncouragementApp()
    app.run() 
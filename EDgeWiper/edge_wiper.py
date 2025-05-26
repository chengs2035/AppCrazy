import pygame
import os
import sys
import ctypes
from ctypes import wintypes
import math
import random

class EdgeWiper:
    def __init__(self):
        # 初始化Pygame
        pygame.init()
        
        # 设置窗口
        self.margin = 50  # 边距
        self.content_width = 600
        self.content_height = 800
        self.width = self.content_width + 2 * self.margin
        self.height = self.content_height + 2 * self.margin
        
        # 创建无边框窗口
        flags = pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode((self.width, self.height), flags)
        pygame.display.set_caption("擦边工具 v1.0")
        
        # 设置窗口置顶
        if sys.platform.startswith('win'):
            self.hwnd = pygame.display.get_wm_info()["window"]
            # 设置窗口样式
            style = ctypes.windll.user32.GetWindowLongW(self.hwnd, -20)  # GWL_EXSTYLE
            style |= 0x00000008  # WS_EX_TOPMOST
            ctypes.windll.user32.SetWindowLongW(self.hwnd, -20, style)
            # 设置窗口置顶
            ctypes.windll.user32.SetWindowPos(self.hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)  # HWND_TOPMOST
        
        # 设置颜色
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)  # 黑客绿
        self.DARK_GREEN = (0, 200, 0)
        self.BRIGHT_GREEN = (0, 255, 128)
        self.GRAY = (20, 20, 20)  # 深灰色背景
        
        # 加载图片
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "images", "bu.png")
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        
        # 创建字体
        try:
            # 尝试使用系统中文字体
            if sys.platform.startswith('win'):
                # Windows系统
                font_names = ['microsoftyahei', 'msyh', 'simhei', 'simsun']
                font_loaded = False
                for font_name in font_names:
                    try:
                        self.font = pygame.font.SysFont(font_name, 36)
                        self.small_font = pygame.font.SysFont(font_name, 20)  # 小字体
                        # 测试字体是否支持中文
                        test_text = self.font.render("测试", True, self.GREEN)
                        if test_text.get_width() > 0:
                            print(f"成功加载字体: {font_name}")
                            font_loaded = True
                            break
                    except:
                        continue
                if not font_loaded:
                    raise Exception("无法加载Windows中文字体")
            elif sys.platform.startswith('darwin'):
                # macOS系统
                self.font = pygame.font.SysFont('pingfang', 36)
                self.small_font = pygame.font.SysFont('pingfang', 20)
            else:
                # Linux系统
                self.font = pygame.font.SysFont('notosanscjk', 36)
                self.small_font = pygame.font.SysFont('notosanscjk', 20)
        except:
            # 如果系统字体不可用，尝试加载自定义字体
            try:
                font_path = os.path.join(script_dir, "fonts", "msyh.ttc")  # 微软雅黑字体
                self.font = pygame.font.Font(font_path, 36)
                self.small_font = pygame.font.Font(font_path, 20)
            except:
                # 如果都失败了，使用默认字体
                self.font = pygame.font.Font(None, 36)
                self.small_font = pygame.font.Font(None, 20)
                print("警告：无法加载中文字体，文字可能显示为乱码")
        
        # 创建按钮
        self.button_rect = pygame.Rect(
            self.margin + self.content_width//2 - 100,
            self.margin + self.content_height - 100,
            200, 50
        )
        
        # 动画相关变量
        self.animation_running = False
        self.current_position = 0
        self.clock = pygame.time.Clock()
        self.wipe_time = 0  # 用于计算摆动效果
        
        # 窗口拖动相关变量
        self.dragging = False
        self.drag_offset = (0, 0)
        
        # 黑客风格动态效果
        self.matrix_chars = []
        self.init_matrix_chars()
        
        # 进度条相关变量
        self.loading = False
        self.progress = 0
        self.loading_texts = [
            "正在初始化系统...",
            "扫描目标系统...",
            "分析系统漏洞...",
            "注入渗透代码...",
            "绕过安全防护...",
            "建立后门连接...",
            "数据加密传输...",
            "清理入侵痕迹..."
        ]
        self.current_text_index = 0
        self.text_change_time = 0
        self.scan_line_pos = 0
        
        # 倒计时相关变量
        self.countdown = False
        self.countdown_number = 3
        self.countdown_time = 0
        self.show_start_text = False
        self.start_text_time = 0
        
        # 创建大号字体用于倒计时
        try:
            if sys.platform.startswith('win'):
                self.big_font = pygame.font.SysFont('microsoftyahei', 200)
            elif sys.platform.startswith('darwin'):
                self.big_font = pygame.font.SysFont('pingfang', 200)
            else:
                self.big_font = pygame.font.SysFont('notosanscjk', 200)
        except:
            self.big_font = pygame.font.Font(None, 200)
        
    def init_matrix_chars(self):
        # 初始化矩阵字符
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        for _ in range(100):  # 增加字符数量到100个
            x = random.randint(self.margin, self.margin + self.content_width)
            y = random.randint(self.margin, self.margin + self.content_height)
            speed = random.randint(2, 5)  # 增加速度范围
            char = random.choice(chars)
            self.matrix_chars.append({"x": x, "y": y, "speed": speed, "char": char})
        
    def draw_matrix_effect(self):
        # 绘制矩阵效果
        for char in self.matrix_chars:
            # 随机调整字符的亮度
            brightness = random.randint(0, 255)
            color = (0, brightness, 0)
            text = self.small_font.render(char["char"], True, color)
            self.screen.blit(text, (char["x"], char["y"]))
            char["y"] += char["speed"]
            if char["y"] > self.margin + self.content_height:
                char["y"] = self.margin
                char["x"] = random.randint(self.margin, self.margin + self.content_width)
                char["char"] = random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[]{}|;:,.<>?/~`")
                char["speed"] = random.randint(2, 5)  # 重置速度
        
    def get_window_pos(self):
        if sys.platform.startswith('win'):
            rect = wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(self.hwnd, ctypes.byref(rect))
            return rect.left, rect.top
        return 0, 0
        
    def set_window_pos(self, x, y):
        if sys.platform.startswith('win'):
            ctypes.windll.user32.SetWindowPos(self.hwnd, -1, x, y, 0, 0, 0x0001 | 0x0002)
        
    def draw_button(self, text):
        # 绘制按钮
        pygame.draw.rect(self.screen, self.GRAY, self.button_rect)
        pygame.draw.rect(self.screen, self.GREEN, self.button_rect, 2)
        
        # 绘制按钮文字
        text_surface = self.font.render(text, True, self.GREEN)
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
    def draw_title(self):
        # 绘制标题
        title = self.font.render("擦边工具 v1.0", True, self.GREEN)
        title_rect = title.get_rect(center=(self.width//2, self.margin + 50))
        self.screen.blit(title, title_rect)
        
    def get_image_position(self):
        # 计算图片在边框上的位置
        total_distance = 2 * (self.content_width + self.content_height)
        current_pos = self.current_position % total_distance
        
        # 图片大小的一半，用于居中显示
        image_half = 25  # 50/2
        
        # 计算摆动效果
        wipe_offset = math.sin(self.wipe_time * 20) * 10  # 摆动幅度为10像素，频率为20
        
        if current_pos < self.content_width:  # 上边框
            x = self.margin + current_pos - image_half
            y = self.margin - image_half + wipe_offset  # 垂直方向摆动
        elif current_pos < self.content_width + self.content_height:  # 右边框
            x = self.margin + self.content_width - image_half - wipe_offset  # 水平方向摆动
            y = self.margin + current_pos - self.content_width - image_half
        elif current_pos < 2 * self.content_width + self.content_height:  # 下边框
            x = self.margin + 2 * self.content_width + self.content_height - current_pos - image_half
            y = self.margin + self.content_height - image_half - wipe_offset  # 垂直方向摆动
        else:  # 左边框
            x = self.margin - image_half + wipe_offset  # 水平方向摆动
            y = self.margin + 2 * (self.content_width + self.content_height) - current_pos - image_half
            
        return x, y
        
    def draw_slogan(self):
        # 绘制标语
        slogan = self.small_font.render("科学擦边，安全可靠...", True, self.BRIGHT_GREEN)
        slogan_rect = slogan.get_rect(center=(self.width//2, self.button_rect.bottom + 20))
        self.screen.blit(slogan, slogan_rect)
        
    def draw_loading_bar(self):
        if not self.loading:
            return
            
        # 绘制进度条背景
        bar_width = self.content_width - 100
        bar_height = 20
        bar_x = self.margin + 50
        bar_y = self.margin + self.content_height - 200
        
        # 绘制外框
        pygame.draw.rect(self.screen, self.GREEN, (bar_x-2, bar_y-2, bar_width+4, bar_height+4), 2)
        
        # 绘制进度条
        progress_width = int(bar_width * (self.progress / 100))
        pygame.draw.rect(self.screen, self.GREEN, (bar_x, bar_y, progress_width, bar_height))
        
        # 绘制扫描线效果
        scan_line_x = bar_x + progress_width
        pygame.draw.line(self.screen, self.BRIGHT_GREEN, 
                        (scan_line_x, bar_y-5), 
                        (scan_line_x, bar_y+bar_height+5), 2)
        
        # 绘制进度文字
        progress_text = f"{int(self.progress)}%"
        text = self.small_font.render(progress_text, True, self.GREEN)
        text_rect = text.get_rect(center=(bar_x + bar_width + 30, bar_y + bar_height//2))
        self.screen.blit(text, text_rect)
        
        # 绘制当前加载状态
        current_time = pygame.time.get_ticks()
        if current_time - self.text_change_time > 1000:  # 每秒更新一次文字
            self.current_text_index = (self.current_text_index + 1) % len(self.loading_texts)
            self.text_change_time = current_time
            
        status_text = self.loading_texts[self.current_text_index]
        text = self.small_font.render(status_text, True, self.BRIGHT_GREEN)
        text_rect = text.get_rect(center=(self.width//2, bar_y - 30))
        self.screen.blit(text, text_rect)
        
        # 绘制装饰性元素
        for i in range(5):
            x = bar_x + (bar_width * i // 4)
            pygame.draw.line(self.screen, self.GREEN, 
                           (x, bar_y-5), 
                           (x, bar_y+bar_height+5), 1)
        
    def draw_countdown(self):
        if not self.countdown and not self.show_start_text:
            return
            
        if self.countdown:
            # 绘制倒计时数字
            text = self.big_font.render(str(self.countdown_number), True, self.BRIGHT_GREEN)
            text_rect = text.get_rect(center=(self.width//2, self.height//2))
            self.screen.blit(text, text_rect)
            
            # 添加发光效果
            for i in range(3):
                glow_color = (0, 255 - i*50, 0)
                glow_text = self.big_font.render(str(self.countdown_number), True, glow_color)
                glow_rect = glow_text.get_rect(center=(self.width//2 + i*2, self.height//2 + i*2))
                self.screen.blit(glow_text, glow_rect)
        elif self.show_start_text:
            # 绘制开始文字
            text = self.font.render("现在将开始擦边", True, self.BRIGHT_GREEN)
            text_rect = text.get_rect(center=(self.width//2, self.height//2))
            self.screen.blit(text, text_rect)
            
            # 添加发光效果
            for i in range(3):
                glow_color = (0, 255 - i*50, 0)
                glow_text = self.font.render("现在将开始擦边", True, glow_color)
                glow_rect = glow_text.get_rect(center=(self.width//2 + i*2, self.height//2 + i*2))
                self.screen.blit(glow_text, glow_rect)
        
    def run(self):
        running = True
        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键点击
                        if self.button_rect.collidepoint(event.pos):
                            if not self.animation_running and not self.loading:
                                self.loading = True
                                self.progress = 0
                                self.current_text_index = 0
                                self.text_change_time = pygame.time.get_ticks()
                        else:
                            # 开始拖动窗口
                            self.dragging = True
                            mouse_x, mouse_y = event.pos
                            window_x, window_y = self.get_window_pos()
                            self.drag_offset = (window_x - mouse_x, window_y - mouse_y)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # 左键释放
                        self.dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        mouse_x, mouse_y = event.pos
                        window_x = mouse_x + self.drag_offset[0]
                        window_y = mouse_y + self.drag_offset[1]
                        self.set_window_pos(window_x, window_y)
                            
            # 清空屏幕
            self.screen.fill(self.BLACK)
            
            # 绘制内容区域背景
            content_rect = pygame.Rect(self.margin, self.margin, self.content_width, self.content_height)
            pygame.draw.rect(self.screen, self.GRAY, content_rect)
            pygame.draw.rect(self.screen, self.GREEN, content_rect, 2)
            
            # 绘制矩阵效果
            self.draw_matrix_effect()
            
            # 绘制标题
            self.draw_title()
            
            # 更新动画
            if self.animation_running:
                x, y = self.get_image_position()
                self.screen.blit(self.image, (x, y))
                
                self.current_position += 5
                self.wipe_time += 0.016  # 约60帧每秒
                
                # 检查是否完成一圈
                if self.current_position >= 2 * (self.content_width + self.content_height):
                    self.animation_running = False
                    
            # 绘制进度条
            self.draw_loading_bar()
            
            # 绘制倒计时
            self.draw_countdown()
            
            # 绘制按钮
            if self.loading:
                button_text = "系统入侵中..."
            elif self.countdown or self.show_start_text:
                button_text = "准备开始..."
            elif self.animation_running:
                button_text = "擦边中..."
            elif self.current_position == 0:
                button_text = "开始擦边"
            else:
                button_text = "擦边成功"
            self.draw_button(button_text)
            
            # 绘制标语
            self.draw_slogan()
            
            # 更新显示
            pygame.display.flip()
            
            # 控制帧率
            self.clock.tick(60)
            
            # 更新进度条
            if self.loading:
                self.progress += 0.5  # 控制进度条速度
                if self.progress >= 100:
                    self.loading = False
                    self.countdown = True
                    self.countdown_number = 3
                    self.countdown_time = pygame.time.get_ticks()
                    self.progress = 0
            
            # 更新倒计时
            if self.countdown:
                current_time = pygame.time.get_ticks()
                if current_time - self.countdown_time > 1000:  # 每秒更新一次
                    self.countdown_number -= 1
                    self.countdown_time = current_time
                    if self.countdown_number < 0:
                        self.countdown = False
                        self.show_start_text = True
                        self.start_text_time = current_time
            
            # 更新开始文字
            if self.show_start_text:
                current_time = pygame.time.get_ticks()
                if current_time - self.start_text_time > 2000:  # 显示2秒
                    self.show_start_text = False
                    self.animation_running = True
                    self.current_position = 0
                    self.wipe_time = 0
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = EdgeWiper()
    app.run() 
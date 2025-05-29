import pygame
import sys
import os
import random
import cv2
import numpy as np

# 初始化Pygame
pygame.init()

# 设置窗口
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 576
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("空调模拟器")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GOLD = (255, 215, 0)

# 加载视频背景
def load_video_background(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file: {video_path}")
            return None, 30  # 返回None和默认帧率
        
        # 获取视频信息
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # 读取所有帧
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # 调整帧大小以匹配窗口
            frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
            # 转换颜色空间从BGR到RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 转换为Pygame surface
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frames.append(frame)
        
        cap.release()
        if not frames:  # 如果没有成功读取到任何帧
            print("Error: No frames were read from the video")
            return None, 30
        return frames, fps
    except Exception as e:
        print(f"Error loading video: {str(e)}")
        return None, 30

# 加载图片资源
def load_image(name):
    return pygame.image.load(os.path.join('AirConditionerGame', 'assets', 'images', name))

# 加载并缩放背景图片（作为备选）
background = load_image('liveroom.png')
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# 尝试加载视频背景
video_path = os.path.join('AirConditionerGame', 'assets', 'videos', 'background.mp4')
video_frames, video_fps = load_video_background(video_path)

# 如果视频加载失败，使用静态背景
if video_frames is None:
    print("Using static background image instead of video")
    video_frames = [background]  # 使用静态背景图片
    video_fps = 30  # 设置默认帧率

current_frame = 0
frame_timer = 0

class Remote:
    def __init__(self):
        self.width = 85  # 170/2
        self.height = 190  # 381/2
        self.x = 470
        self.y = WINDOW_HEIGHT - 50  # 初始位置露出50像素
        self.target_y = WINDOW_HEIGHT//2  # 最终位置改为屏幕中间
        self.temperature = 26
        self.power = False
        self.image = load_image('air_remote_close.png')
        self.image_click = load_image('air_remote_click.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image_click = pygame.transform.scale(self.image_click, (self.width, self.height))
        self.button_pressed = False
        self.sparkle_effect = False
        self.sparkle_timer = 0
        self.sparkle_particles = []
        self.is_animating = False  # 控制是否正在动画中
        self.animation_speed = 5  # 动画速度
        self.mouse_entered = False  # 控制鼠标是否进入窗口
        self.is_retracting = False  # 控制是否正在退回
        
    def create_sparkle_particle(self):
        button_x = self.x + 15
        button_y = self.y + 77
        button_width = 55
        button_height = 12
        
        # 在按钮周围随机位置创建粒子
        side = random.randint(0, 3)  # 0:上, 1:右, 2:下, 3:左
        if side == 0:  # 上边
            x = random.randint(button_x - 5, button_x + button_width + 5)
            y = button_y - 5
        elif side == 1:  # 右边
            x = button_x + button_width + 5
            y = random.randint(button_y - 5, button_y + button_height + 5)
        elif side == 2:  # 下边
            x = random.randint(button_x - 5, button_x + button_width + 5)
            y = button_y + button_height + 5
        else:  # 左边
            x = button_x - 5
            y = random.randint(button_y - 5, button_y + button_height + 5)
            
        return {
            'x': x,
            'y': y,
            'size': random.randint(2, 4),
            'life': 20,  # 粒子寿命
            'color': (255, 215, 0)  # 金色
        }
        
    def is_fully_visible(self):
        return self.y <= self.target_y
        
    def is_mouse_over(self, mouse_pos):
        # 检查鼠标是否在遥控器上方（包括露出的部分）
        return (self.x <= mouse_pos[0] <= self.x + self.width and 
                self.y <= mouse_pos[1] <= self.y + self.height)
        
    def update(self):
        if self.is_retracting:  # 如果正在退回
            if self.y < WINDOW_HEIGHT - 50:  # 如果还没退到露出50像素的位置
                self.y += self.animation_speed
            else:  # 如果已经退到露出50像素的位置
                self.is_retracting = False
                self.mouse_entered = False
            return
            
        if not self.is_fully_visible() and self.mouse_entered:  # 当鼠标在遥控器上方时，开始显示
            self.is_animating = True
            
        if self.is_animating:
            # 计算目标位置
            target_y = min(WINDOW_HEIGHT//2, self.target_y)
            # 平滑移动到目标位置
            if abs(self.y - target_y) > self.animation_speed:
                if self.y > target_y:
                    self.y -= self.animation_speed
                else:
                    self.y += self.animation_speed
            else:
                self.y = target_y
                if self.y == self.target_y:
                    self.is_animating = False
        
    def draw(self, screen):
        # 绘制遥控器图片
        if self.button_pressed:
            screen.blit(self.image_click, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))
            
        # 绘制闪烁效果
        if self.sparkle_effect:
            # 更新粒子
            if len(self.sparkle_particles) < 10:  # 限制最大粒子数
                self.sparkle_particles.append(self.create_sparkle_particle())
            
            # 绘制和更新粒子
            for particle in self.sparkle_particles[:]:
                pygame.draw.circle(screen, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), 
                                 particle['size'])
                particle['life'] -= 1
                if particle['life'] <= 0:
                    self.sparkle_particles.remove(particle)
            
            # 更新闪烁计时器
            self.sparkle_timer += 1
            if self.sparkle_timer >= 60:  # 闪烁持续1秒
                self.sparkle_effect = False
                self.sparkle_timer = 0
                self.sparkle_particles.clear()

class AirConditioner:
    def __init__(self):
        self.width = 178  # 357/2
        self.height = 88  # 176/2
        self.x = 680
        self.y = 50
        self.power = False
        self.temperature = 26
        # 加载空调图片
        self.image_close = load_image('air_condition_close.png')
        self.image_open = load_image('air_condition_open.png')
        self.image_close = pygame.transform.scale(self.image_close, (self.width, self.height))
        self.image_open = pygame.transform.scale(self.image_open, (self.width, self.height))
        # 加载风效果图片
        self.wind_image1 = load_image('windy_01.png')
        self.wind_image2 = load_image('windy_02.png')
        self.wind_image1 = pygame.transform.scale(self.wind_image1, (self.width, 50))  # 调整风效果图片大小
        self.wind_image2 = pygame.transform.scale(self.wind_image2, (self.width, 50))
        self.wind_frame = 0  # 用于控制风效果动画
        self.wind_timer = 0  # 用于控制动画速度
        
    def draw(self, screen):
        # 根据电源状态选择显示图片
        if self.power:
            screen.blit(self.image_open, (self.x, self.y))
            # 显示风效果
            self.wind_timer += 1
            if self.wind_timer >= 10:  # 每10帧切换一次图片
                self.wind_frame = (self.wind_frame + 1) % 2
                self.wind_timer = 0
            # 在空调下方显示风效果
            if self.wind_frame == 0:
                screen.blit(self.wind_image1, (self.x, self.y-10 + self.height))
            else:
                screen.blit(self.wind_image2, (self.x, self.y-10 + self.height))
        else:
            screen.blit(self.image_close, (self.x, self.y))
        
        # 绘制温度显示
        if self.power:
            font = pygame.font.SysFont("microsoft yahei", 24)
            temp_text = f"{self.temperature}°C"
            text = font.render(temp_text, True, BLACK)
            text_rect = text.get_rect(center=(self.x + self.width//2, self.y + 25))
            screen.blit(text, text_rect)

def main():
    clock = pygame.time.Clock()
    remote = Remote()
    ac = AirConditioner()
    global current_frame, frame_timer
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # 检查开关按钮点击
                button_rect = pygame.Rect(remote.x + 15, remote.y + 77, 55, 12)
                if button_rect.collidepoint(mouse_pos):
                    remote.button_pressed = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                
                # 检查开关按钮释放
                button_rect = pygame.Rect(remote.x + 15, remote.y + 77, 55, 12)
                if button_rect.collidepoint(mouse_pos) and remote.button_pressed:
                    remote.power = not remote.power
                    ac.power = remote.power
                    remote.sparkle_effect = True  # 触发闪烁效果
                    remote.is_retracting = True  # 开始退回动画
                    # 如果关闭空调，重置视频帧到第一帧
                    if not remote.power:
                        current_frame = 0
                remote.button_pressed = False
                
            if event.type == pygame.MOUSEMOTION:
                # 检测鼠标是否在遥控器上方
                mouse_pos = pygame.mouse.get_pos()
                remote.mouse_entered = remote.is_mouse_over(mouse_pos)
        
        # 更新视频帧（只在空调开启时更新）
        if ac.power:
            frame_timer += 1
            if frame_timer >= 60 / video_fps:  # 根据视频帧率更新
                current_frame = (current_frame + 1) % len(video_frames)
                frame_timer = 0
        
        # 更新遥控器位置
        remote.update()
        
        # 绘制
        screen.blit(video_frames[current_frame], (0, 0))
        remote.draw(screen)
        ac.draw(screen)
        pygame.display.flip()
        
        clock.tick(60)

if __name__ == "__main__":
    main() 
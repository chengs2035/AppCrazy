import pygame
import sys
from src.mosquito import Mosquito
from src.player import Player
from src.utils import load_image, load_sound, random_position

class Game:
    def __init__(self):
        # 设置窗口
        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("拍蚊子游戏")
        
        # 设置时钟
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # 游戏状态
        self.running = True
        self.game_over = False
        
        # 加载资源
        self.load_resources()
        
        # 初始化游戏对象
        self.player = Player()
        self.mosquitos = []
        self.spawn_mosquito()
        
    def load_resources(self):
        """加载游戏资源"""
        # 加载图片
        self.background = load_image("HitMosquito/assets/images/background.png", (self.width, self.height))
        self.mosquito_img = load_image("HitMosquito/assets/images/mosquito.png", (120, 120))
        self.mosquito_close_img = load_image("HitMosquito/assets/images/mosquito_close.png", (120, 120))  # 加载第二张蚊子图片
        self.hand_cursor = load_image("HitMosquito/assets/images/hand.png", (150, 150))
        
        # 加载音效
        self.hit_sound = load_sound("HitMosquito/assets/sounds/hit.mp3")
        self.miss_sound = load_sound("HitMosquito/assets/sounds/no-96018.mp3")
        self.game_over_sound = load_sound("HitMosquito/assets/sounds/woo-hoo.mp3")
        
        # 设置自定义光标
        if self.hand_cursor:
            pygame.mouse.set_visible(False)
        
    def spawn_mosquito(self):
        """生成新的蚊子"""
        x, y = random_position(self.width, self.height, 30, 30)
        self.mosquitos.append(Mosquito(x, y))
        
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                self.handle_click(event.pos)
                
    def handle_click(self, pos):
        """处理点击事件"""
        hit = False
        for mosquito in self.mosquitos:
            if mosquito.check_hit(pos):
                mosquito.alive = False
                self.player.add_score()
                if self.hit_sound:
                    self.hit_sound.play()
                hit = True
                break
                
        if not hit:
            self.player.add_miss()
            if self.miss_sound:
                self.miss_sound.play()
                
        if self.player.is_game_over():
            self.game_over = True
            if self.game_over_sound:
                self.game_over_sound.play()
                
    def update(self):
        """更新游戏状态"""
        if self.game_over:
            return
            
        # 更新蚊子
        for mosquito in self.mosquitos[:]:
            mosquito.update(self.width, self.height)
            if not mosquito.alive:
                self.mosquitos.remove(mosquito)
                
        # 生成新蚊子
        if len(self.mosquitos) < 2:  # 减少同时存在的蚊子数量
            self.spawn_mosquito()
            
    def render(self):
        """渲染游戏画面"""
        # 绘制背景
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((255, 255, 255))
            
        # 绘制蚊子
        for mosquito in self.mosquitos:
            if self.mosquito_img and self.mosquito_close_img:
                # 根据蚊子的动画状态选择图片
                current_img = self.mosquito_img if mosquito.is_open else self.mosquito_close_img
                self.screen.blit(current_img, (mosquito.x, mosquito.y))
            else:
                mosquito.draw(self.screen)
                
        # 绘制分数
        font = pygame.font.SysFont("microsoftyahei", 36)
        
        score_text = font.render(f"分数: {self.player.get_score()}", True, (0, 0, 0))
        misses_text = font.render(f"未击中: {self.player.get_misses()}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(misses_text, (10, 50))
        
        # 绘制游戏结束文字
        if self.game_over:
            game_over_text = font.render("游戏结束！", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.width/2, self.height/2))
            self.screen.blit(game_over_text, text_rect)
            
        # 绘制自定义光标
        if self.hand_cursor:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.hand_cursor, mouse_pos)
            
        # 更新显示
        pygame.display.flip()
        
    def run(self):
        """运行游戏主循环"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS) 
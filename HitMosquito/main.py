import pygame
import sys
from src.game import Game

def main():
    # 初始化pygame
    pygame.init()
    
    # 创建游戏实例
    game = Game()
    
    # 运行游戏主循环
    game.run()
    
    # 退出pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
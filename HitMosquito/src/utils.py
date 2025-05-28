import pygame
import random

def load_image(path, size=None):
    """加载并调整图片大小"""
    try:
        image = pygame.image.load(path)
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error:
        print(f"无法加载图片: {path}")
        return None

def load_sound(path):
    """加载音效"""
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        print(f"无法加载音效: {path}")
        return None

def random_position(screen_width, screen_height, object_width, object_height):
    """生成随机位置"""
    x = random.randint(0, screen_width - object_width)
    y = random.randint(0, screen_height - object_height)
    return x, y 
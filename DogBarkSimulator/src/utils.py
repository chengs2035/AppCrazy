import os
import hashlib
import pygame
from constants import FONT_NAMES, FONT_SIZE, BLACK, SOUND_EXTENSIONS

def get_md5(text):
    """计算文本的MD5值"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def get_sound_index(md5_value, sound_count):
    """根据MD5值选择音效索引"""
    if not sound_count:
        return 0
    # 将MD5值转换为整数
    md5_int = int(md5_value, 16)
    # 使用取模运算确保索引在有效范围内
    return md5_int % sound_count

def init_font():
    """初始化字体"""
    try:
        font = None
        for font_name in FONT_NAMES:
            try:
                font = pygame.font.SysFont(font_name, FONT_SIZE)
                test_text = font.render("测试", True, BLACK)
                if test_text.get_width() > 0:
                    break
            except:
                continue
        
        if font is None:
            font = pygame.font.Font(None, FONT_SIZE)
            print("警告：未找到支持中文的字体，将使用默认字体")
        return font
    except Exception as e:
        print(f"初始化字体时出错：{str(e)}")
        return pygame.font.Font(None, FONT_SIZE)

def load_sounds(sound_dir):
    """加载音效文件"""
    sounds = []
    try:
        for file in os.listdir(sound_dir):
            if any(file.endswith(ext) for ext in SOUND_EXTENSIONS):
                sound_path = os.path.join(sound_dir, file)
                sounds.append(sound_path)
    except Exception as e:
        print(f"加载音效时出错：{str(e)}")
    return sounds

def get_asset_path(asset_type, filename):
    """获取资源文件路径"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', asset_type, filename) 
from dataclasses import dataclass
from typing import Tuple

@dataclass
class TrainImageConfig:
    """高铁图片配置类"""
    # 图片位置配置
    HEAD_POS: Tuple[int, int, int, int] = (9, 0, 1271, 255)  # 车头位置 (x, y, width, height)
    BODY_POS: Tuple[int, int, int, int] = (9, 513, 788, 768)  # 车厢位置
    TAIL_POS: Tuple[int, int, int, int] = (9, 257, 1270, 511)  # 车尾位置
    
    # 缩放配置
    SCALE_FACTOR: float = 0.2  # 默认缩小5倍
    
    # 车厢配置
    MIN_CARRIAGES: int = 1  # 最小车厢数
    MAX_CARRIAGES: int = 10  # 最大车厢数
    DEFAULT_CARRIAGES: int = 3  # 默认车厢数
    
    # 移动配置
    MOVE_SPEED: int = 5  # 移动速度
    VERTICAL_STEP: int = 50  # 垂直移动步长

# 创建全局配置实例
train_config = TrainImageConfig() 
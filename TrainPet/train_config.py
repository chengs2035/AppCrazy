from dataclasses import dataclass, field
from typing import Tuple, List

@dataclass
class TrainImageConfig:
    """高铁图片配置类"""
    # 图片位置配置
    HEAD_POS: Tuple[int, int, int, int] = (9, 0, 1271, 255)  # 车头位置 (x, y, width, height)
    BODY_POS: Tuple[int, int, int, int] = (9, 513, 788, 153)  # 车厢位置
    TAIL_POS: Tuple[int, int, int, int] = (9, 257, 1270, 255)  # 车尾位置
    
    # 缩放配置
    SCALE_FACTOR: float = 0.2  # 缩小到原来的 1/5
    
    # 车厢配置
    MIN_CARRIAGES: int = 1  # 最小车厢数
    MAX_CARRIAGES: int = 3  # 最大车厢数
    DEFAULT_CARRIAGES: int = 2  # 默认车厢数
    
    # 移动配置
    MOVE_SPEED: int = 3  # 移动速度
    VERTICAL_STEP: int = 50  # 垂直移动步长
    
    # 调试配置
    DEBUG_MODE: bool = False  # 是否启用调试模式
    
    # 旋转配置
    ROTATION_ANGLE_UP: float = 270.0    # 向上移动时的旋转角度
    ROTATION_ANGLE_DOWN: float = 90.0   # 向下移动时的旋转角度
    ROTATION_ANGLE_HORIZONTAL: float = 0.0  # 水平移动时的旋转角度
    
    # 窗口配置
    WINDOW_MARGIN: int = 20  # 窗口边距
    WINDOW_OPACITY: float = 0.9  # 窗口透明度
    
    # 动画配置
    ANIMATION_FPS: int = 60  # 动画帧率
    ANIMATION_INTERVAL: int = 16  # 动画间隔（毫秒）
    
    # 图片配置
    IMAGE_FORMATS: List[str] = field(default_factory=lambda: ['.png', '.jpg', '.jpeg'])  # 支持的图片格式
    IMAGE_CACHE_SIZE: int = 10  # 图片缓存大小
    
    # 日志配置
    LOG_LEVEL: str = 'ERROR'  # 日志级别
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # 日志格式
    LOG_DATE_FORMAT: str = '%Y-%m-%d %H:%M:%S'  # 日志日期格式
    
    # 状态配置
    STATE_TRANSITION_THRESHOLD: int = 5  # 状态转换阈值（像素）
    STATE_CHECK_INTERVAL: int = 100  # 状态检查间隔（毫秒）
    
    # 渲染配置
    RENDER_ANTIALIASING: bool = True  # 是否启用抗锯齿
    RENDER_SMOOTH_TRANSFORM: bool = True  # 是否启用平滑变换
    RENDER_DEBUG_BOX: bool = True  # 是否显示调试边界框
    RENDER_DEBUG_INFO: bool = True  # 是否显示调试信息
    
    # 事件配置
    MOUSE_DRAG_THRESHOLD: int = 5  # 鼠标拖拽阈值（像素）
    KEY_REPEAT_INTERVAL: int = 100  # 按键重复间隔（毫秒）
    
    # 错误配置
    ERROR_RETRY_COUNT: int = 3  # 错误重试次数
    ERROR_RETRY_INTERVAL: int = 1000  # 错误重试间隔（毫秒）

# 创建全局配置实例
train_config = TrainImageConfig() 
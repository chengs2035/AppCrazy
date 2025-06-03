from typing import Optional
from PySide6.QtCore import QPoint
from .train_state import TrainState
from train_config import train_config

class BorderState(TrainState):
    """边框移动状态，控制列车沿屏幕边框移动，确保图片底部（车轮）贴着边框"""
    
    def __init__(self, train_pet):
        """初始化边框状态
        
        Args:
            train_pet: 列车宠物实例
        """
        super().__init__(train_pet)  # 确保调用父类初始化
        self._current_corner = 0  # 当前所在角落（0:右下, 1:右上, 2:左上, 3:左下）
        self._move_speed = train_config.MOVE_SPEED
        
    def update_position(self):
        """更新位置"""
        current_pos = self.train_pet.pos()
        screen_width = self.train_pet.screen_width
        screen_height = self.train_pet.screen_height
        margin = train_config.WINDOW_MARGIN
        
        # 根据当前角落计算目标位置
        target_pos = self._get_target_position(current_pos, screen_width, screen_height, margin)
        
        # 计算移动方向
        dx = target_pos.x() - current_pos.x()
        dy = target_pos.y() - current_pos.y()
        
        # 计算移动步长
        if abs(dx) > abs(dy):
            # 水平移动为主
            step_x = self._move_speed if dx > 0 else -self._move_speed
            step_y = int(dy * (self._move_speed / abs(dx))) if dx != 0 else 0
        else:
            # 垂直移动为主
            step_y = self._move_speed if dy > 0 else -self._move_speed
            step_x = int(dx * (self._move_speed / abs(dy))) if dy != 0 else 0
            
        # 更新位置
        new_pos = QPoint(
            current_pos.x() + step_x,
            current_pos.y() + step_y
        )
        
        # 检查是否到达目标位置
        if self._is_at_target(new_pos, target_pos):
            # 移动到下一个角落（顺时针移动）
            old_corner = self._current_corner
            self._current_corner = (self._current_corner + 1) % 4  # 改为顺时针移动
            
            # 每次移动都调整窗口大小
            self.train_pet.adjust_window_size(True)  # 总是调整窗口大小
            
            self.train_pet.move(target_pos)
        else:
            self.train_pet.move(new_pos)
            
    def get_rotation_angle(self) -> float:
        """获取旋转角度，确保图片底部（车轮）朝向边框"""
        # 根据当前角落返回旋转角度，使图片底部朝向边框
        angles = {
            2: 0,    # 右下角：底部朝右
            3: 270,   # 右上角：底部朝上
            0: 0,  # 左上角：底部朝左
            1: 270   # 左下角：底部朝下
        }
        return angles[self._current_corner]
        
    def get_next_state(self) -> Optional['TrainState']:
        """获取下一个状态"""
        return None  # 边框状态不需要切换
        
    def _get_target_position(self, current_pos: QPoint, screen_width: int,
                           screen_height: int, margin: int) -> QPoint:
        """获取目标位置，确保图片底部（车轮）贴着边框
        
        Args:
            current_pos: 当前位置
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
            margin: 边距
            
        Returns:
            QPoint: 目标位置
        """
        # 定义四个角落的位置（顺时针顺序：右下->右上->左上->左下）
        # 位置计算确保图片底部贴着边框
        corners = [
            # 右下角：图片底部贴着屏幕底部
            QPoint(screen_width - self.train_pet.width() - margin,  # 右下 (0)
                   screen_height - self.train_pet.height()),  # 去掉底部边距
            # 右上角：图片底部贴着屏幕右侧
            QPoint(screen_width - self.train_pet.width(),  # 去掉右侧边距
                   margin),  # 右上 (1)
            # 左上角：图片底部贴着屏幕顶部
            QPoint(margin,  # 左上 (2)
                   0),  # 去掉顶部边距
            # 左下角：图片底部贴着屏幕左侧
            QPoint(0,  # 去掉左侧边距
                   screen_height - self.train_pet.height() - margin)  # 左下 (3)
        ]
        return corners[self._current_corner]
        
    def _is_at_target(self, current_pos: QPoint, target_pos: QPoint) -> bool:
        """检查是否到达目标位置
        
        Args:
            current_pos: 当前位置
            target_pos: 目标位置
            
        Returns:
            bool: 是否到达目标位置
        """
        # 允许一定的误差范围
        error_margin = self._move_speed
        return (abs(current_pos.x() - target_pos.x()) <= error_margin and
                abs(current_pos.y() - target_pos.y()) <= error_margin)
                
    @property
    def is_moving_right(self) -> bool:
        """是否向右移动"""
        # 在右下角时向右移动
        return self._current_corner == 0 
from abc import ABC, abstractmethod
from PySide6.QtCore import QPoint
from typing import Optional

class TrainState(ABC):
    """列车状态基类"""
    def __init__(self, train_pet):
        """初始化状态
        
        Args:
            train_pet: 列车宠物实例
        """
        self._train_pet = train_pet
        
    @property
    def train_pet(self):
        """获取列车宠物实例"""
        return self._train_pet
        
    @abstractmethod
    def update_position(self) -> None:
        """更新位置"""
        pass
        
    @abstractmethod
    def get_next_state(self) -> Optional['TrainState']:
        """获取下一个状态"""
        pass
        
    @abstractmethod
    def get_rotation_angle(self) -> float:
        """获取旋转角度"""
        pass
        
    def is_moving_vertical(self) -> bool:
        """是否正在垂直移动"""
        return False
        
    def is_moving_horizontal(self) -> bool:
        """是否正在水平移动"""
        return False 
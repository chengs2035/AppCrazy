from .train_state import TrainState
from PySide6.QtCore import QPoint
from typing import Optional

class VerticalState(TrainState):
    """垂直移动状态"""
    def __init__(self, train):
        super().__init__(train)
        self._is_moving_up = train.pos().y() > train.vertical_target
        
    def update_position(self) -> None:
        """更新位置"""
        current_pos = self.train.pos()
        x = current_pos.x()
        y = current_pos.y()
        
        if self._is_moving_up:
            y -= self.train.move_speed
            if y <= self.train.vertical_target:
                y = self.train.vertical_target
        else:
            y += self.train.move_speed
            if y >= self.train.vertical_target:
                y = self.train.vertical_target
                
        self.train.move(QPoint(x, y))
        
    def get_next_state(self) -> Optional[TrainState]:
        """获取下一个状态"""
        from .horizontal_state import HorizontalState
        
        current_pos = self.train.pos()
        if (self._is_moving_up and current_pos.y() <= self.train.vertical_target) or \
           (not self._is_moving_up and current_pos.y() >= self.train.vertical_target):
            return HorizontalState(self.train, not self.train.is_moving_right)
        return None
        
    def get_rotation_angle(self) -> float:
        """获取旋转角度"""
        return 270.0 if self._is_moving_up else 90.0
        
    def is_moving_vertical(self) -> bool:
        """是否正在垂直移动"""
        return True
        
    @property
    def is_moving_up(self) -> bool:
        """是否向上移动"""
        return self._is_moving_up 
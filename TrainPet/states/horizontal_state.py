from .train_state import TrainState
from PySide6.QtCore import QPoint
from typing import Optional

class HorizontalState(TrainState):
    """水平移动状态"""
    def __init__(self, train, is_moving_right: bool = True):
        super().__init__(train)
        self._is_moving_right = is_moving_right
        
    def update_position(self) -> None:
        """更新位置"""
        current_pos = self.train.pos()
        x = current_pos.x()
        y = current_pos.y()
        
        if self._is_moving_right:
            x += self.train.move_speed
            if x >= self.train.screen_width - self.train.width():
                x = self.train.screen_width - self.train.width()
                self._is_moving_right = False
                self.train.current_row += 1
                self.train.vertical_target = self.train.current_row * self.train.vertical_step
                if self.train.vertical_target >= self.train.screen_height - self.train.height():
                    self.train.vertical_target = 0
                    self.train.current_row = 0
        else:
            x -= self.train.move_speed
            if x <= 0:
                x = 0
                self._is_moving_right = True
                self.train.current_row += 1
                self.train.vertical_target = self.train.current_row * self.train.vertical_step
                if self.train.vertical_target >= self.train.screen_height - self.train.height():
                    self.train.vertical_target = 0
                    self.train.current_row = 0
                    
        self.train.move(QPoint(x, y))
        
    def get_next_state(self) -> Optional[TrainState]:
        """获取下一个状态"""
        from .vertical_state import VerticalState
        
        current_pos = self.train.pos()
        if (self._is_moving_right and current_pos.x() >= self.train.screen_width - self.train.width()) or \
           (not self._is_moving_right and current_pos.x() <= 0):
            return VerticalState(self.train)
        return None
        
    def get_rotation_angle(self) -> float:
        """获取旋转角度"""
        return 0.0
        
    def is_moving_horizontal(self) -> bool:
        """是否正在水平移动"""
        return True
        
    @property
    def is_moving_right(self) -> bool:
        """是否向右移动"""
        return self._is_moving_right 
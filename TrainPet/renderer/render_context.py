from dataclasses import dataclass
from PySide6.QtCore import QPoint, QSize
from PySide6.QtGui import QPainter

@dataclass
class RenderContext:
    """渲染上下文，管理渲染状态和参数"""
    painter: QPainter  # 画笔对象
    window_size: QSize  # 窗口大小
    scale_factor: float  # 缩放因子
    rotation_angle: float  # 旋转角度
    center_point: QPoint  # 旋转中心点
    debug_mode: bool  # 调试模式
    
    def save_state(self):
        """保存当前渲染状态"""
        self.painter.save()
        
    def restore_state(self):
        """恢复渲染状态"""
        self.painter.restore()
        
    def translate(self, point: QPoint):
        """平移坐标系"""
        self.painter.translate(point)
        
    def rotate(self, angle: float):
        """旋转坐标系"""
        self.painter.rotate(angle)
        
    def scale(self, factor: float):
        """缩放坐标系"""
        self.painter.scale(factor, factor)
        
    def get_center_point(self) -> QPoint:
        """获取窗口中心点"""
        return QPoint(
            self.window_size.width() // 2,
            self.window_size.height() // 2
        )
        
    def apply_transform(self):
        """应用变换矩阵"""
        if self.rotation_angle != 0:
            center = self.center_point or self.get_center_point()
            self.translate(center)
            self.rotate(self.rotation_angle)
            self.translate(-center)
            
    def clear_transform(self):
        """清除变换矩阵"""
        self.painter.resetTransform()
        
    def __enter__(self):
        """上下文管理器入口"""
        self.save_state()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.restore_state() 
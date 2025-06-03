from PySide6.QtCore import QSize, QPoint, Qt
from PySide6.QtGui import QPixmap, QTransform
from typing import Optional

class TrainComponent:
    """列车组件基类"""
    def __init__(self, pixmap: QPixmap, position: QPoint, scale_factor: float = 1.0):
        self._original_pixmap = pixmap
        self._position = position
        self._scale_factor = scale_factor
        self._rotation_angle = 0
        
    @property
    def original_pixmap(self) -> QPixmap:
        """获取原始图片"""
        return self._original_pixmap
        
    @property
    def scaled_size(self) -> QSize:
        """获取缩放后的尺寸"""
        return QSize(
            int(self._original_pixmap.width() * self._scale_factor),
            int(self._original_pixmap.height() * self._scale_factor)
        )
        
    @property
    def position(self) -> QPoint:
        """获取位置"""
        return self._position
        
    @position.setter
    def position(self, pos: QPoint):
        """设置位置"""
        self._position = pos
        
    @property
    def rotation_angle(self) -> float:
        """获取旋转角度"""
        return self._rotation_angle
        
    @rotation_angle.setter
    def rotation_angle(self, angle: float):
        """设置旋转角度"""
        self._rotation_angle = angle
        
    def get_scaled_pixmap(self) -> QPixmap:
        """获取缩放后的图片"""
        return self._original_pixmap.scaled(
            self.scaled_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
    def get_rotated_pixmap(self) -> QPixmap:
        """获取旋转后的图片"""
        if self._rotation_angle == 0:
            return self.get_scaled_pixmap()
            
        pixmap = self.get_scaled_pixmap()
        transform = QTransform()
        transform.translate(pixmap.width() / 2, pixmap.height() / 2)
        transform.rotate(self._rotation_angle)
        transform.translate(-pixmap.width() / 2, -pixmap.height() / 2)
        return pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation) 
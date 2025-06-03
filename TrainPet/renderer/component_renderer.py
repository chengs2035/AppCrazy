
from typing import Dict, Optional
from PySide6.QtCore import QPoint, QSize, Qt
from PySide6.QtGui import QPixmap, QPainter, QTransform
from .render_context import RenderContext

class ComponentRenderer:
    """组件渲染器，负责单个组件的渲染"""
    def __init__(self):
        
        # 缓存变换后的图片
        self._cache: Dict[str, QPixmap] = {}
        
    def render_component(self, context: RenderContext, pixmap: QPixmap, 
                        position: QPoint, scale_factor: float = 1.0,
                        rotation_angle: float = 0.0, is_mirrored: bool = False) -> None:
        """渲染单个组件
        
        Args:
            context: 渲染上下文
            pixmap: 原始图片
            position: 渲染位置
            scale_factor: 缩放因子
            rotation_angle: 旋转角度
            is_mirrored: 是否水平镜像
        """
        # 计算缓存键
        cache_key = f"{pixmap.cacheKey()}_{scale_factor}_{rotation_angle}_{is_mirrored}"
        
        # 获取或创建变换后的图片
        transformed_pixmap = self._get_transformed_pixmap(
            pixmap, scale_factor, rotation_angle, cache_key, is_mirrored
        )
        
        # 计算实际渲染位置
        render_pos = self._calculate_render_position(
            context, position, transformed_pixmap.size()
        )
        
        # 渲染图片
        with context:
            context.painter.drawPixmap(render_pos, transformed_pixmap)
            
            
    def _get_transformed_pixmap(self, pixmap: QPixmap, scale_factor: float,
                              rotation_angle: float, cache_key: str,
                              is_mirrored: bool = False) -> QPixmap:
        """获取变换后的图片
        
        Args:
            pixmap: 原始图片
            scale_factor: 缩放因子
            rotation_angle: 旋转角度
            cache_key: 缓存键
            is_mirrored: 是否水平镜像
            
        Returns:
            QPixmap: 变换后的图片
        """
        # 检查缓存
        if cache_key in self._cache:
            
            return self._cache[cache_key]
            
        # 计算缩放后的尺寸
        scaled_size = QSize(
            int(pixmap.width() * scale_factor),
            int(pixmap.height() * scale_factor)
        )
        
        # 缩放图片
        scaled_pixmap = pixmap.scaled(
            scaled_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        # 创建变换矩阵
        transform = QTransform()
        
        # 如果需要镜像
        if is_mirrored:
            # 水平镜像
            transform.scale(-1, 1)
            transform.translate(-scaled_pixmap.width(), 0)
            
        # 如果需要旋转
        if rotation_angle != 0:
            # 移动到中心点
            transform.translate(scaled_pixmap.width() / 2, scaled_pixmap.height() / 2)
            # 旋转
            transform.rotate(rotation_angle)
            # 移回原位
            transform.translate(-scaled_pixmap.width() / 2, -scaled_pixmap.height() / 2)
            
        # 应用变换
        transformed = scaled_pixmap.transformed(
            transform,
            Qt.TransformationMode.SmoothTransformation
        )
            
        # 缓存结果
        self._cache[cache_key] = transformed
    
        return transformed
        
    def _calculate_render_position(self, context: RenderContext,
                                 position: QPoint, size: QSize) -> QPoint:
        """计算实际渲染位置
        
        Args:
            context: 渲染上下文
            position: 目标位置
            size: 图片尺寸
            
        Returns:
            QPoint: 实际渲染位置
        """
        # 如果位置是相对于窗口中心的
        if position.x() == 0 and position.y() == 0:
            return QPoint(
                (context.window_size.width() - size.width()) // 2,
                (context.window_size.height() - size.height()) // 2
            )
        return position
        
    def _draw_debug_info(self, context: RenderContext,
                        position: QPoint, size: QSize) -> None:
        """绘制调试信息
        
        Args:
            context: 渲染上下文
            position: 渲染位置
            size: 图片尺寸
        """
        # 保存当前画笔状态
        context.save_state()
        
        try:
            # 设置画笔
            context.painter.setPen(Qt.PenStyle.SolidLine)
            context.painter.setBrush(Qt.BrushStyle.NoBrush)
            
            # 绘制边界框
            context.painter.drawRect(position.x(), position.y(),
                                   size.width(), size.height())
            
            # 绘制尺寸信息
            context.painter.drawText(
                position.x(), position.y() - 5,
                f"{size.width()}x{size.height()}"
            )
            
        finally:
            # 恢复画笔状态
            context.restore_state()
            
    def clear_cache(self):
        """清除图片缓存"""
        
        self._cache.clear() 

from typing import List, Optional
from PySide6.QtCore import QPoint, QSize, Qt
from PySide6.QtGui import QPainter, QColor
from .render_context import RenderContext
from .component_renderer import ComponentRenderer
from components.train_component import TrainComponent

class TrainRenderer:
    """列车渲染器，负责整体渲染流程"""
    def __init__(self, debug_mode: bool = False):
        self._debug_mode = debug_mode

        # 创建组件渲染器
        self._component_renderer = ComponentRenderer()
        
      
        
    def render(self, painter: QPainter, components: List[TrainComponent],
              window_size: QSize, scale_factor: float = 1.0,
              rotation_angle: float = 0.0, center_point: Optional[QPoint] = None,
              is_mirrored: bool = False) -> None:
        """渲染列车
        
        Args:
            painter: 画笔对象
            components: 列车组件列表
            window_size: 窗口大小
            scale_factor: 缩放因子
            rotation_angle: 旋转角度
            center_point: 旋转中心点
            is_mirrored: 是否水平镜像
        """
        if not components:
            
            return
            
        # 创建渲染上下文
        context = RenderContext(
            painter=painter,
            window_size=window_size,
            scale_factor=scale_factor,
            rotation_angle=rotation_angle,
            center_point=center_point,
            debug_mode=self._debug_mode
        )
        
        # 计算组件位置
        positions = self._calculate_component_positions(
            context, components
        )
        
        # 渲染每个组件
        for i, (component, position) in enumerate(zip(components, positions)):
            self._component_renderer.render_component(
                context=context,
                pixmap=component.original_pixmap,
                position=position,
                scale_factor=scale_factor,
                rotation_angle=rotation_angle,
                is_mirrored=is_mirrored
            )
            
        # 绘制调试信息
        if self._debug_mode:
            self._draw_debug_info(context, components, positions)
        
    def _calculate_component_positions(self, context: RenderContext,
                                    components: List[TrainComponent]) -> List[QPoint]:
        """计算组件位置
        
        Args:
            context: 渲染上下文
            components: 组件列表
            
        Returns:
            List[QPoint]: 组件位置列表
        """
        positions = []
        current_x = 0
        
        # 计算总宽度
        total_width = sum(
            int(comp.original_pixmap.width() * context.scale_factor)
            for comp in components
        )
        
        # 计算起始位置（水平居中）
        start_x = (context.window_size.width() - total_width) // 2
        
        # 计算每个组件的位置
        for component in components:
            # 计算组件宽度
            width = int(component.original_pixmap.width() * context.scale_factor)
            
            # 计算垂直位置（垂直居中）
            y = (context.window_size.height() - 
                 int(component.original_pixmap.height() * context.scale_factor)) // 2
            
            # 添加位置
            positions.append(QPoint(start_x + current_x, y))
            current_x += width
            
        return positions
        
    def _draw_debug_info(self, context: RenderContext,
                        components: List[TrainComponent],
                        positions: List[QPoint]) -> None:
        """绘制调试信息
        
        Args:
            context: 渲染上下文
            components: 组件列表
            positions: 位置列表
        """
        with context:
            # 设置画笔
            context.painter.setPen(QColor(255, 0, 0))  # 红色
            context.painter.setBrush(Qt.BrushStyle.NoBrush)
            
            # 绘制旋转角度
            context.painter.drawText(
                10, 20,
                f"旋转角度: {context.rotation_angle}°"
            )
            
            # 绘制旋转中心点
            if context.center_point:
                context.painter.setBrush(Qt.BrushStyle.SolidPattern)
                context.painter.drawEllipse(context.center_point, 5, 5)
                
            # 绘制组件信息
            for i, (component, position) in enumerate(zip(components, positions)):
                # 计算组件尺寸
                width = int(component.original_pixmap.width() * context.scale_factor)
                height = int(component.original_pixmap.height() * context.scale_factor)
                
                # 绘制组件信息
                context.painter.drawText(
                    position.x(), position.y() - 20,
                    f"组件 {i+1}: {width}x{height}"
                )
                
    def clear_cache(self):
        """清除渲染缓存"""
        self._component_renderer.clear_cache()
        
    @property
    def debug_mode(self) -> bool:
        """获取调试模式状态"""
        return self._debug_mode
        
    @debug_mode.setter
    def debug_mode(self, enabled: bool):
        """设置调试模式状态"""
        self._debug_mode = enabled 
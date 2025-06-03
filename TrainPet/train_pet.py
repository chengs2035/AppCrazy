from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QTimer, QSize
from PySide6.QtGui import QPainter, QKeyEvent, QMouseEvent
import os

from train_config import train_config
from components.train_component import TrainComponent
from states.train_state import TrainState
from states.border_state import BorderState
from renderer.train_renderer import TrainRenderer
from utils.image_loader import ImageLoader


class TrainPet(QWidget):
    """高铁宠物主窗口"""
    def __init__(self):
        super().__init__()
        
        # 初始化图片加载器
        self._image_loader = ImageLoader(
            os.path.join(os.path.dirname(__file__), 'images')
        )
        
       
        
        # 初始化渲染器
        self._renderer = TrainRenderer(debug_mode=True)
        
        # 初始化位置相关属性
        self._current_row = 0  # 当前行号
        self._vertical_target = 0  # 垂直目标位置
        
        # 加载图片资源
        try:
            self._load_images()
        except FileNotFoundError as e:
            
            QApplication.quit()
            return
            
        # 初始化组件
        self._init_components()
        
        # 初始化状态（使用边框状态）
        self._current_state: TrainState = BorderState(self)
        
        # 初始化窗口
        self._init_window()
        
        # 初始化动画
        self._init_animation()
        
    def _load_images(self):
        """加载图片资源"""
        # 加载完整图片
        try:
            self._full_image = self._image_loader.load_image('train_all.png')
        except FileNotFoundError as e:
           
            raise
            
        # 只裁剪车头图片
        try:
            self._head_image = self._image_loader.crop_image(
                self._full_image, train_config.HEAD_POS
            )
        except Exception as e:
           
            raise
            
    def _init_components(self):
        """初始化列车组件"""
        # 只创建车头组件
        self._head = TrainComponent(
            self._head_image,
            QPoint(0, 0),  # 位置将由渲染器计算
            train_config.SCALE_FACTOR
        )
        
    def _init_window(self):
        """初始化窗口"""
        # 设置窗口属性
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |  # 无边框
            Qt.WindowType.WindowStaysOnTopHint | # 置顶
            Qt.WindowType.Tool                   # 工具窗口
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 透明背景
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # 允许接收键盘事件
        
        # 获取屏幕尺寸
        screen = QApplication.primaryScreen().geometry()
        self._screen_width = screen.width()
        self._screen_height = screen.height()
        
        # 设置初始窗口大小（水平方向）
        self.adjust_window_size(is_vertical=True)
        
        # 设置初始位置（屏幕右下角）
        self.move(
            self._screen_width - self.width() - train_config.WINDOW_MARGIN,
            self._screen_height - self.height() - train_config.WINDOW_MARGIN
        )
        
    def adjust_window_size(self, is_vertical: bool):
        """调整窗口大小
        
        Args:
            is_vertical: 是否垂直移动
        """
        # 获取图片原始尺寸
        original_width = self._head_image.width()
        original_height = self._head_image.height()

        if original_width > original_height:
            width = int(original_width * train_config.SCALE_FACTOR)
            height = int(original_width * train_config.SCALE_FACTOR)
        else:
            width = int(original_height * train_config.SCALE_FACTOR)
            height = int(original_height * train_config.SCALE_FACTOR)

        # 记录当前位置
        current_pos = self.pos()
        
        # 设置新的窗口大小
        self.setFixedSize(width, height)
        
        # 保持窗口中心点不变 TODO:后面还需要调整
        center_x = current_pos.x() + self.width() // 2
        center_y = current_pos.y() + self.height() // 2
        new_x = center_x - width // 2
        new_y = center_y - height // 2
        
        # 移动到新位置
        self.move(new_x, new_y)
        
    def _init_animation(self):
        """初始化动画"""
        # 创建定时器
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update)
        self._timer.start(16)  # 约60FPS
        
    def _update(self):
        """更新状态"""
        # 更新位置
        self._current_state.update_position()
        
        # 更新旋转角度
        rotation_angle = self._current_state.get_rotation_angle()
        if rotation_angle != self._head.rotation_angle:
            old_angle = self._head.rotation_angle
            self._head.rotation_angle = rotation_angle
            
            
        # 强制重绘
        self.update()
        
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        try:
            # 只渲染车头组件
            components = [self._head]
            
            # 计算旋转中心点
            center_point = QPoint(self.width() / 2, self.height() / 2)
            
            # 渲染列车
            self._renderer.render(
                painter=painter,
                components=components,
                window_size=QSize(self.width(), self.height()),
                scale_factor=train_config.SCALE_FACTOR,
                rotation_angle=self._current_state.get_rotation_angle(),
                center_point=center_point,
                is_mirrored=self.is_moving_right  # 向右移动时进行镜像
            )
            
        finally:
            # 确保画笔正确结束
            painter.end()
        
    def keyPressEvent(self, event: QKeyEvent):
        """键盘按下事件"""
        super().keyPressEvent(event)
        
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - \
                                 self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()
            
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """鼠标双击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.close()
            
    @property
    def move_speed(self) -> int:
        """获取移动速度"""
        return train_config.MOVE_SPEED
        
    @property
    def vertical_step(self) -> int:
        """获取垂直步长"""
        return train_config.VERTICAL_STEP
        
    @property
    def screen_width(self) -> int:
        """获取屏幕宽度"""
        return self._screen_width
        
    @property
    def screen_height(self) -> int:
        """获取屏幕高度"""
        return self._screen_height
        
    @property
    def current_row(self) -> int:
        """获取当前行"""
        return self._current_row
        
    @current_row.setter
    def current_row(self, value: int):
        """设置当前行"""
        self._current_row = value
        
    @property
    def vertical_target(self) -> int:
        """获取垂直目标位置"""
        return self._vertical_target
        
    @vertical_target.setter
    def vertical_target(self, value: int):
        """设置垂直目标位置"""
        self._vertical_target = value
        
    @property
    def is_moving_right(self) -> bool:
        """是否向右移动"""
        # 使用当前状态的移动方向判断
        return self._current_state.is_moving_right if hasattr(self._current_state, 'is_moving_right') else False 
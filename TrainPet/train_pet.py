from PySide6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QApplication
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QRect, QTimer, QSize
from PySide6.QtGui import QPainter, QColor, QKeyEvent, QPixmap, QImage
from train_config import train_config
import os

class TrainImage:
    """高铁图片管理类"""
    def __init__(self):
        # 修正图片路径：直接使用TrainPet目录下的images文件夹
        self.image_path = os.path.join(os.path.dirname(__file__), 'images', 'train_all.png')
        self.full_image = QPixmap(self.image_path)
        if self.full_image.isNull():
            raise FileNotFoundError(f"无法加载图片: {self.image_path}")
            
        print(f"图片路径: {self.image_path}")
        print(f"完整图片尺寸: {self.full_image.width()}x{self.full_image.height()}")
            
        # 裁剪并缓存各部分图片
        self.head = self._crop_image(*train_config.HEAD_POS)
        self.body = self._crop_image(*train_config.BODY_POS)
        self.tail = self._crop_image(*train_config.TAIL_POS)
        
        print(f"车头尺寸: {self.head.width()}x{self.head.height()}")
        print(f"车厢尺寸: {self.body.width()}x{self.body.height()}")
        print(f"车尾尺寸: {self.tail.width()}x{self.tail.height()}")
        
    def _crop_image(self, x: int, y: int, width: int, height: int) -> QPixmap:
        """裁剪图片"""
        pixmap = self.full_image.copy(x, y, width, height)
        if pixmap.isNull():
            print(f"警告: 裁剪图片失败 - 位置({x}, {y}), 尺寸({width}, {height})")
        return pixmap
        
    def get_scaled_size(self, pixmap: QPixmap) -> QSize:
        """获取缩放后的尺寸"""
        return QSize(
            int(pixmap.width() * train_config.SCALE_FACTOR),
            int(pixmap.height() * train_config.SCALE_FACTOR)
        )

class TrainPet(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化图片资源
        try:
            self.train_image = TrainImage()
        except FileNotFoundError as e:
            print(f"错误: {e}")
            QApplication.quit()
            return
            
        # 添加移动状态变量
        self.is_moving_right = True
        self.move_speed = train_config.MOVE_SPEED
        self.vertical_step = train_config.VERTICAL_STEP
        self.current_row = 0
        self.is_moving_vertical = False
        self.vertical_target = 0
        self.debug_mode = True
        # 车厢管理
        self.carriage_count = train_config.DEFAULT_CARRIAGES
        
        # 计算窗口大小
        head_size = self.train_image.get_scaled_size(self.train_image.head)
        body_size = self.train_image.get_scaled_size(self.train_image.body)
        tail_size = self.train_image.get_scaled_size(self.train_image.tail)
        
        # 计算总宽度：车头 + 车厢数 * 车厢宽度 + 车尾
        total_width = head_size.width() + (self.carriage_count * body_size.width()) + tail_size.width()
        # 使用最大高度作为窗口高度
        total_height = max(head_size.height(), body_size.height(), tail_size.height())
        
        print(f"窗口尺寸: {total_width}x{total_height}")
        
        # 设置窗口大小
        self.setFixedSize(total_width, total_height)
        
        self.init_ui()
        self.init_animation()
        
    def init_ui(self):
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
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        
        # 初始位置（屏幕右下角）
        self.move(self.screen_width - self.width() - 20, self.screen_height - self.height() - 20)
        
    def init_animation(self):
        # 创建动画对象
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(16)  # 约60FPS的更新频率
        
        # 创建定时器用于更新位置
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(16)  # 约60FPS的更新频率
        
    def update_position(self):
        # 获取当前位置
        current_pos = self.pos()
        x = current_pos.x()
        y = current_pos.y()
        
        # 如果正在垂直移动
        if self.is_moving_vertical:
            # 计算垂直移动
            if y > self.vertical_target:
                y -= self.move_speed
                if y <= self.vertical_target:
                    y = self.vertical_target
                    self.is_moving_vertical = False
            else:
                y += self.move_speed
                if y >= self.vertical_target:
                    y = self.vertical_target
                    self.is_moving_vertical = False
        else:
            # 水平移动
            if self.is_moving_right:
                x += self.move_speed
                # 检查是否到达右边界
                if x >= self.screen_width - self.width():
                    x = self.screen_width - self.width()
                    self.is_moving_right = False
                    # 开始垂直移动
                    self.current_row += 1
                    self.vertical_target = self.current_row * self.vertical_step
                    # 检查是否需要重置到顶部
                    if self.vertical_target >= self.screen_height - self.height():
                        self.vertical_target = 0
                        self.current_row = 0
                    self.is_moving_vertical = True
            else:
                x -= self.move_speed
                # 检查是否到达左边界
                if x <= 0:
                    x = 0
                    self.is_moving_right = True
                    # 开始垂直移动
                    self.current_row += 1
                    self.vertical_target = self.current_row * self.vertical_step
                    # 检查是否需要重置到顶部
                    if self.vertical_target >= self.screen_height - self.height():
                        self.vertical_target = 0
                        self.current_row = 0
                    self.is_moving_vertical = True
        
        # 设置新位置
        new_pos = QPoint(x, y)
        self.move(new_pos)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 计算各部分图片的缩放尺寸
        head_size = self.train_image.get_scaled_size(self.train_image.head)
        body_size = self.train_image.get_scaled_size(self.train_image.body)
        tail_size = self.train_image.get_scaled_size(self.train_image.tail)
        
        # 计算垂直居中的偏移量
        y_offset = (self.height() - max(head_size.height(), body_size.height(), tail_size.height())) // 2
        
        # 绘制车头
        painter.drawPixmap(0, y_offset, head_size.width(), head_size.height(), self.train_image.head)
        
        # 绘制车厢
        current_x = head_size.width()
        for _ in range(self.carriage_count):
            painter.drawPixmap(current_x, y_offset, body_size.width(), body_size.height(), self.train_image.body)
            current_x += body_size.width()
            
        # 绘制车尾
        painter.drawPixmap(current_x, y_offset, tail_size.width(), tail_size.height(), self.train_image.tail)
        
        # 调试信息
        if hasattr(self, 'debug_mode') and self.debug_mode:
            painter.setPen(Qt.PenStyle.SolidLine)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            # 绘制车头边界
            painter.drawRect(0, y_offset, head_size.width(), head_size.height())
            # 绘制车厢边界
            current_x = head_size.width()
            for _ in range(self.carriage_count):
                painter.drawRect(current_x, y_offset, body_size.width(), body_size.height())
                current_x += body_size.width()
            # 绘制车尾边界
            painter.drawRect(current_x, y_offset, tail_size.width(), tail_size.height())
        
    def add_carriage(self):
        """增加一节车厢"""
        if self.carriage_count < train_config.MAX_CARRIAGES:
            self.carriage_count += 1
            self.update()
            
    def remove_carriage(self):
        """减少一节车厢"""
        if self.carriage_count > train_config.MIN_CARRIAGES:
            self.carriage_count -= 1
            self.update()
            
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            QApplication.quit()
        elif event.key() == Qt.Key.Key_Plus:  # 按+键增加车厢
            self.add_carriage()
        elif event.key() == Qt.Key.Key_Minus:  # 按-键减少车厢
            self.remove_carriage()
        super().keyPressEvent(event)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
            
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.close() 
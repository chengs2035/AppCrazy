import os

from PySide6.QtGui import QPixmap
from typing import Dict, Tuple, Optional

class ImageLoader:
    """图片加载工具类"""
    def __init__(self, image_dir: str):
        self._image_dir = image_dir
        self._images: Dict[str, QPixmap] = {}
        
       
        
        
    def load_image(self, filename: str) -> QPixmap:
        """加载图片
        
        Args:
            filename: 图片文件名
            
        Returns:
            QPixmap: 加载的图片
            
        Raises:
            FileNotFoundError: 图片文件不存在
        """
        # 检查缓存
        if filename in self._images:
            
            return self._images[filename]
            
        # 构建完整路径
        filepath = os.path.join(self._image_dir, filename)
        
        
        # 检查文件是否存在
        if not os.path.exists(filepath):
            
            raise FileNotFoundError(f"图片文件不存在: {filepath}")
            
        # 加载图片
        try:
            pixmap = QPixmap(filepath)
            if pixmap.isNull():
                
                raise ValueError(f"图片加载失败: {filepath}")
                
            # 缓存图片
            self._images[filename] = pixmap
            return pixmap
            
        except Exception as e:
            
            raise
            
    def crop_image(self, pixmap: QPixmap, rect: Tuple[int, int, int, int]) -> QPixmap:
        """裁剪图片
        
        Args:
            pixmap: 原始图片
            rect: 裁剪区域 (x, y, width, height)
            
        Returns:
            QPixmap: 裁剪后的图片
        """
        x, y, width, height = rect
        
        
        if x < 0 or y < 0 or width <= 0 or height <= 0 or \
           x + width > pixmap.width() or y + height > pixmap.height():
            
            raise ValueError("裁剪区域超出图片范围")
            
        try:
            cropped = pixmap.copy(x, y, width, height)
            if cropped.isNull():
                
                raise ValueError("裁剪操作失败")
                
            
            return cropped
            
        except Exception as e:
            
            raise
            
    def get_image_size(self, filename: str) -> Tuple[int, int]:
        """获取图片尺寸
        
        Args:
            filename: 图片文件名
            
        Returns:
            Tuple[int, int]: 图片尺寸 (width, height)
            
        Raises:
            KeyError: 图片未加载
        """
        if filename not in self._images:
            self._logger.error(f"图片未加载: {filename}")
            raise KeyError(f"图片未加载: {filename}")
            
        pixmap = self._images[filename]
        return pixmap.width(), pixmap.height()
        
    def clear_cache(self):
        """清除图片缓存"""
        
        self._images.clear() 
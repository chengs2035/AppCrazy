import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QObject, QEvent
from PySide6.QtGui import QKeyEvent, QKeySequence, QShortcut
from train_pet import TrainPet

def main():
    app = QApplication(sys.argv)
    
    # 创建高铁宠物实例
    pet = TrainPet()
    
    # 创建ESC快捷键
    esc_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), pet)
    esc_shortcut.activated.connect(app.quit)
    
    # 创建Shift+ESC快捷键
    shift_esc_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape | Qt.KeyboardModifier.ShiftModifier), pet)
    shift_esc_shortcut.activated.connect(app.quit)
    
    # 显示窗口
    pet.show()
    
    # 启动事件循环
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 
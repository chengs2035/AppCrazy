import sys
from PySide6.QtWidgets import QApplication
from train_pet import TrainPet

def main():
    app = QApplication(sys.argv)
    
    # 创建高铁宠物实例
    pet = TrainPet()
    pet.show()
    
    # 启动事件循环
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 
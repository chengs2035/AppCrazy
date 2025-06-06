import tkinter as tk
from tkinter import ttk
import random
import time
from collections import deque
import os

class StudentEncouragementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("妈祖保佑加油站V1.0")
        self.root.geometry("600x400")
        self.root.iconbitmap("StudentEncouragement/resources/app.ico")
        # 获取屏幕尺寸
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # 设置窗口样式
        self.root.configure(bg='#87CEEB')  # 更柔和的浅蓝色
        self.root.attributes('-alpha', 0.9)  # 设置窗口透明度
        
        # 创建主框架
        self.main_frame = tk.Frame(self.root, bg='#87CEEB')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 创建标题标签
        self.title_label = tk.Label(
            self.main_frame,
            text="妈祖保佑，平安顺遂",
            font=('华文行楷', 24, 'bold'),
            bg='#87CEEB',  # 更柔和的浅蓝色
            fg='white'
        )
        self.title_label.pack(pady=20)
        
        # 创建按钮容器框架
        self.button_frame = tk.Frame(self.main_frame, bg='#87CEEB')
        self.button_frame.pack(pady=20)
        
        # 加载妈祖图片
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            resources_dir = os.path.join(os.path.dirname(current_dir), 'resources')
            image_path = os.path.join(resources_dir, 'safer.png')
            self.mazu_image = tk.PhotoImage(file=image_path)
            # 调整图片大小
            self.mazu_image = self.mazu_image.subsample(2, 2)  # 缩小到原来的一半
        except Exception as e:
            print(f"加载图片失败: {e}")
            self.mazu_image = None
        
        # 创建图片标签
        if self.mazu_image:
            self.image_label = tk.Label(
                self.button_frame,
                image=self.mazu_image,
                bg='#87CEEB'
            )
            self.image_label.pack(side=tk.LEFT, padx=10)
        
        # 创建加油按钮
        self.cheer_button = tk.Button(
            self.button_frame,
            text="点击获得妈祖保佑",
            command=self.start_encouragement,
            font=('华文行楷', 16),
            bg='#FF0000',  # 保持红色
            fg='white',
            relief=tk.RAISED,
            borderwidth=3
        )
        self.cheer_button.pack(side=tk.LEFT, padx=10)
        
        # 创建进度条
        self.progress = ttk.Progressbar(
            self.main_frame,
            orient='horizontal',
            length=400,
            mode='determinate'
        )
        self.progress.pack(pady=10)
        self.progress.pack_forget()
        
        # 创建进度标签
        self.progress_label = tk.Label(
            self.main_frame,
            text="",
            font=('华文行楷', 12),
            bg='#87CEEB',  # 更柔和的浅蓝色
            fg='white'
        )
        self.progress_label.pack(pady=10)
        self.progress_label.pack_forget()
        
        # 加载鼓励语
        self.load_encouragements()
        
        # 初始化变量
        self.windows = []
        self.encouragement_queue = deque()
        self.total_windows = 2000  # 设置要显示的窗口数量
        self.current_window = 0
        self.is_running = False
        
        # 计算网格大小
        self.grid_size = 50  # 网格大小（像素）
        self.grid_cols = self.screen_width // self.grid_size
        self.grid_rows = self.screen_height // self.grid_size
        self.used_positions = set()  # 记录已使用的位置
        
        # 更新颜色组合
        self.color_combinations = [
            # 背景色和文字色组合
            ('#E6F3FF', '#8B0000'),  # 浅蓝色背景配深红色文字
            ('#F0F8FF', '#006400'),  # 爱丽丝蓝背景配深绿色文字
            ('#F5F5F5', '#4B0082'),  # 白色背景配靛蓝色文字
            ('#FFF0F5', '#8B4513'),  # 淡粉色背景配棕色文字
            ('#F0FFF0', '#800080'),  # 蜜瓜绿背景配紫色文字
            ('#FFFACD', '#000080'),  # 柠檬黄背景配深蓝色文字
            ('#F5F5DC', '#8B008B'),  # 米色背景配深紫色文字
            ('#E0FFFF', '#8B0000'),  # 淡青色背景配深红色文字
            ('#FFE4E1', '#006400'),  # 淡红色背景配深绿色文字
            ('#F0F8FF', '#8B4513'),  # 爱丽丝蓝背景配棕色文字
            ('#FFF0F5', '#4B0082'),  # 淡粉色背景配靛蓝色文字
            ('#F0FFF0', '#8B0000'),  # 蜜瓜绿背景配深红色文字
            ('#FFFACD', '#800080'),  # 柠檬黄背景配紫色文字
            ('#F5F5DC', '#000080'),  # 米色背景配深蓝色文字
            ('#E0FFFF', '#8B008B')   # 淡青色背景配深紫色文字
        ]

        # 随机文字颜色
        self.text_colors = [
            '#8B0000',  # 深红色
            '#006400',  # 深绿色
            '#4B0082',  # 靛蓝色
            '#8B4513',  # 棕色
            '#800080',  # 紫色
            '#000080',  # 深蓝色
            '#8B008B',  # 深紫色
            '#8B0000',  # 深红色
            '#006400',  # 深绿色
            '#4B0082'   # 靛蓝色
        ]

    def get_random_position(self):
        # 获取随机网格位置
        while True:
            col = random.randint(0, self.grid_cols - 1)
            row = random.randint(0, self.grid_rows - 1)
            pos = (col, row)
            
            if pos not in self.used_positions:
                self.used_positions.add(pos)
                # 转换为实际像素坐标
                x = col * self.grid_size
                y = row * self.grid_size
                return x, y
            
            # 如果所有位置都被使用，清空已使用位置
            if len(self.used_positions) >= self.grid_cols * self.grid_rows:
                self.used_positions.clear()

    def load_encouragements(self):
        try:
            # 获取当前文件所在目录的上级目录中的resources目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            resources_dir = os.path.join(os.path.dirname(current_dir), 'resources')
            encouragements_file = os.path.join(resources_dir, 'encouragements.txt')
            
            with open(encouragements_file, 'r', encoding='utf-8') as f:
                self.encouragements = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.encouragements = [
                "加油！你是最棒的！",
                "相信自己，你一定能行！",
                "你的努力一定会得到回报！",
            ]

    def start_encouragement(self):
        if self.is_running:
            return
            
        self.is_running = True
        self.cheer_button.config(state='disabled')
        self.progress.pack(pady=10)
        self.progress_label.pack(pady=10)
        
        # 清空队列和窗口列表
        self.encouragement_queue.clear()
        for window in self.windows:
            window.destroy()
        self.windows.clear()
        self.used_positions.clear()
        
        # 准备鼓励语队列
        for _ in range(self.total_windows):
            self.encouragement_queue.append(random.choice(self.encouragements))
        
        # 开始显示窗口
        self.show_next_window()

    def show_next_window(self):
        if not self.encouragement_queue or not self.is_running:
            self.finish_encouragement()
            return
            
        # 更新进度
        self.current_window += 1
        progress = (self.current_window / self.total_windows) * 100
        self.progress['value'] = progress
        self.progress_label.config(text=f"进度: {self.current_window}/{self.total_windows}")
        
        # 获取随机位置
        x, y = self.get_random_position()
        self.create_encouragement_window(x, y)
        
        # 安排下一个窗口
        self.root.after(5, self.show_next_window)  # 每5毫秒显示一个新窗口

    def create_encouragement_window(self, x, y):
        if not self.encouragement_queue:
            return
            
        # 创建新窗口
        window = tk.Toplevel(self.root)
        window.geometry(f"+{x}+{y}")
        window.overrideredirect(True)
        
        # 随机选择颜色组合
        colors = random.choice(self.color_combinations)
        # 随机选择文字颜色
        text_color = random.choice(self.text_colors)
        
        # 设置窗口样式
        window.configure(bg=colors[0])
        
        # 创建标签
        label = tk.Label(
            window,
            text=f"妈祖保佑\n{self.encouragement_queue.popleft()}",
            font=('华文行楷', 13, 'bold'),
            bg=colors[0],
            fg=text_color,  # 使用随机文字颜色
            padx=20,
            pady=10
        )
        label.pack()
        
        # 存储窗口引用
        self.windows.append(window)
        
        # 20秒后自动关闭
        window.after(20000, lambda: self.close_window(window))

    def close_window(self, window):
        if window in self.windows:
            self.windows.remove(window)
            window.destroy()

    def finish_encouragement(self):
        self.is_running = False
        self.cheer_button.config(state='normal')
        self.progress.pack_forget()
        self.progress_label.pack_forget()
        self.current_window = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentEncouragementApp(root)
    root.mainloop() 
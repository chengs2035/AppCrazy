import tkinter as tk
from tkinter import ttk
import random
import time
from collections import deque
import os

class StudentEncouragementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("赛博佛祖加油站V1.0")
        self.root.geometry("600x400")
        self.root.iconbitmap("StudentEncouragement/resources/app.ico")
        # 获取屏幕尺寸
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # 设置窗口样式
        self.root.configure(bg='#FFD700')  # 金色背景
        
        # 创建主框架
        self.main_frame = tk.Frame(self.root, bg='#FFD700')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 创建标题标签
        self.title_label = tk.Label(
            self.main_frame,
            text="阿弥陀佛，善哉善哉",
            font=('微软雅黑', 24, 'bold'),
            bg='#FFD700',
            fg='#8B0000'  # 深红色文字
        )
        self.title_label.pack(pady=20)
        
        # 创建加油按钮
        self.cheer_button = tk.Button(
            self.main_frame,
            text="点击获得佛祖加持",
            command=self.start_encouragement,
            font=('微软雅黑', 16),
            bg='#8B0000',  # 深红色按钮
            fg='#FFD700',  # 金色文字
            width=15,
            height=2,
            relief='raised',
            cursor='hand2'
        )
        self.cheer_button.pack(pady=20)
        
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
            font=('微软雅黑', 12),
            bg='#FFD700',
            fg='#8B0000'
        )
        self.progress_label.pack(pady=5)
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
        
        # 禅意颜色组合
        self.color_combinations = [
            # 金色系
            {'bg': '#FFD700', 'fg': '#8B0000'},  # 金色配深红
            {'bg': '#FFA500', 'fg': '#8B0000'},  # 橙色配深红
            {'bg': '#FFC0CB', 'fg': '#8B0000'},  # 粉色配深红
            # 红色系
            {'bg': '#FF0000', 'fg': '#FFD700'},  # 红色配金色
            {'bg': '#8B0000', 'fg': '#FFD700'},  # 深红配金色
            {'bg': '#CD5C5C', 'fg': '#FFD700'},  # 印度红配金色
            # 白色系
            {'bg': '#FFFFFF', 'fg': '#8B0000'},  # 白色配深红
            {'bg': '#F5F5F5', 'fg': '#8B0000'},  # 淡灰配深红
            {'bg': '#FFFAFA', 'fg': '#8B0000'},  # 雪白配深红
            # 暖色系
            {'bg': '#FFE4E1', 'fg': '#8B0000'},  # 淡粉配深红
            {'bg': '#FFF0F5', 'fg': '#8B0000'},  # 淡紫红配深红
            {'bg': '#FFEFD5', 'fg': '#8B4513'},  # 淡黄配棕色
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
        self.progress_label.pack(pady=5)
        
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
        
        # 设置窗口样式
        window.configure(bg=colors['bg'])
        
        # 创建标签
        label = tk.Label(
            window,
            text=f"阿弥陀佛\n{self.encouragement_queue.popleft()}",
            font=('微软雅黑', 12, 'bold'),
            bg=colors['bg'],
            fg=colors['fg'],
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
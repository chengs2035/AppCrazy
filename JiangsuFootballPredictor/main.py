import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import time
import random
import math

class Particle:
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.size = random.randint(2, 5)
        self.color = random.choice(['#FFD700', '#FFA500', '#FF4500', '#FF6347'])
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, 2 * math.pi)
        self.life = random.randint(20, 40)
        self.id = canvas.create_oval(x, y, x+self.size, y+self.size, fill=self.color)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.life -= 1
        self.canvas.coords(self.id, self.x, self.y, self.x+self.size, self.y+self.size)
        return self.life > 0

class FootballPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("江苏足球联赛冠军预测V1.0 AI预测，科学可信")
        self.root.geometry("800x600")
        
        # 设置程序图标
        try:
            self.root.iconbitmap("JiangsuFootballPredictor/resources/app.ico")
        except Exception as e:
            print(f"无法加载程序图标: {e}")
        
        # 创建画布用于特效
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 加载背景图片
        try:
            self.bg_image = Image.open("JiangsuFootballPredictor/resources/background.jpg")
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self.canvas, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"无法加载背景图片: {e}")
            self.bg_label = None
        
        # 创建半透明背景框
        self.frame = tk.Frame(self.canvas, bg='white')
        self.frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=300)
        
        # 设置半透明效果
        self.frame.configure(bg='white')
        self.frame.attributes = {'alpha': 0.8}
        
        # 创建标题标签
        self.title_label = tk.Label(
            self.frame,
            text="苏超冠军预测（心情舒畅版）",
            font=('微软雅黑', 20, 'bold'),
            bg='white'
        )
        self.title_label.pack(pady=20)
        
        # 创建输入框和标签
        self.input_frame = tk.Frame(self.frame, bg='white')
        self.input_frame.pack(pady=10)
        
        self.city_label = tk.Label(
            self.input_frame,
            text="请输入你所在地：",
            font=('微软雅黑', 12),
            bg='white'
        )
        self.city_label.pack(side=tk.LEFT, padx=5)
        
        # 创建预测按钮
        self.predict_button = tk.Button(
            self.frame,
            text="请填写所在地",
            command=self.button_click,
            font=('微软雅黑', 14),
            bg='#4CAF50',
            fg='white',
            width=15,
            height=2
        )
        self.predict_button.pack(pady=20)
        
        # 创建结果显示标签
        self.result_label = tk.Label(
            self.frame,
            text="",
            font=('微软雅黑', 14),
            bg='white',
            wraplength=350
        )
        self.result_label.pack(pady=10)
        
        # 创建进度条
        self.progress = ttk.Progressbar(
            self.frame,
            orient='horizontal',
            length=300,
            mode='determinate'
        )
        self.progress.pack(pady=10)
        self.progress.pack_forget()  # 初始隐藏进度条
        
        # 城市列表
        self.cities = [
            "南京", "无锡", "徐州", "常州", "苏州",
            "南通", "连云港", "淮安", "盐城", "扬州",
            "镇江", "泰州", "宿迁"
        ]

        self.ai_steps = [
            "正在连接江苏本地AI足球数据库...",
            "正在分析各方球员的八卦新闻...",
            "正在深度学习球迷的呐喊分贝...",
            "正在模拟裁判的临场心情...",
            "正在统计球场附近小吃摊数量...",
            "正在和VAR系统争论人生...",
            "正在预测球员发型对胜负的影响...",
            "正在分析天气对球的弹跳影响...",
            "正在和隔壁AI打赌...",
            "正在计算球员的星座运势...",
            "正在研究球场的风水布局...",
            "正在分析球迷的应援口号...",
            "正在研究球员的社交媒体动态...",
            "正在计算球场的WiFi信号强度...",
            "正在分析球员的午餐菜单...",
            "正在研究球场的草坪生长情况...",
            "正在计算球迷的应援道具数量...",
            "正在分析球员的宠物情况...",
            "正在研究球场的停车位数量...",
            "正在计算球员的粉丝数量...",
            "正在分析球场的厕所数量...",
            "正在研究球员的球鞋品牌...",
            "正在计算球迷的应援服装颜色...",
            "正在分析球场的照明系统...",
            "正在研究球员的社交媒体粉丝互动...",
            "正在计算球场的座位舒适度...",
            "正在分析球员的应援歌曲...",
            "正在研究球场的音响效果...",
            "正在计算球迷的应援道具种类...",
            "正在分析球员的球衣号码...",
            "正在研究球场的VIP包厢数量...",
            "正在计算球迷的应援口号长度...",
            "正在分析球员的球鞋磨损程度...",
            "正在研究球场的草皮维护情况...",
            "正在计算球迷的应援服装款式...",
            "正在分析球员的球衣颜色...",
            "正在研究球场的座位布局...",
            "正在计算球迷的应援道具价格...",
            "正在分析球员的球鞋尺码...",
            "正在研究球场的VIP通道数量...",
            "AI思考完毕，准备公布结果！"
        ]

        self.city = None
        self.state = 'input'  # 状态: input(等待输入) 或 predict(等待预测)
        self.particles = []
        self.is_celebrating = False

    def create_particles(self, x, y):
        for _ in range(20):
            self.particles.append(Particle(x, y, self.canvas))

    def update_particles(self):
        if not self.particles:
            return
        
        self.particles = [p for p in self.particles if p.update()]
        if self.particles:
            self.root.after(50, self.update_particles)
        else:
            self.is_celebrating = False

    def flash_text(self, label, colors, index=0):
        if not self.is_celebrating:
            return
        label.config(fg=colors[index])
        next_index = (index + 1) % len(colors)
        self.root.after(200, lambda: self.flash_text(label, colors, next_index))

    def celebrate_result(self):
        self.is_celebrating = True
        # 创建粒子效果
        self.create_particles(400, 300)
        self.update_particles()
        # 文字闪烁效果
        colors = ['#FFD700', '#FFA500', '#FF4500', '#FF6347', '#FF8C00']
        self.flash_text(self.result_label, colors)

    def animate_text(self, text):
        self.result_label.config(text="")
        for char in text:
            self.result_label.config(text=self.result_label.cget("text") + char)
            self.root.update()
            time.sleep(0.05)
        # 显示完文字后开始庆祝效果
        self.celebrate_result()

    def ai_thinking(self, city, step=0):
        if step == 0:
            self.result_label.config(text="")
            self.progress['value'] = 0
            self.progress.pack(pady=5)
            self.result_label.config(text="")
            self.result_label.pack(pady=5)

        if step < len(self.ai_steps):
            self.result_label.config(text=self.ai_steps[step])
            self.progress['value'] = int((step+1) * 100 / len(self.ai_steps))
            self.root.update()
            self.root.after(800, lambda: self.ai_thinking(city, step+1))
        else:
            self.progress.pack_forget()
            self.result_label.config(text="AI分析完成！")
            # 预测逻辑
            if city in self.cities:
                result = f"预测冠军是：{city}！"
            else:
                result = "冠军是全国人民的！"
            self.root.after(1000, lambda: self.animate_text(result))
            # 恢复按钮状态
            self.root.after(3000, self.reset_button)

    def button_click(self):
        if self.state == 'input':
            city = simpledialog.askstring("输入", "请输入你的所在地（如：南京市）：", parent=self.root)
            if city:
                self.city = city.strip()
                self.predict_button.config(text="AI开始预测")
                self.state = 'predict'
            else:
                messagebox.showwarning("提示", "你还没有输入所在地哦！")
        elif self.state == 'predict':
            self.predict_button.config(state='disabled')
            self.ai_thinking(self.city)

    def reset_button(self):
        self.predict_button.config(text="请填写所在地", state='normal')
        self.state = 'input'
        self.city = None
        self.is_celebrating = False
        self.result_label.config(fg='#d2691e')

if __name__ == "__main__":
    root = tk.Tk()
    app = FootballPredictorApp(root)
    root.mainloop() 
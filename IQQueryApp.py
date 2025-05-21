import tkinter as tk
from tkinter import messagebox, font
import time
import math
import random


'''
    数字雨效果
'''
class MatrixRain:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.chars = "0123456789ABCDEF"
        self.drops = []
        self.init_drops()
        
    def init_drops(self):
        # 增加间距，减少数字雨密度
        for i in range(0, self.width, 30):  # 从15改为30，减少密度
            self.drops.append({
                'x': i,
                'y': random.randint(-100, 0),
                'speed': random.randint(2, 4),  # 降低速度范围
                'length': random.randint(3, 8)  # 减少长度范围
            })
    
    def update(self):
        self.canvas.delete("matrix")
        for drop in self.drops:
            # 绘制数字
            for i in range(drop['length']):
                char = random.choice(self.chars)
                y = drop['y'] - i * 30  # 增加间距，从20改为30
                if 0 <= y < self.height:
                    # 简化透明度计算
                    alpha = 1.0 - (i / drop['length'])
                    # 使用预定义的颜色而不是每次都计算
                    if alpha > 0.7:
                        color = '#00ff00'  # 最亮
                    elif alpha > 0.4:
                        color = '#00cc00'  # 中等
                    else:
                        color = '#009900'  # 最暗
                    
                    self.canvas.create_text(
                        drop['x'], y,
                        text=char,
                        fill=color,
                        font=('Courier New', 12),
                        tags="matrix"
                    )
            
            # 更新位置
            drop['y'] += drop['speed']
            if drop['y'] > self.height:
                drop['y'] = random.randint(-100, 0)

'''
    智商查询器
    100% AI生成
    100% 原创
    100% 无bug
    100% 无广告
    100% 无水印
    100% 无后门
    100% 无病毒
    100% 无木马
    100% 无漏洞
    2025年5月21日
'''
class IQQueryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("智商查询器V1.0 AI版")
        self.root.configure(bg='#000000')
        self.root.geometry("900x1600")  # 修改为9:16比例
        self.root.icon = tk.PhotoImage(file='./icons/IQQueryApp.png')
        self.root.iconphoto(False, self.root.icon)
        
        # 创建画布用于数字雨效果
        self.canvas = tk.Canvas(root, width=900, height=1600, bg='#000000', highlightthickness=0)
        self.canvas.place(x=0, y=0)
        self.matrix_rain = MatrixRain(self.canvas, 900, 1600)
        
        # 设置自定义字体
        self.title_font = font.Font(family="Courier New", size=32, weight="bold")  # 放大标题字体
        self.label_font = font.Font(family="Courier New", size=24)  # 放大标签字体
        self.button_font = font.Font(family="Courier New", size=24, weight="bold")  # 放大按钮字体
        
        # 创建标题
        self.title_label = tk.Label(
            root,
            text="智商查询器V1.0",
            font=self.title_font,
            fg="#00ff00",
            bg='#000000'
        )
        self.title_label.place(relx=0.5, rely=0.1, anchor='center')
        
        # 创建主框架
        main_frame = tk.Frame(root, bg='#000000')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # 创建并布局GUI元素
        self.name_label = tk.Label(
            main_frame,
            text="请输入姓名：",
            font=self.label_font,
            fg="#00ff00",
            bg='#000000',
            bd=0,
            highlightthickness=0
        )
        self.name_label.pack(pady=20)  # 增加间距
        
        self.name_entry = tk.Entry(
            main_frame,
            font=self.label_font,
            bg='#000000',
            fg='#00ff00',
            insertbackground='#00ff00',
            relief='flat',
            highlightthickness=1,
            highlightbackground='#00ff00',
            highlightcolor='#00ff00'
        )
        self.name_entry.pack(pady=10, ipady=10, ipadx=20)  # 增加输入框大小
        
        self.iq_label = tk.Label(
            main_frame,
            text="您的智商为：",
            font=self.label_font,
            fg="#00ff00",
            bg='#000000'
        )
        self.iq_label.pack(pady=20)  # 增加间距
        
        self.iq_entry = tk.Entry(
            main_frame,
            font=self.label_font,
            bg='#000000',
            fg='#00ff00',
            insertbackground='#00ff00',
            relief='flat',
            highlightthickness=1,
            highlightbackground='#00ff00',
            highlightcolor='#00ff00'
        )
        self.iq_entry.pack(pady=10, ipady=10, ipadx=20)  # 增加输入框大小
        
        # 创建评语标签
        self.comment_label = tk.Label(
            main_frame,
            text="",
            font=self.label_font,
            fg="#00ff00",
            bg='#000000',
            wraplength=700  # 增加文本换行宽度
        )
        self.comment_label.pack(pady=20)  # 增加间距
        
        # 创建按钮框架
        button_frame = tk.Frame(main_frame, bg='#000000')
        button_frame.pack(pady=40)  # 增加按钮区域间距
        
        # 创建按钮样式
        button_style = {
            'font': self.button_font,
            'bg': '#000000',
            'fg': '#00ff00',
            'activebackground': '#00ff00',
            'activeforeground': '#000000',
            'relief': 'flat',
            'borderwidth': 0,
            'padx': 40,  # 增加按钮内边距
            'pady': 20   # 增加按钮内边距
        }
        
        self.query_button = tk.Button(
            button_frame,
            text="开始查询",
            command=lambda: self.animate_button_click(self.query_button, self.query_iq),
            **button_style
        )
        self.query_button.pack(padx=20)  # 增加按钮间距
        
        # 添加AI计算说明标签
        self.ai_label = tk.Label(
            main_frame,
            text="AI计算，科学合理",
            font=self.label_font,
            fg="#00ff00",
            bg='#000000'
        )
        self.ai_label.pack(pady=20)  # 增加间距
        
        # 绑定鼠标悬停事件
        for button in [self.query_button]:
            button.bind('<Enter>', lambda e, b=button: self.on_enter(b))
            button.bind('<Leave>', lambda e, b=button: self.on_leave(b))
        
        # 启动数字雨动画，降低更新频率
        self.update_matrix()
    
    def update_matrix(self):
        self.matrix_rain.update()
        self.root.after(100, self.update_matrix)  # 从50ms改为100ms，降低更新频率
    
    def animate_button_click(self, button, callback):
        """按钮点击动画效果"""
        original_bg = button.cget('bg')
        original_fg = button.cget('fg')
        
        # 缩放动画
        def scale_animation(scale=1.0, step=0.1):
            if scale <= 0.8:
                scale = 0.8
                button.configure(bg='#00ff00', fg='#000000')
                self.root.update()
                time.sleep(0.1)
                button.configure(bg=original_bg, fg=original_fg)
                callback()
                return
            
            self.root.update()
            time.sleep(0.01)
            scale_animation(scale - step)
        
        scale_animation()
    
    def on_enter(self, button):
        """鼠标悬停效果"""
        button.configure(bg='#00ff00', fg='#000000')
    
    def on_leave(self, button):
        """鼠标离开效果"""
        button.configure(bg='#000000', fg='#00ff00')
    
    def get_iq_color(self, iq):
        """根据智商值返回对应的颜色"""
        if isinstance(iq, str):
            return '#ffffff'
        if iq >= 100:
            return '#00ff00'  # 矩阵绿色
        elif iq >= 80:
            return '#00ffff'  # 青色
        elif iq >= 60:
            return '#ffff00'  # 黄色
        else:
            return '#ff0000'  # 红色
    
    def get_iq_comment(self, iq):
        """根据智商值返回评语"""
        if isinstance(iq, str):
            return "这个智商值有点神秘..."
        if iq >= 100:
            return random.choice([
                "哇！您简直就是天才！建议去拯救世界！",
                "您的智商已经突破天际，建议去火星定居！",
                "这么高的智商，您是不是偷偷吃了什么补脑神药？",
                "您的智商已经达到了AI的水平，建议去和ChatGPT比试比试！"
            ])
        elif iq >= 80:
            return random.choice([
                "不错不错，是个聪明人！",
                "您的智商已经超过了全国80%的人，继续保持！",
                "这个智商水平，建议去参加最强大脑！",
                "您的智商已经可以碾压大多数人了！"
            ])
        elif iq >= 60:
            return random.choice([
                "还行，继续努力！",
                "您的智商还有提升空间，建议多吃点核桃！",
                "这个智商水平，建议去参加《一站到底》！",
                "您的智商已经超过了及格线，可喜可贺！"
            ])
        else:
            return random.choice([
                "这个...建议多吃点核桃补补脑...",
                "您的智商可能需要充值了...",
                "这个智商水平，建议去参加《开心辞典》！",
                "您的智商已经达到了可爱水平，继续保持！"
            ])
    
    def query_iq(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("警告", "请输入姓名！")
            return
        
        # 添加查询动画效果
        self.iq_entry.delete(0, tk.END)
        self.iq_entry.insert(0, "计算中")
        self.root.update()
        
        # 动态加载动画
        for i in range(5):
            self.iq_entry.delete(0, tk.END)
            self.iq_entry.insert(0, "计算中" + "." * (i + 1))
            self.root.update()
            time.sleep(0.2)
        
        iq = self.get_iq_by_name(name)
        
        # 结果渐变动画
        self.iq_entry.delete(0, tk.END)
        self.iq_entry.insert(0, str(iq))
        color = self.get_iq_color(iq)
        self.iq_entry.configure(fg=color)
        self.root.update()
        time.sleep(0.3)
        
        # 显示评语
        comment = self.get_iq_comment(iq)
        self.comment_label.configure(text=comment, fg=color)
    
    def get_iq_by_name(self, name):
        name = name.lower()
        # 特殊人物
        special_names = {
            "关羽": 99,
            "诸葛亮": 100,
            "张飞": 60,
            "我": 200,  # 修改"我"的智商为200
            "你": 0,    # 修改"你"的智商为0
            "爱因斯坦": 200,
            "牛顿": 190,
            "达芬奇": 180,
            "爱迪生": 170,
            "岳云鹏": 80,
            "于谦": 70,
            "宋小宝": 65
        }
        
        # 检查是否是特殊人物
        if name in special_names:
            return special_names[name]
        
        # 检查是否包含特殊关键词
        if "天才" in name:
            return random.randint(150, 200)
        elif "聪明" in name:
            return random.randint(120, 150)
        elif "笨蛋" in name or "傻瓜" in name:
            return random.randint(0, 30)
        
        # 根据名字长度计算基础智商
        base_iq = len(name) * 10
        
        # 随机因素
        random_factor = random.randint(-20, 20)
        
        # 特殊规则
        if "王" in name:
            random_factor += 15  # 姓王的智商加成
        if "李" in name:
            random_factor += 10  # 姓李的智商加成
        if "张" in name:
            random_factor += 5   # 姓张的智商加成
            
        # 根据时间计算额外加成
        current_hour = time.localtime().tm_hour
        if 0 <= current_hour < 6:
            random_factor -= 10  # 熬夜会降低智商
        elif 6 <= current_hour < 12:
            random_factor += 15  # 早上智商最高
        elif 12 <= current_hour < 18:
            random_factor += 5   # 下午智商一般
        else:
            random_factor -= 5   # 晚上智商略低
            
        # 计算最终智商
        final_iq = base_iq + random_factor
        
        # 确保智商在合理范围内
        final_iq = max(0, min(200, final_iq))
        
        return final_iq
    

if __name__ == "__main__":
    root = tk.Tk()
    app = IQQueryApp(root)
    root.mainloop()

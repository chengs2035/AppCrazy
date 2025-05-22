import tkinter as tk
from tkinter import messagebox, font
import time
import os

class OpenYellowJoke:
    def __init__(self, root):
        self.root = root
        self.root.title("开黄腔工具V1.0")
        self.root.configure(bg='#000000')
        self.root.geometry("900x600")
        
        # 设置自定义字体
        self.title_font = font.Font(family="Courier New", size=32, weight="bold")
        self.button_font = font.Font(family="Courier New", size=24, weight="bold")
        
        # 创建标题框架
        title_frame = tk.Frame(root, bg='#000000')
        title_frame.place(relx=0.5, rely=0.2, anchor='center')
        
        # 创建三个标题标签
        self.label1 = tk.Label(
            title_frame,
            text="开黄",
            font=self.title_font,
            fg="#00ff00",
            bg='#000000'
        )

        self.label1.pack(side='left')
        
        self.label2 = tk.Label(
            title_frame,
            text="腔",
            font=self.title_font,
            fg="#00ff00",
            bg='#000000'
        )
        self.label2.pack(side='left')
        
        self.label3 = tk.Label(
            title_frame,
            text="工具V1.0",
            font=self.title_font,
            fg="#00ff00",
            bg='#000000'
        )
        self.label3.pack(side='left')
        
        # 创建主框架
        main_frame = tk.Frame(root, bg='#000000')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # 创建按钮样式
        button_style = {
            'font': self.button_font,
            'bg': '#000000',
            'fg': '#00ff00',
            'activebackground': '#00ff00',
            'activeforeground': '#000000',
            'relief': 'flat',
            'borderwidth': 0,
            'padx': 40,
            'pady': 20
        }
        
        # 创建按钮
        self.show_button = tk.Button(
            main_frame,
            text="点击开黄腔",
            command=lambda: self.animate_button_click(self.show_button),
            **button_style
        )
        self.show_button.pack(pady=20)
        
        # 绑定鼠标悬停事件
        self.show_button.bind('<Enter>', lambda e: self.on_enter(self.show_button))
        self.show_button.bind('<Leave>', lambda e: self.on_leave(self.show_button))
    
    def animate_text(self):
        # 先执行原有的空格动画
        #new_text_black=""
        for i in range(15):
            #new_text_black = new_text_black+" "
            
            #self.label2.configure(text=new_text_black+"腔")
            new_font = font.Font(family="Courier New", size=32 + i * 4, weight="bold")
            self.label2.configure(font=new_font)
            
            self.root.update()
            time.sleep(0.1)
        
        self.label2.configure(fg="yellow")
        
        # 将label2替换成图片（图片内容为images/hq.png）
        self.animate_label2_step("hq.png")
        time.sleep(0.4)
        
        self.animate_label2_step("hq2.png")
        time.sleep(0.4)
        
        self.animate_label2_step("hq3.png")
        time.sleep(0.4)
        
        self.animate_label2_step("hq4.png")
        time.sleep(0.4)

        self.animate_label2_step("hq5.png")
        time.sleep(0.4)

        self.animate_label2_step("hq6.png")
        time.sleep(0.4)
        self.animate_label2_step("hq7.png")
        time.sleep(0.4)
        self.animate_label2_step("hq8.png")
        time.sleep(0.4)
        self.animate_label2_step("hq9.png")
        time.sleep(0.4)
        
        # 然后变化为新的文本
        self.show_button.configure(text="已成功开黄腔")
        
        
        self.root.update()
        time.sleep(0.1)
    def animate_label2_image_path(self,imageName):
        # 获取脚本所在目录的绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建图片的完整路径
        image_path = os.path.join(script_dir, "images", imageName)
        return image_path


    def animate_label2_step(self,imageName):
        image_path = self.animate_label2_image_path(imageName)
        # 将label2替换成图片
        self.hq_image = tk.PhotoImage(file=image_path)
        self.label2.configure(image=self.hq_image)
        self.label2.image = self.hq_image
        self.label2.configure(text="")
        self.root.update()
    

    def animate_button_click(self, button):
        """按钮点击动画效果"""
        original_bg = button.cget('bg')
        original_fg = button.cget('fg')
        
        # 检查按钮文本，如果是"我不开黄腔了"，则先恢复label2样式
        if button.cget('text') == "我不开黄腔了":
            self.label2.configure(font=self.title_font, fg="#00ff00")
            self.show_button.configure(text="点击开黄腔")
            self.root.update()

        else:
            # 缩放动画
            def scale_animation(scale=1.0, step=0.1):
                if scale <= 0.8:
                    scale = 0.8
                    button.configure(bg='#00ff00', fg='#000000')
                    self.root.update()
                    time.sleep(0.1)
                    button.configure(bg=original_bg, fg=original_fg)
                    # 在按钮动画完成后开始文本动画
                    self.animate_text()
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

if __name__ == "__main__":
    root = tk.Tk()
    app = OpenYellowJoke(root)
    root.mainloop() 
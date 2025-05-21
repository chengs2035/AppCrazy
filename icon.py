from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    # 创建不同尺寸的图标
    sizes = [16, 32, 48, 64, 128, 256]
    icons = []
    
    for size in sizes:
        # 创建新图像
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 计算字体大小
        font_size = int(size * 0.6)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # 绘制背景圆
        circle_radius = int(size * 0.45)
        circle_center = (size // 2, size // 2)
        draw.ellipse(
            [
                circle_center[0] - circle_radius,
                circle_center[1] - circle_radius,
                circle_center[0] + circle_radius,
                circle_center[1] + circle_radius
            ],
            fill=(0, 255, 157, 255)  # 霓虹绿色
        )
        
        # 绘制文字
        text = "IQ"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_position = (
            (size - text_width) // 2,
            (size - text_height) // 2
        )
        
        # 绘制文字阴影
        shadow_offset = int(size * 0.02)
        draw.text(
            (text_position[0] + shadow_offset, text_position[1] + shadow_offset),
            text,
            font=font,
            fill=(0, 100, 60, 255)  # 深绿色阴影
        )
        
        # 绘制主文字
        draw.text(
            text_position,
            text,
            font=font,
            fill=(255, 255, 255, 255)  # 白色文字
        )
        
        # 添加发光效果
        glow_radius = int(size * 0.1)
        for i in range(glow_radius):
            alpha = int(255 * (1 - i / glow_radius))
            draw.ellipse(
                [
                    circle_center[0] - circle_radius - i,
                    circle_center[1] - circle_radius - i,
                    circle_center[0] + circle_radius + i,
                    circle_center[1] + circle_radius + i
                ],
                outline=(0, 255, 157, alpha)
            )
        
        icons.append(img)
    
    # 保存图标
    if not os.path.exists('icons'):
        os.makedirs('icons')
    
    # 保存为ICO文件
    icons[0].save(
        'icons/app_icon.ico',
        format='ICO',
        sizes=[(size, size) for size in sizes],
        append_images=icons[1:]
    )
    
    # 保存为PNG文件（用于其他用途）
    icons[-1].save('icons/app_icon.png')

if __name__ == "__main__":
    create_app_icon() 
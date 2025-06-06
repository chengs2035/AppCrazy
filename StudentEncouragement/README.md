# 考生加油站

这是一个为考生加油打气的程序，通过显示大量鼓励性的窗口来为考生加油。

## 功能特点

- 显示大量鼓励性的窗口
- 窗口均匀分布在整个屏幕上
- 使用温暖的颜色组合
- 自动关闭功能
- 进度显示

## 目录结构

```
StudentEncouragement/
├── src/
│   └── student_encouragement.py  # 主程序
├── resources/
│   └── encouragements.txt        # 鼓励语文件
└── README.md                     # 说明文档
```

## 使用方法

1. 确保已安装Python 3.x
2. 运行主程序：
   ```bash
   python src/student_encouragement.py
   ```
3. 点击"点击加油！"按钮开始显示鼓励窗口

## 自定义设置

- 修改 `encouragements.txt` 文件可以添加或修改鼓励语
- 在 `student_encouragement.py` 中可以调整以下参数：
  - `total_windows`：要显示的窗口总数
  - `grid_size`：网格大小
  - 窗口显示时间
  - 颜色组合等

## 注意事项

- 程序会占用一定的系统资源
- 建议在运行程序时关闭其他占用内存的应用程序
- 如果系统性能不足，可以适当减少窗口数量 
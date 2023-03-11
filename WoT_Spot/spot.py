import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


# 设置图像透明度方法
def addTransparency(image, factor):
    img_convert = image.convert('RGBA')
    blender = Image.new('RGBA', img_convert.size, (255, 255, 255, 0))
    img_blend = Image.blend(blender, img_convert, factor)
    return img_blend


# 判断植被列表当前所选
def switch_plant(number):
    if number == 0:
        return 0
    elif number == 1:
        return 25
    elif number == 2:
        return 50
    elif number == 3:
        return 75
    elif number == 4:
        return 80


# 判断装备列表当前所选
def switch_equip(number):
    if number == 0:
        return 1, 1
    elif number == 1:
        return 0.9, 0.85
    elif number == 2:
        return 0.875, 0.8


# 主要计算逻辑
def calculateFunc():
    print("Calculation button clicked.")

    try:
        global resultString

        plant_val = switch_plant(plant.current())
        m1_val, p1_val = switch_equip(sight_1.current())
        m2_val, p2_val = switch_equip(sight_2.current())

        v1 = float(view_1_val.get())
        v2 = float(view_2_val.get())
        s1 = float(station_camo_1_val.get())
        s2 = float(station_camo_2_val.get())
        m1 = float(moving_camo_1_val.get())
        m2 = float(moving_camo_2_val.get())
        f1 = float(fire_camo_1_val.get())
        f2 = float(fire_camo_2_val.get())

        result_strA1 = v1 - (v1 - 50) * (s2 + plant_val * p1_val) / 100
        result_strA2 = v1 - (v1 - 50) * (m2 * m1_val + plant_val * p1_val) / 100
        result_strA3 = v1 - (v1 - 50) * (f2 + plant_val * p1_val) / 100
        result_strB1 = v2 - (v2 - 50) * (s1 + plant_val * p2_val) / 100
        result_strB2 = v2 - (v2 - 50) * (m1 * m2_val + plant_val * p2_val) / 100
        result_strB3 = v2 - (v2 - 50) * (f1 + plant_val * p2_val) / 100

        result_strA1 = 445 if result_strA1 >= 445 else 50 if result_strA1 <= 50 else result_strA1
        result_strA2 = 445 if result_strA2 >= 445 else 50 if result_strA2 <= 50 else result_strA2
        result_strA3 = 445 if result_strA3 >= 445 else 50 if result_strA3 <= 50 else result_strA3
        result_strB1 = 445 if result_strB1 >= 445 else 50 if result_strB1 <= 50 else result_strB1
        result_strB2 = 445 if result_strB2 >= 445 else 50 if result_strB2 <= 50 else result_strB2
        result_strB3 = 445 if result_strB3 >= 445 else 50 if result_strB3 <= 50 else result_strB3

        resultString = "己方坦克点亮敌方：静止 {}米，移动 {}米，开火 {}米\n" \
                       "敌方坦克点亮己方：静止 {}米，移动 {}米，开火 {}米" \
            .format(int(result_strA1), int(result_strA2), int(result_strA3),
                    int(result_strB1), int(result_strB2), int(result_strB3))

    except ValueError:
        resultString = '输入数据错误！'

    canvas.itemconfig(result_text, fill='black', text=resultString)


def clearFunc():
    print("Clear button clicked.")

    view_1_val.set('')
    view_2_val.set('')
    station_camo_1_val.set('')
    station_camo_2_val.set('')
    moving_camo_1_val.set('')
    moving_camo_2_val.set('')
    fire_camo_1_val.set('')
    fire_camo_2_val.set('')


# ----------#
# 全局变量  #
# ----------#
global_width = 960
global_height = 640
resultString = ''

# 生成一个主窗口
# 这里面可以作为消息循环，添加窗口功能
window = tk.Tk()

window.title('Spot Distance Calculator')

# 创建画布
canvas = tk.Canvas(window,
                   width=global_width,
                   height=global_height,
                   bd=0,
                   highlightthickness=0)

img = Image.open('background.png')

# 图像大小重置
img_resize = img.resize((global_width, global_height), Image.LANCZOS)

# 设置图像透明度
img_trans = addTransparency(img_resize, factor=0.5)

# 创建图片对象
image_file = ImageTk.PhotoImage(img_trans)

# 将图片放置在画布上
canvas.create_image(global_width / 2, global_height / 2, image=image_file)

# 放置画布
canvas.pack()

# 画面标题
canvas.create_text((480, 30),
                   text="坦克点亮距离计算器",
                   font=('微软雅黑 Bold', 24),
                   fill='indigo')

# 提示信息
canvas.create_text((480, 70),
                   text="输入双方坦克的视野和隐蔽，选择配件与植被状况，再点击计算。结果展示在屏幕下方",
                   font=('微软雅黑', 12),
                   fill='navy')

# ---------------#
#  己方坦克数据  #
# ---------------#
canvas.create_text((260, 120),
                   text="己方坦克",
                   font=('微软雅黑 Bold', 18),
                   fill='darkgreen')

# 己方坦克观察范围
canvas.create_text((200, 160),
                   text="观察范围（米）：",
                   font=('微软雅黑 Bold', 14),
                   fill='black')

# 己方坦克观察范围输入框
view_1_val = tk.StringVar()
view_1 = tk.Entry(window,
                  insertbackground='grey',
                  highlightthickness=1,
                  font=('微软雅黑', 14),
                  textvariable=view_1_val)
view_1.pack()
canvas.create_window(360, 160, width=180, height=30, window=view_1)

# 己方坦克静止隐蔽
canvas.create_text((200, 200),
                   text="静止隐蔽（%）：",
                   font=('微软雅黑 Bold', 14),
                   fill='black')

# 己方坦克静止隐蔽输入框
station_camo_1_val = tk.StringVar()
station_camo_1 = tk.Entry(window,
                          insertbackground='grey',
                          highlightthickness=1,
                          font=('微软雅黑', 14),
                          textvariable=station_camo_1_val)
station_camo_1.pack()
canvas.create_window(360, 200, width=180, height=30, window=station_camo_1)

# 己方坦克移动隐蔽
canvas.create_text((200, 240),
                   text="移动隐蔽（%）：",
                   font=('微软雅黑 Bold', 14),
                   fill='black')

# 己方坦克移动隐蔽输入框
moving_camo_1_val = tk.StringVar()
moving_camo_1 = tk.Entry(window,
                         insertbackground='grey',
                         highlightthickness=1,
                         font=('微软雅黑', 14),
                         textvariable=moving_camo_1_val)
moving_camo_1.pack()
canvas.create_window(360, 240, width=180, height=30, window=moving_camo_1)

# 己方坦克开火隐蔽
canvas.create_text((200, 280),
                   text="开火隐蔽（%）：",
                   font=('微软雅黑 Bold', 14),
                   fill='black')

# 己方坦克开火隐蔽输入框
fire_camo_1_val = tk.StringVar()
fire_camo_1 = tk.Entry(window,
                       insertbackground='grey',
                       highlightthickness=1,
                       font=('微软雅黑', 14),
                       textvariable=fire_camo_1_val)
fire_camo_1.pack()
canvas.create_window(360, 280, width=180, height=30, window=fire_camo_1)

# 己方坦克移动隐蔽
canvas.create_text((190, 320),
                   text="车长观瞄系统配件：",
                   font=('微软雅黑 Bold', 14),
                   fill='black')

sight_1 = ttk.Combobox(window,
                       values=["不装配件",
                               "普通装（-10%移动/-15%草后）",
                               "加成装（-12.5%移动/-20%草后）"],
                       state="readonly",
                       font=('微软雅黑', 12))
sight_1.current(0)
canvas.create_window(360, 320, width=180, window=sight_1)

# ---------------#
#  敌方坦克数据  #
# ---------------#
canvas.create_text((680, 120),
                   text="敌方坦克",
                   font=('微软雅黑 Bold', 18),
                   fill='darkred')

# 敌方坦克观察范围
canvas.create_text((600, 160),
                   text="观察范围（米）：",
                   font=('微软雅黑 Bold', 14),
                   fill='black')

# 敌方坦克观察范围输入框
view_2_val = tk.StringVar()
view_2 = tk.Entry(window,
                  insertbackground='grey',
                  highlightthickness=1,
                  font=('微软雅黑', 14),
                  textvariable=view_2_val)
view_2.pack()
canvas.create_window(760, 160, width=180, height=30, window=view_2)

# 敌方坦克静止隐蔽
canvas.create_text((600, 200),
                   text="静止隐蔽（%）：",
                   font=('微软雅黑 Bold', 14),
                   fill='black')

# 敌方坦克静止隐蔽输入框
station_camo_2_val = tk.StringVar()
station_camo_2 = tk.Entry(window,
                          insertbackground='grey',
                          highlightthickness=1,
                          font=('微软雅黑', 14),
                          textvariable=station_camo_2_val)
station_camo_2.pack()
canvas.create_window(760, 200, width=180, height=30, window=station_camo_2)

# 敌方坦克移动隐蔽
canvas.create_text((600, 240),
                   text="移动隐蔽（%）：",
                   font=('微软雅黑 Bold', 14),
                   fill='black')

# 敌方坦克移动隐蔽输入框
moving_camo_2_val = tk.StringVar()
moving_camo_2 = tk.Entry(window,
                         insertbackground='grey',
                         highlightthickness=1,
                         font=('微软雅黑', 14),
                         textvariable=moving_camo_2_val)
moving_camo_2.pack()
canvas.create_window(760, 240, width=180, height=30, window=moving_camo_2)

# 敌方坦克开火隐蔽
canvas.create_text((600, 280),
                   text="开火隐蔽（%）：",
                   font=('微软雅黑 Bold', 14),
                   fill='black')

# 敌方坦克开火隐蔽输入框
fire_camo_2_val = tk.StringVar()
fire_camo_2 = tk.Entry(window,
                       insertbackground='grey',
                       highlightthickness=1,
                       font=('微软雅黑', 14),
                       textvariable=fire_camo_2_val)
fire_camo_2.pack()
canvas.create_window(760, 280, width=180, height=30, window=fire_camo_2)

# 敌方坦克移动隐蔽
canvas.create_text((590, 320),
                   text="车长观瞄系统配件：",
                   font=('微软雅黑 Bold', 14),
                   fill='black')

sight_2 = ttk.Combobox(window,
                       values=["不装配件",
                               "普通装（-10%移动/-15%草后）",
                               "加成装（-12.5%移动/-20%草后）"],
                       state="readonly",
                       font=('微软雅黑', 12))
sight_2.current(0)
canvas.create_window(760, 320, width=180, window=sight_2)

# 双方坦克草丛状况
canvas.create_text((400, 380),
                   text="双方坦克之间植被状况：",
                   font=('微软雅黑 Bold', 14),
                   fill='black')

# 双方坦克草丛状况下拉选择栏
plant = ttk.Combobox(window,
                     values=["无草丛（+0%）",
                             "单层薄草/灌木（+25%）",
                             "单层厚草/树叶（+50%）",
                             "薄草/灌木+厚草/树叶（+75%）",
                             "双草（+80%）"],
                     state="readonly",
                     font=('微软雅黑', 12))
plant.current(0)
canvas.create_window(600, 380, width=180, window=plant)

# 添加计算按钮
calculate = tk.Button(window,
                      text="计算",
                      font=('微软雅黑 Bold', 16),
                      command=calculateFunc)
calculate.pack()
canvas.create_window(560, 440, width=120, height=40, window=calculate)

# 添加重置按钮
clear = tk.Button(window,
                  text="重置",
                  font=('微软雅黑 Bold', 16),
                  command=clearFunc)
clear.pack()
canvas.create_window(400, 440, width=120, height=40, window=clear)

# 显示输出结果
result_text = canvas.create_text((global_width / 2, 540),
                                 text='',
                                 font=('微软雅黑 Bold', 18),
                                 fill='black')

# 进入消息循环
window.mainloop()

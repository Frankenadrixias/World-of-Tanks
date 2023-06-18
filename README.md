
# World-of-Tanks

一些关于坦克世界的程序和代码 \
Some programs and codes about the game World of Tanks

## 坦克世界缩圈扩圈计算器

文件夹 WoT_Fire

### 介绍

坦克世界缩圈扩圈计算器 \
实现方式：python + matplotlib + pyqt5 \
总代码量约1300行

### 使用说明

1. 下载 WoT_Fire/dist 目录下的 “wot缩圈扩圈计算器.exe” 文件
2. 如果您的电脑对 exe 文件敏感，直接下载会触发杀毒软件保护机制，那么请下载 WoT_Fire 目录下的 “wot缩圈扩圈计算器.zip” 文件，将其解压
3. 打开 “wot缩圈扩圈计算器.exe” 文件运行程序

### 更新内容

#### 2023.03.11 v1.0

1. 上线了坦克世界缩圈计算器

#### 2023.06.18 v2.0

1. 实现了两套配件的对比：在右侧配置数据中选择第一
2. 本ReadMe文档的注意事项写入了帮助信息

### 注意事项

1. 基础属性中扩圈系数来源于 tanks.gg；配置数据中请注意配件的等级选择；
2. 具体结论需要综合绘图结果和数据信息展示的具体数值；
3. 由于如果将两个配件的对比结果均在图中展示，那么差异会很小，很难分辨，最终采用文本方式；
4. 该程序目前主要是为了对比配件的效果，暂时没考虑战地改装、成员技能的影响，如果需要在此基础上计算，建议在tanks.gg上配置好后输入等效数据；
5. 目前程序是1.0版本，很多功能还没有实现（比如打开、保存：计划是将这些车辆的属性和数据保存为excel表格，如果想查看之前的结果可以直接读取数据）；
6. 帮助信息需要等大家的测试结果，看看哪里有不懂的或容易误解的地方，我好在之后的版本中写在上面。

## 坦克世界点亮距离计算器

文件夹 WoT_Spot

### 介绍

坦克世界点亮距离计算器 \
实现方式：python + tkinter \
总代码量约350行

### 使用说明

1. 下载 WoT_Spot 目录下的 “WOT_spot.zip” 文件
2. 将压缩文件解压到同一文件夹
3. 打开 “WOT_spot.exe” 文件运行程序
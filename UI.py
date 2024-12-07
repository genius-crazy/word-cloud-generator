# -*- coding: UTF-8 -*-
# 中文注释
import wordcloud
import jieba as jb
import threading as td
import numpy as np
from PIL import Image as ig
import datetime
import tkinter as tk
from tkinter import filedialog as fd
from time import sleep
# 导入库

# 载入背景图片
China = np.array(ig.open(r'map\China.png'))
guangxi = np.array(ig.open(r'map\guangxi.png'))
star = np.array(ig.open(r'map\star.png'))
cloud = np.array(ig.open(r'map\cloud.png'))
princess = np.array(ig.open(r'map\princess.png'))


# 创建一个窗口对象
root = tk.Tk()

###调参###
# UI参数
height = root.winfo_screenmmheight()  # 获取屏幕高度
width = root.winfo_screenwidth()  # 获取屏幕宽度
root.geometry('800x600+%d+%d' % ((width-800)/2, (height-600)/2))
root.title('词云生成器')
root.geometry('800x600+100+100')  # 宽度x高度+出现在X的位置上+出现在Y的位置上
root['background'] = 'white'
root.attributes('-alpha', 0.93)  # 透明度
# 词云参数
stopwords = ['的', '和', '是', '你', '我', '他', '她', '它']  # 屏蔽词
background_color = 'White'
mask = None
repeat = True
stopwords = stopwords
font_path = 'fonts/msyh.ttf'
height = 600
width = 800
colormap = None

text1 = (
    '富强 民主 文明 和谐 自由 平等 公正 法治 爱国 敬业 诚信 友善')

with open("二十大报告.txt") as reader:
    text2 = reader.read()

# 创建一个可变变量
time_now = tk.StringVar()
time_now.set(str(datetime.datetime.now()))
choice = tk.IntVar()

# 单选框
rbn1 = tk.Radiobutton(
    root, text='China', variable=choice, value=1)
rbn2 = tk.Radiobutton(
    root, text='guangxi', variable=choice, value=2)

# 显示时间
tlb_time = tk.Label(
    root, textvariable=time_now,
    fg='blue',
    bg='yellow',
    font=('微软雅黑', 26)
)
tlb_time.pack()

# 显示文字
tlb_1 = tk.Label(
    root, text='请输入文本',
    fg='blue',
    bg='yellow',
    font=('微软雅黑', 26)
)
tlb_1.pack()





global cue
cue = ""

a = '.'
tlb_cue = tk.Label(root, textvariable=cue,bg='white')
tlb_cue.pack()
print(cue)








# 背景图片选择模块
'''尝试'''


def f():
    p = fd.asksaveasfilename(title='保存词云图',
                            initialfile='词云图', filetypes=[('png图片', '.png'), ('jpg图片', '.jpg'), ('jpeg图片', '.jpeg')])
    print(p)


def backimage():
    a = choice.get()
    mask = None
    if a == 1:
        mask = China
    elif a == 2:
        mask = guangxi
    elif a == 3:
        mask = star
    elif a == 4:
        mask = cloud
    elif a == 5:
        mask = princess
    return mask


# 按钮组件
btn1 = tk.Button(root, text='确认')
btn2 = tk.Button(root, text='打开窗口')
btn2.pack()
btn2 = tk.Button(root, text='开始生成词云图')


'''_____函数模块_____'''

def win_set():
    windows_set=tk.Toplevel(root)
    windows_set.geometry('300x400')
    windows_set.title('自定义词云参数')
    
    lb_background = tk.Label(windows_set, text="请选择词云轮廓(默认为矩形)", bg='white')
    lb_backcolor = tk.Label(windows_set, text="请选择背景色(默认为黑色)", bg='white')
    lb_repeat = tk.Label(windows_set, text="词汇是否重复(默认为重复)", bg='white')
    # 单选框
    choice_bg = None  # 背景图
    choice_bg = tk.IntVar()
    rbn_bg1 = tk.Radiobutton(
        windows_set, text='中国版图', variable=choice_bg, value=1, bg='white')
    rbn_bg2 = tk.Radiobutton(
        windows_set, text='广西版图', variable=choice_bg, value=2, bg='white')
    rbn_bg3 = tk.Radiobutton(
        windows_set, text='五角星', variable=choice_bg, value=3, bg='white')
    rbn_bg4 = tk.Radiobutton(
        windows_set, text='云朵', variable=choice_bg, value=4, bg='white')
    rbn_bg5 = tk.Radiobutton(
        windows_set, text='公主', variable=choice_bg, value=5, bg='white')
    rbn_bg6 = tk.Radiobutton(
        windows_set, text='自定义一张png图片为背景', variable=choice_bg, value=6, bg='white')

    choice_bc = None  # 背景色
    choice_bc = tk.IntVar()
    rbn_bc1 = tk.Radiobutton(
        windows_set, text='白色', variable=choice_bc, value=1, bg='white')
    rbn_bc2 = tk.Radiobutton(
        windows_set, text='黑色', variable=choice_bc, value=2, bg='white')

    choice_rp = None  # 重复词
    choice_rp = tk.IntVar()
    rbn_rp1 = tk.Radiobutton(
        windows_set, text='重复', variable=choice_rp, value=1, bg='white')
    rbn_rp2 = tk.Radiobutton(
        windows_set, text='不重复', variable=choice_rp, value=2, bg='white')


    lb_background.pack()
    rbn_bg1.pack()
    rbn_bg2.pack()
    rbn_bg3.pack()
    rbn_bg4.pack()
    rbn_bg5.pack()
    rbn_bg6.pack()

    lb_backcolor.pack()
    rbn_bc1.pack()
    rbn_bc2.pack()

    lb_repeat.pack()
    rbn_rp1.pack()
    rbn_rp2.pack()
        






# 词云模块
wc = wordcloud.WordCloud(
    background_color=background_color, mask=mask, repeat=repeat, stopwords=stopwords, font_path=font_path, height=height, width=width, colormap=colormap)

# 分词模块


def cutwords(text):
    result = ' '.join(jb.lcut(text.strip()))
    return result
# 词云生成模块


def process(text):
    wc.generate(text)
# 展示模块


def show():
    print('词云图为')
    wc.to_image().show()
# 保存模块


def save():
    save = int(input('是否保存？(1/0)\n'))
    if save == 1:
        name = str(input('请输入文件名'))
        wc.to_file(name+'.png')
# UI模块


def ui():
    root.mainloop()
    # 进入事件循环


# 分词
result = cutwords(text2)
# 事件绑定
rbn1.pack()
rbn2.pack()
btn1.pack()
btn2.pack()
btn1.config(command=f)
btn2.config(command=lambda: process(result))

# 主进程
if __name__ == "__main__":
    # 定义进程
    thread_ui = td.Thread(target=ui)
    thread_2 = td.Thread(target=show)
    thread_3 = td.Thread(target=save)
    # 运行
    thread_ui.start()
    # thread_2.start()
    # thread_3.start()
# 更新时间
new = '请稍后，词云正在生成中\n'
while True:
    
    
    time_now.set(new)
    tlb_time.update()
    sleep(0.5)
    new += a
    time_now.set(new)
    tlb_time.update()
    sleep(0.5)
    
while True:

    new = '请稍后，词云正在生成中/n'
    cue.set(new)
    tlb_cue.update()
    sleep(0.5)
    new += a
    cue.set(new)
    tlb_cue.update()
    sleep(0.5)
print(cue)

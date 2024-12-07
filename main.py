# -*- coding: UTF-8 -*-
# 中文注释

from imageio import imread as ig
from jieba import lcut
from wordcloud import WordCloud
import tkinter as tk
from tkinter import filedialog as fd
from os import path
from chardet import detect
from tkinter import messagebox
from datetime import datetime
from time import sleep
from threading import Thread
from docx import Document
from PIL import Image, ImageTk
# 导入库



# 进程退出标志
flag_home = True

# 载入背景图片
China = ig(r'conf\image\China.png')
guangxi = ig(r'conf\image\guangxi.png')
star = ig(r'conf\image\star.png')
cloud = ig(r'conf\image\cloud.png')
princess = ig(r'conf\image\princess.png')
one = ig(r'conf\image\frist.png')



'''词云参数'''
wc = WordCloud()
with open(r'conf\wordcloud_config.ini', 'w') as writer:
    # 清除上一次用户的词云配置
    writer.close()
with open(r'conf\stopwords.ini') as reader:
    # 屏蔽词列表
    file = reader.readlines()
    stopwords = []
    for s in file:
        if '\n' in s:
            s = s[:-1]
        stopwords.append(s)

background_color = 'white'
mask = None
repeat = True
stopwords = stopwords
font_path = 'conf/fonts/msyh.ttf'
height = 300
width = 400
colormap = None  # 词云主题色
max_words = 400
relative_scaling = 1.0  # 词频和字体大小的关联性

'''词云参数'''


''''UI参数'''''
root = tk.Tk()
root.title('尹豪牌词云生成器')
root.geometry('800x600+100+100')  # 宽度x高度+出现在X的位置上+出现在Y的位置上
root['background'] = 'white'
root.attributes('-alpha', 0.93)  # 透明度
root.iconbitmap(r'conf\image\logo.ico')  # 设置图标
''''UI参数'''''

# 主页画布
home = tk.Canvas(root, height=160, width=800,bg='white')
home_1 = tk.PhotoImage(file=r'conf\image\home_1.png')
home_2 = tk.PhotoImage(file=r'conf\image\home_2.png')
po1 = tk.PhotoImage(file=r'conf\image\11.png')
po2 = tk.PhotoImage(file=r'conf\image\2.png')
po3 = tk.PhotoImage(file=r'conf\image\3.png')
po4 = tk.PhotoImage(file=r'conf\image\4.png')
po5 = tk.PhotoImage(file=r'conf\image\5.png')
po6 = tk.PhotoImage(file=r'conf\image\6.png')
# 标签
signal = tk.StringVar()
signal.set('')
lb_cue = tk.Label(root, textvariable=signal, fg='red', bg='white',font=('conf/fonts/simkai.ttf',12))

# 文本框
t_text = tk.Text(root, width=80, height=19)
t_text.insert(tk.INSERT, "\n")

# 按钮
btn_set = tk.Button(root, text='自定义词云参数', width=180, height=60,
                    bg='Silver', activebackground='PeachPuff', image=po2)  # activebackground是按下时的颜色
btn_file = tk.Button(root, text='选择文本文件', width=180, height=60,
                     bg='Silver', activebackground='PeachPuff', image=po1)
btn_wc = tk.Button(root, text='生成词云图', width=180, height=60,
                   bg='Silver', activebackground='PeachPuff', image=po3)
btn_recolor = tk.Button(root, text='重新上色', width=180, height=60,
                        bg='Silver', activebackground='PeachPuff', image=po4)
btn_save = tk.Button(root, text='保存词云图', width=180, height=60,
                     bg='Silver', activebackground='PeachPuff', image=po5)
btn_quit = tk.Button(root, text='退出程序', width=180, height=60,
                     bg='Silver', activebackground='PeachPuff', image=po6)
''''UI参数'''''


'''函数'''


def label_clear():
    signal.set('')
    lb_cue.update()


def win_set():

    signal.set('正在自定义词云参数...')
    lb_cue.update()

    windows_set = tk.Toplevel(root)
    windows_set.geometry('600x600')
    windows_set.title('自定义词云参数')
    windows_set.iconbitmap(r'conf\image\logo.ico')

    lb_background = tk.Label(
        windows_set, text="1、请选择词云轮廓(默认为矩形)", bg='PeachPuff')
    lb_backcolor = tk.Label(
        windows_set, text="2、请选择背景色(默认为白色)", bg='PeachPuff')
    lb_repeat = tk.Label(windows_set, text="3、词汇是否重复(默认为重复)", bg='PeachPuff')
    lb_font = tk.Label(windows_set, text="4、请选择字体(默认为微软雅黑)", bg='PeachPuff')
    lb_rpmax = tk.Label(
        windows_set, text="5、请输入词云最大词汇数(默认为400)", bg='PeachPuff')

    # 单选框
    choice_bg = tk.IntVar()  # 背景图
    choice_bg.set(0)
    rbn_bg0 = tk.Radiobutton(
        windows_set, text='矩形', variable=choice_bg, value=0, bg='white')
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

    choice_bc = tk.IntVar()  # 背景色
    choice_bc.set(0)
    rbn_bc1 = tk.Radiobutton(
        windows_set, text='白色', variable=choice_bc, value=0, bg='white')
    rbn_bc2 = tk.Radiobutton(
        windows_set, text='黑色', variable=choice_bc, value=1, bg='white')

    choice_rp = tk.IntVar()  # 重复词
    choice_rp.set(0)
    rbn_rp1 = tk.Radiobutton(
        windows_set, text='重复', variable=choice_rp, value=0, bg='white')
    rbn_rp2 = tk.Radiobutton(
        windows_set, text='不重复', variable=choice_rp, value=1, bg='white')

    choice_font = tk.IntVar()  # 字体
    choice_font.set(0)
    rbn_font0 = tk.Radiobutton(
        windows_set, text='微软雅黑', variable=choice_font, value=0, bg='white')
    rbn_font1 = tk.Radiobutton(
        windows_set, text='宋体', variable=choice_font, value=1, bg='white')
    rbn_font2 = tk.Radiobutton(
        windows_set, text='仿宋', variable=choice_font, value=2, bg='white')
    rbn_font3 = tk.Radiobutton(
        windows_set, text='楷体', variable=choice_font, value=3, bg='white')
    rbn_font4 = tk.Radiobutton(
        windows_set, text='自定义字体(选择字体文件)', variable=choice_font, value=4, bg='white')

    # 单行文本框
    text_max = tk.Entry(windows_set, bg='white')

    # 确认按钮
    btn_sure = tk.Button(windows_set, text='确认', width=12, height=2)

    # 新建列表以储存用户词云配置及其项
    con_list = [choice_bg, choice_bc, choice_rp, choice_font]  # 词云配置项
    with open(r'conf\wordcloud_config.ini') as config:
        config_list = config.readlines()  # 词云配置

    # 读取用户词云配置
    cons = []
    for c in config_list:
        c.strip()
        c = int(c)
        cons.append(c)

    if cons != []:
        # 设定配置为用户未退出程序前的上一次配置
        for a, b in zip(con_list, cons):
            a.set(b)

    # 函数模块
    def backimage():
        # 背景图片选择模块
        a = choice_bg.get()
        global mask
        if a == 0:
            mask = None
        elif a == 1:
            mask = China
        elif a == 2:
            mask = guangxi
        elif a == 3:
            mask = star
        elif a == 4:
            mask = cloud
        elif a == 5:
            mask = princess
        elif a == 6:
            signal.set('正在自定义背景图片...')
            lb_cue.update()
            p = fd.askopenfilename(
                title='选择png图片', filetypes=[('png图片', '.png')])
            p = path.abspath(p)

            d = path.dirname(p)
            if path.exists(d) == False:
                # 判断文件路径是否存在
                label_clear()
                tk.messagebox.showerror(title='错误', message='文件路径错误,请检查后重新选择')

            try:
                mask = ig(p)
                label_clear()
            except:
                label_clear()
                tk.messagebox.showerror(title='错误', message='图片不存在,请检查后重新选择')

    def backcolor():
        # 背景色选择模块
        a = choice_bc.get()
        global background_color
        if a == 0:
            background_color = 'white'
        elif a == 1:
            background_color = 'black'

    def repeat():
        # 重复词模块
        a = choice_rp.get()
        global repeat
        if a == 0:
            repeat = True
        elif a == 1:
            repeat = False

    def font():
        # 字体选择模块
        a = choice_font.get()
        global font_path
        if a == 0:
            font_path = 'conf\fonts\msyh.ttf'
        elif a == 1:
            font_path = 'conf\fonts\simsun.ttc'
        elif a == 2:
            font_path = 'conf\fonts\simfang.ttf'
        elif a == 3:
            font_path = 'conf\fonts\simkai.ttf'

        elif a == 4:
            signal.set('正在自定义字体...')
            lb_cue.update()
            p = fd.askopenfilename(
                title='选择字体文件', filetypes=[('ttf字体文件', '.ttf'), ('ttc字体文件', '.ttc')])
            p = path.abspath(p)

            d = path.dirname(p)
            if path.exists(d) == False:
                # 判断文件路径是否存在
                label_clear()
                tk.messagebox.showerror(title='错误', message='文件路径错误,请检查后重新选择')

            try:
                font_path = p
                label_clear()
            except:
                label_clear()
                tk.messagebox.showerror(title='错误', message='字体不存在,请检查后重新选择')

    def max_words_set(event=''):
        # 回车设定最大词汇量
        try:
            global max_words
            max_words = int(text_max.get())
            text_max.delete(0, tk.END)
        except:
            tk.messagebox.showerror(
                title='识别错误', message='输入的不是数字或不是整数,请检查后重新输入')

    def quit():

        with open(r'conf\wordcloud_config.ini', 'w') as writer:
            # 保存用户配置信息
            for c in con_list:
                con = str(c.get())+'\n'
                writer.write(con)

        # 保存词云最大词汇数
        a = text_max.get()
        if a:
            try:
                global max_words
                max_words = int(text_max.get())
                text_max.delete(0, tk.END)
            except:
                tk.messagebox.showerror(
                    title='识别错误', message='输入的不是数字或不是整数,请检查后重新输入')

        label_clear()
        windows_set.destroy()

    # 事件返回
    lb_background.place(x=5, y=10)
    rbn_bg0.place(x=20, y=40)
    rbn_bg1.place(x=120, y=40)
    rbn_bg2.place(x=220, y=40)
    rbn_bg3.place(x=340, y=40)
    rbn_bg4.place(x=440, y=40)
    rbn_bg5.place(x=20, y=80)
    rbn_bg6.place(x=120, y=80)

    lb_backcolor.place(x=5, y=140)
    rbn_bc1.place(x=20, y=170)
    rbn_bc2.place(x=100, y=170)

    lb_repeat.place(x=280, y=140)
    rbn_rp1.place(x=280, y=170)
    rbn_rp2.place(x=400, y=170)

    lb_font.place(x=5, y=220)
    rbn_font0.place(x=20, y=260)
    rbn_font1.place(x=140, y=260)
    rbn_font2.place(x=230, y=260)
    rbn_font3.place(x=20, y=300)
    rbn_font4.place(x=120, y=300)

    lb_rpmax.place(x=5, y=360)
    text_max.place(x=5, y=400)

    btn_sure.place(x=250, y=460)

    # 事件绑定
    rbn_bg1.config(command=backimage)
    rbn_bg2.config(command=backimage)
    rbn_bg3.config(command=backimage)
    rbn_bg4.config(command=backimage)
    rbn_bg5.config(command=backimage)
    rbn_bg6.config(command=backimage)

    rbn_bc1.config(command=backcolor)
    rbn_bc2.config(command=backcolor)

    rbn_rp2.config(command=repeat)
    rbn_rp1.config(command=repeat)

    rbn_font0.config(command=font)
    rbn_font1.config(command=font)
    rbn_font2.config(command=font)
    rbn_font3.config(command=font)
    rbn_font4.config(command=font)

    text_max.bind('<Return>', max_words_set)

    btn_sure.config(command=quit)


def file():
    signal.set('正在选择文本文件...')
    lb_cue.update()
    p = fd.askopenfilename(title='选择文本文件', filetypes=[('txt文件', '.txt'),('docx文档','.docx')])
    p = path.abspath(p)
    filename=path.basename(p)
    
    extendname=(path.splitext(filename))[1]
    
    d = path.dirname(p)
    if path.exists(d) == False:
        # 判断文件路径是否存在
        label_clear()
        tk.messagebox.showerror(title='错误', message='文件路径错误,请检查后重新选择')
    if extendname=='.txt':
        #读取txt文件
        try:
            with open(p, 'rb') as f:
                # 获取文件的编码类型
                coding = str(detect(f.read())['encoding'])
            with open(p, encoding=coding) as reader:
                # 读取文本文档
                txt = reader.read()
                t_text.insert(0.0, txt)
            tk.messagebox.showinfo(title='读取成功', message='成功读取%s'%filename)
            label_clear()
        except:
            label_clear()
            tk.messagebox.showerror(title='读取错误', message='文件编码错误或文件不存在,请检查后重新选择')
    elif extendname == '.docx':
        #读取docx文件
        document = Document(p)
        try:
            #获取所有段落
            all_paragraphs = document.paragraphs
            paragraphs = []
            for paragraph in all_paragraphs:
                txt = paragraph.text
                paragraphs.append(txt)

            txts = "\n".join(paragraphs)
            t_text.insert(0.0, txts)
            label_clear()
        except:
            label_clear()
            tk.messagebox.showerror(
                title='读取错误', message='文件编码错误或文件不存在,请检查后重新选择')

def create():
    signal.set('正在生成词云图...')
    lb_cue.update()

    # 获取文本框文字
    txt = t_text.get(0.0, tk.END)
    txtlist = lcut(txt)
    txt = " ".join(txtlist)

    # 词云模块
    try:

        global wc
        wc = WordCloud(background_color=background_color, mask=mask, repeat=repeat, stopwords=stopwords,
                       font_path=font_path, height=height, width=width, colormap=colormap, max_words=max_words, relative_scaling=relative_scaling)
        wc.generate(txt)
        wc.to_image().show()
        label_clear()
        a = tk.messagebox.askokcancel(title='生成完毕', message='生成完毕,是否保存?')
        if a:
            save()

    except ValueError:
        label_clear()
        tk.messagebox.showerror(
            title='生成失败', message='无文本输入或该文本为屏蔽词\n请检查后输入文本或更改文本')


def recolor():
    # 重上色模块
    signal.set('正在为词云图重新上色...')
    lb_cue.update()

    try:
        wc.recolor()
        wc.to_image().show()
        label_clear()
        a = tk.messagebox.askokcancel(title='重新上色完毕', message='重新上色完毕,是否保存?')
        if a:
            save()

    except ValueError:
        label_clear()
        tk.messagebox.showerror(title='上色失败', message='请先生成词云图')


def save():
    # 保存模块
    signal.set('正在保存词云图...')
    lb_cue.update()

    now = str(datetime.now())[:-7]  # 获取当前时间
    leng = now.__len__()
    for i in now:
        if i not in [' ', ':']:
            now += i
        else:
            i = '_'
            now += i

    now = now[leng:]

    p = fd.asksaveasfilename(
        title='保存词云图', initialfile='词云图___%s.png' % (now), filetypes=[('png图片', '.png')])
    p = path.abspath(p)

    d = path.dirname(p)
    if path.exists(d) == False:
        # 判断文件路径是否存在
        label_clear()
        tk.messagebox.showerror(title='保存失败', message='文件路径错误,请检查后重新选择')
    try:
        wc.to_file(p)  # 设置保存路径
        label_clear()
        tk.messagebox.showinfo(title='保存完毕', message='保存完毕')

    except ValueError:
        label_clear()
        tk.messagebox.showerror(
            title='保存失败', message='未确认保存或未生成词云图,\n请确认保存或先生成词云图')


def home_picture():
    # 主页背景
    while True:
        home.delete('all')
        image_1 = home.create_image(0, 0, anchor='nw', image=home_1)
        home.update()
        sleep(1)
        if flag_home == False:
            break
        home.delete('all')
        image_2 = home.create_image(0, 0, anchor='nw', image=home_2)
        home.update()
        sleep(1)
        if flag_home == False:
            break


def quit():
    with open(r'conf\wordcloud_config.ini', 'w') as writer:
        # 清除上一次用户的词云配置
        writer.close()
    # 退出程序
    global flag_home  # 退出进程
    flag_home = False
    thread_home.join()
    root.quit()


'''函数'''

#定义进程
thread_home=Thread(target=home_picture)


# 事件返回
home.place(x=10, y=20)  # 改pack为place方式

t_text.place(x=220, y=180)

btn_set.place(x=10, y=350)
btn_file.place(x=10, y=250)
btn_wc.place(x=10, y=450)
btn_recolor.place(x=210, y=450)
btn_save.place(x=410, y=450)
btn_quit.place(x=610, y=450)

lb_cue.place(x=10, y=10)  # 改pack为place方式

# 事件绑定

btn_set.config(command=win_set)
btn_file.config(command=file)
btn_wc.config(command=create)
btn_recolor.config(command=recolor)
btn_save.config(command=save)
btn_quit.config(command=quit)

if __name__=='__main__':
    thread_home.start()


root.mainloop()


"""
    This is the main part of the program
"""

import time
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
import pygame as pg
from pygame import midi
import chorder
from chord_player import play_chord_set

import threading

"""
    Initialization
    初始化
"""
last_pitch = 0  # 键盘演奏数据初始化
# 定义颜色
BG_COLOUR = 'Beige'
STRIPS_COLOUR = 'Tan'
piano = None  # 钢琴图片会一直留在界面上，所以定为全局变量，初始化：

# 初始化控件组
start_win = []
cpg_win = []
cpg_piano = []
cpg_wd_input_boxs1 = []
gcpg_win = []
gcpg_piano = []
gcpg_wd_input_boxs1 = []
help_win = []
generated_blocks = []

# 初始化时值数组
available_duration = ["1/4", "1/3", "1/2", "2/3", "3/4", "1", "5/4", "4/3", "3/2", "5/3", "7/4", "2",
                      "9/4", "7/3", "5/2", "8/3", "11/4", "3", "13/4", "10/3", "7/2", "11/3", "15/4", "4",
                      "17/4", "13/3", "9/2", "14/3", "19/4", "5", "21/4", "16/3", "11/2", "17/3", "23/4", "6",
                      "25/4", "19/3", "13/2", "20/3", "27/4", "7", "29/4", "22/3", "25/2", "23/3", "31/4", "8"]
result = []


# TODO:测试用代码
def print_result():
    print('Model:' + str(result[3]), end='')
    print('   BPS:' + str(result[4]))
    print('\033[0;33;1m-\033[0m' * (1 + len(result[0]) * 7))
    for i in range(3):
        print("\033[0;33;1m|\033[0m", end='')
        for ii in result[i]:
            if len(ii.get()) == 1:
                print("  ", end='')
                if ii == result[i][-1]:
                    print(ii.get(), end='   ')
                    continue
                print(ii.get(), end='\033[0;33;1m   |\033[0m')
            if len(ii.get()) == 2:
                print("  ", end='')
                if ii == result[i][-1]:
                    print(ii.get(), end='  ')
                    continue
                print(ii.get(), end='\033[0;33;1m  |\033[0m')
            if len(ii.get()) == 3:
                print(" ", end='')
                if ii == result[i][-1]:
                    print(ii.get(), end=' ')
                    continue
                print(ii.get(), end='\033[0;33;1m  |\033[0m')
            if len(ii.get()) == 4:
                print(" ", end='')
                if ii == result[i][-1]:
                    print(ii.get(), end='')
                    continue
                print(ii.get(), end='\033[0;33;1m |\033[0m')
        print("\033[0;33;1m|\033[0m")
    print('\033[0;33;1m-\033[0m' * (1 + len(result[0]) * 7))


"""
    Play functions
    播放函数
"""


def play_note(pitch, instrument='Piano'):
    global last_pitch
    player.note_off(last_pitch, 60)
    ticks1 = time.time()
    print(ticks1)
    if instrument == 'Piano':
        player.set_instrument(0)
    player.note_on(pitch + 21, 60)
    last_pitch = pitch + 21
    return last_pitch


"""
    Tkinter's lable functions
    Tkinter的标签函数
"""


def colour_block(belonging, master, position, width=10, height=15):
    blk = tk.Frame(master, bg='white')
    blk.pack(side=position, fill='none', padx=width, pady=height, expand=0)
    belonging.append(blk)
    return blk


def y_blank(belonging, position, height=15):
    blk = tk.Frame(window, bg=BG_COLOUR)
    blk.pack(side=position, fill='y', ipadx=10, ipady=height, expand=0)
    if belonging is not None:
        belonging.append(blk)


def x_blank(belonging, position, width=15):
    blk = tk.Frame(window, bg=BG_COLOUR)
    blk.pack(side=position, fill='y', ipadx=width, ipady=10, expand=0)
    belonging.append(blk)
    if belonging is not None:
        belonging.append(blk)


# cpg某函数特有的空
def cpg_win_left_blank(master, width=10):
    frame_xx = tk.Frame(master, width=width, background=BG_COLOUR)
    frame_xx.pack(fill="y", side='left', expand=True)
    cpg_win.append(frame_xx)


def y_colour_block(belonging, position, colour, height=1):
    blk = tk.Frame(window, bg=colour)
    blk.pack(side=position, fill='y', ipadx=1400, ipady=height, expand=0)
    if belonging is not None:
        belonging.append(blk)


def title(belonging, text="text", font_size=20, wid=35, hei=2):
    title_text = tk.StringVar()  # 定义一个字符串变量
    title_v = tk.Label(
        window,
        textvariable=title_text,  # 标签的文字
        bg=BG_COLOUR,  # 标签背景颜色
        font=('Arial', font_size),  # 字体和字体大小
        width=wid, height=hei)  # 标签长宽
    title_v.pack()  # 固定窗口位置
    if belonging is not None:
        belonging.append(title_v)
    title_text.set(text)


# 定义按钮
def button(belonging, hit_func, text='text', font_size=30):
    b = tk.Button(window, text=text, font=('Arial', font_size), width=10, height=1, command=hit_func)
    b.pack()
    if belonging is not None:
        belonging.append(b)
    return hit_func


def button2(master, belonging, hit_func, text='text', font_size=13):
    b = tk.Button(master, text=text, font=('Arial', font_size), width=0, height=4, command=hit_func)
    b.pack(expand=True)
    belonging.append(b)
    return hit_func


# 定义输入框
def entry_box(master, belonging, entry_bind_func, mouse_wheel_f, position="left", font_size=13, width=5, default='3'):
    f_entry = tk.Entry(master, font=('Arial', font_size), justify="center", width=width)
    belonging.append(f_entry)
    f_entry.pack(side=position, expand=0)
    f_entry.insert(0, default)
    f_entry.bind("<Return>", entry_bind_func)
    f_entry.bind("<Enter>", entry_bind_func)
    f_entry.bind("<Button-1>", entry_bind_func)
    f_entry.bind("<MouseWheel>", mouse_wheel_f)
    return [f_entry, f_entry.get()]


# 定义下拉选择框
def combox(master, belonging, selected_func, values, position='left', width=7, height=5):
    text_var = tk.StringVar()
    _combox = ttk.Combobox(master, textvariable=text_var, font=('Arial', 11), width=width, height=height)
    _combox["values"] = values
    _combox.current(0)  # 默认值
    _combox.bind("<<ComboboxSelected>>", selected_func)  # 绑定事件(下拉列表框被选中时，绑定函数selected_func)
    _combox.bind("<Leave>", selected_func)  # 绑定事件(下拉列表框被选中时，绑定函数selected_func)
    _combox.bind("<Return>", selected_func)  # 绑定事件(下拉列表框被选中时，绑定函数selected_func)
    _combox.pack(side=position, expand=True)
    belonging.append(_combox)
    return _combox.get()


"""
    Running functions
    运行函数
"""


def input_piano(belonging):
    keys_frame = tk.Frame(window, bg=BG_COLOUR)
    keys_frame.pack(side="bottom", fill='y', ipadx=0, ipady=0, expand=0)
    belonging.append(keys_frame)
    w_key_list = [0, 2, 3, 5, 7, 8, 10]

    for i in range(88):
        if i % 12 in w_key_list:
            key = tk.Button(
                keys_frame,
                width=1,
                height=0,
                bd=1,
                highlightcolor="white",
                background="white",
                activebackground="skyblue",
                # 运用lambda函数的特性防止传入函数的i为i最后的状态
                command=(lambda num: lambda: press_down(num))(i))
            key.pack(side="left", ipadx=0, padx=0, expand=10)
        else:
            key = tk.Button(
                keys_frame,
                width=1,
                height=0,
                bd=1,
                highlightcolor="gainsboro",
                background="gainsboro",
                activebackground="blue",
                command=(lambda num: lambda: press_down(num))(i))
            key.pack(side="left", ipadx=0, padx=1, expand=10)


def output_piano(belonging, note_list, duration=2):
    for i in generated_blocks:
        i.destroy()
    _frame = colour_block(generated_blocks, belonging, "bottom", width=1000, height=10)
    for i in range(21, 109):
        if i not in note_list:
            colour_block(generated_blocks, _frame, "bottom", width=900, height=10)
        else:
            pass


def press_down(key_num):
    # 注意键盘序号和音符值的区别：一个从0开始，一个从21开始。
    note_value = key_num + 21
    play_note(key_num)
    widget_ = window.focus_get()
    if widget_ in result[2]:
        index_ = result[2].index(widget_)
        if abs(note_value - int(result[2][index_ - 1].get())) <= 12:
            widget_.delete(0, 'end')
            widget_.insert(0, str(note_value))
        else:
            pass
    return key_num


def chord_num_mouse_wheel_change(ent):
    num = int(ent.widget.get())
    if ent.delta > 0 and num < 20:
        ent.widget.delete(0, 'end')
        ent.widget.insert(0, str(num + 1))
    if ent.delta <= 0 and num > 2:
        ent.widget.delete(0, 'end')
        ent.widget.insert(0, str(num - 1))
    if num < 3 or num > 19:
        pass


def bps_mouse_wheel_change(ent):
    num = int(ent.widget.get())
    if ent.delta > 0 and num < 500:
        ent.widget.delete(0, 'end')
        ent.widget.insert(0, str(num + 1))
    if ent.delta <= 0 and num > 20:
        ent.widget.delete(0, 'end')
        ent.widget.insert(0, str(num - 1))
    if num < 21 or num > 499:
        pass


def note_mouse_wheel_change(ent):
    global result
    note_group = result[2]
    note = int(ent.widget.get())
    index_ = note_group.index(ent.widget)
    if index_ == 0:
        if ent.delta > 0 and note < 108:
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, str(note + 1))
        if ent.delta <= 0 and note > 21:
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, str(note - 1))
        if note < 22 or note > 107:
            pass
    else:
        last_note = int(note_group[index_ - 1].get())
        if ent.delta > 0 and note < last_note + 12:
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, str(note + 1))
        if ent.delta <= 0 and note > last_note - 12:
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, str(note - 1))
        if note < last_note - 11 or note > last_note + 11:
            pass


def note_num_mouse_wheel_change(ent):
    num = int(ent.widget.get())
    if ent.delta > 0 and num < 15:
        ent.widget.delete(0, 'end')
        ent.widget.insert(0, str(num + 1))
    if ent.delta <= 0 and num > 3:
        ent.widget.delete(0, 'end')
        ent.widget.insert(0, str(num - 1))
    if num < 4 or num > 14:
        pass


def duration_mouse_wheel_change(ent):
    if str(ent.widget.get()) in available_duration:
        st = str(ent.widget.get())
        num = available_duration.index(st)
        if 0 < ent.delta and num < 47:
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, available_duration[int(num) + 1])
        if ent.delta <= 0 and num > 1:
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, available_duration[int(num) - 1])
        if num < 1 or num > 46:
            pass


# 和回车绑定：判断_entry输入的数字是否属于节拍，并且返回输入的值
def get_duration(ent):
    en = ent.widget.get()
    if en in available_duration:
        return en
    ent.widget.delete(0, 'end')


# 和回车绑定：判断_entry输入的数字是否属于合法音符格式，并且返回输入的值
def get_note(ent):
    note = ent.widget.get()
    try:
        note_ = abs(int(note))
        note_ += 1
    except ValueError:
        ent.widget.delete(0, 'end')
    note_group = result[2]
    index_ = note_group.index(ent.widget)
    if 21 <= int(note) <= 108:
        if index_ == 0:
            pass
        else:
            last_note = int(note_group[index_ - 1].get())
            if abs(last_note - int(note)) >= 13 and last_note != 0:
                ent.widget.delete(0, 'end')
            else:
                pass
    elif int(note) == 0:
        pass
    else:
        ent.widget.delete(0, 'end')


# 和回车绑定：判断_entry输入的数字是否属于音符数量，并且返回输入的值
def get_num(ent):
    en = ent.widget.get()
    try:
        entry_num = abs(int(en))
        if 3 <= entry_num <= 15:
            pass
        else:
            ent.widget.delete(0, 'end')
    except ValueError:
        ent.widget.delete(0, 'end')


# 和回车绑定：判断输入的数字是否属于合法的速度，并且返回输入的值
def get_v(ent):
    entry_v_get = ent.widget.get()
    try:
        v_ = abs(int(entry_v_get))
        if 20 <= v_ <= 500:
            result[4] = int(v_)
        else:
            ent.widget.delete(0, 'end')
    except ValueError:
        ent.widget.delete(0, 'end')


# 和选中绑定：返回下拉框选中的值
def combox_go(ent):
    result[3] = ent.widget.get()


# 定义速度输入框
def v_entry(master, position="top", font_size=13):
    f_entry = tk.Entry(
        master,
        font=('Arial', font_size),
        justify="center",
        width=7)
    cpg_win.append(f_entry)
    f_entry.pack(side=position, expand=0)
    f_entry.insert(0, '120')
    f_entry.bind("<Leave>", get_v)
    f_entry.bind("<Return>", get_v)
    f_entry.bind("<Button-1>", get_v)
    f_entry.bind("<MouseWheel>", bps_mouse_wheel_change)
    return f_entry.get()


""" cpg 读取输入内容："""


def cpg_entry_():
    global result
    # 初始化要返回的数据
    notes_num_entry_box = []
    duration_entry_box = []
    default_note_entry_box = []
    result = [notes_num_entry_box, duration_entry_box, default_note_entry_box]

    # 定义和弦数量输入框
    def chord_num_entry(master, position="top", font_size=13):
        f_entry = tk.Entry(master, font=('Arial', font_size), justify="center", width=7)
        cpg_win.append(f_entry)
        f_entry.pack(side=position, expand=0)
        f_entry.insert(0, '2')
        f_entry.bind("<Return>", draw_input_zone)
        f_entry.bind("<Leave>", draw_input_zone)
        f_entry.bind("<MouseWheel>", chord_num_mouse_wheel_change)
        return [f_entry, f_entry.get()]

    # 和回车绑定：判断输入的数字是否属于合法的和弦数量，并且绘制新的输入框
    def draw_input_zone(ent):
        entry_chord_num_get = ent.widget.get()
        try:
            chord_n = abs(int(entry_chord_num_get))
            if 1 < chord_n < 21:
                pass
            else:
                ent.widget.delete(0, 'end')
        except ValueError:
            ent.widget.delete(0, 'end')

        # 开始绘制输入框
        # 定义输入空
        def draw_blank(master, width):
            blank_frame = tk.Frame(master, background=BG_COLOUR)
            blank_frame.pack(side="left", ipadx=width, expand=0)
            cpg_wd_input_boxs1.append(blank_frame)
            return blank_frame

        # 定义输入框
        def draw_text(master, text):
            text_var = tk.Label(master, text=text, bg=BG_COLOUR, width=9, font=('Arial', 11))
            cpg_wd_input_boxs1.append(text_var)
            text_var.pack(side='left', expand=0)

        # 开始绘制
        if len(cpg_wd_input_boxs1) == 0:
            draw_text(draw_blank(frame_r2, 0), 'Duration:')
            draw_text(draw_blank(frame_r4, 0), 'Default Note:')
            draw_text(draw_blank(frame_re1, 0), 'Note Num:')
        else:
            cpg_wd_input_boxs1[-1].destroy()

        if int(entry_chord_num_get) < len(result[0]):
            # 删除输入框实体，并且将其从列表中删除。
            for i in [result[0], result[1], result[2]]:
                for ii in i:
                    ii.destroy()
            result[0].clear()
            result[1].clear()
            result[2].clear()
            # 绘制新的实体，并加入列表。
            for i in range(int(entry_chord_num_get)):
                entry_box(frame_r2, duration_entry_box, get_duration, duration_mouse_wheel_change, default='2')
                entry_box(frame_r4, default_note_entry_box, get_note, note_mouse_wheel_change, default='60')
                entry_box(frame_re1, notes_num_entry_box, get_num, note_num_mouse_wheel_change, default='3')
        if int(entry_chord_num_get) > len(result[0]):
            box_num = int(entry_chord_num_get)
            # 绘制新的实体，并加入列表。
            for i in range(box_num - len(result[0])):
                entry_box(frame_r2, duration_entry_box, get_duration, duration_mouse_wheel_change, default='2')
                entry_box(frame_r4, default_note_entry_box, get_note, note_mouse_wheel_change, default='60')
                entry_box(frame_re1, notes_num_entry_box, get_num, note_num_mouse_wheel_change, default='3')
        if int(entry_chord_num_get) == len(result[0]):
            pass
        # 输入框右边的空
        draw_blank(frame_r4, 16)

    # 绘制主要分区
    frame = tk.Frame(window, background=BG_COLOUR)
    ll_frame = tk.Frame(frame, background='white')
    l_line_frame = tk.Frame(frame, background='black')
    left_frame = tk.Frame(frame, background=BG_COLOUR)
    right_frame = tk.Frame(frame, background=BG_COLOUR)
    r_line_frame = tk.Frame(frame, background='black')
    rr_frame = tk.Frame(frame, background='white')
    frame.pack(side="top", fill="x", expand=0)
    ll_frame.pack(side="left", fill='both', ipadx=40, expand=0)
    l_line_frame.pack(side="left", fill='y', ipadx=1, expand=0)
    left_frame.pack(side="left", fill='x', ipadx=30, expand=0)
    right_frame.pack(side="left", fill='x', ipadx=0, expand=0)
    r_line_frame.pack(side="left", fill='y', ipadx=1, expand=0)
    rr_frame.pack(side="left", fill='both', ipadx=6, expand=0)
    cpg_win.append(frame)
    cpg_win.append(ll_frame)
    cpg_win.append(l_line_frame)
    cpg_win.append(left_frame)
    cpg_win.append(right_frame)
    cpg_win.append(r_line_frame)
    cpg_win.append(rr_frame)
    """ Draw detailed frames
        细化区块    """
    frame_le1 = tk.Frame(left_frame, height=23, background=BG_COLOUR)
    frame_l1 = tk.Frame(left_frame, height=25, background=STRIPS_COLOUR)
    frame_l2 = tk.Frame(left_frame, height=25, background=BG_COLOUR)
    frame_l3 = tk.Frame(left_frame, height=25, background=STRIPS_COLOUR)
    frame_l4 = tk.Frame(left_frame, height=25, background=BG_COLOUR)
    frame_re1 = tk.Frame(right_frame, height=23, background=BG_COLOUR)
    frame_r1 = tk.Frame(right_frame, height=28, background=STRIPS_COLOUR)
    frame_r2 = tk.Frame(right_frame, height=23, background=BG_COLOUR)
    frame_r3 = tk.Frame(right_frame, height=28, background=STRIPS_COLOUR)
    frame_r4 = tk.Frame(right_frame, height=23, background=BG_COLOUR)
    frame_le1.pack(fill="x", side='top', pady=3, ipady=0, expand=True)
    frame_l1.pack(fill="x", side='top', pady=3, ipady=0, expand=True)
    frame_l2.pack(fill="x", side='top', pady=3, ipady=0, expand=True)
    frame_l3.pack(fill="x", side='top', pady=3, ipady=0, expand=True)
    frame_l4.pack(fill="x", side='top', pady=3, ipady=0, expand=True)
    frame_re1.pack(fill="x", side='top', pady=3, ipady=0, expand=True)
    frame_r1.pack(fill="x", side='top', pady=3, ipady=0, expand=True)
    frame_r2.pack(fill="x", side='top', pady=3, ipady=0, expand=True)
    frame_r3.pack(fill="x", side='top', pady=3, ipady=0, expand=True)
    frame_r4.pack(fill="x", side='top', pady=3, ipady=0, expand=True)
    cpg_win.append(frame_le1)
    cpg_win.append(frame_l1)
    cpg_win.append(frame_l2)
    cpg_win.append(frame_l3)
    cpg_win.append(frame_l4)
    cpg_win.append(frame_re1)
    cpg_win.append(frame_r1)
    cpg_win.append(frame_r2)
    cpg_win.append(frame_r3)
    cpg_win.append(frame_r4)
    """ Add wedges
        向区块添加内容 """
    # 空
    cpg_win_left_blank(frame_le1, 5)
    # 文字：模式
    text_v = tk.Label(frame_le1, text="Model:", width=4, bg=BG_COLOUR, font=('Arial', 11))
    cpg_win.append(text_v)
    text_v.pack(side="left", expand=True)
    # 向返回值添加模式信息
    result.append(combox(frame_le1, cpg_win, combox_go, values=("Melody", "Root", "M＆R", "Random"), ))  # 下拉框：选择模式
    frame_xxx = tk.Frame(frame_le1, width=10, background=BG_COLOUR)
    frame_xxx.pack(fill="y", side='left', expand=True)
    cpg_win.append(frame_xxx)
    # 空
    cpg_win_left_blank(frame_le1, 0)

    # 文字：和弦数量
    text_chord_num = tk.Label(frame_l1, text="Chords' Num:", bg=STRIPS_COLOUR, font=('Arial', 14))
    cpg_win.append(text_chord_num)
    text_chord_num.pack(expand=0)
    chord_num_entry(frame_l2)  # 输入框：输入和弦进行数量
    # 文字：速度(BPS)
    text_v = tk.Label(frame_l3, text="BPS:", bg=STRIPS_COLOUR, font=('Arial', 14))
    cpg_win.append(text_v)
    text_v.pack()
    bpm = v_entry(frame_l4)  # 输入框：输入速度
    result.append(int(bpm))
    y_colour_block(cpg_win, "top", "black")  # 封底
    return result


""" gcpg 读取输入内容："""


def gcpg_entry_():
    return


"""
    Main functions
    主干函数
"""


def starting():
    # 绘制标题和上部空
    y_blank(start_win, "top", 70)
    title(start_win, "Welcome to Chord Progression Generator!", font_size=35, hei=2)
    y_blank(start_win, "top", 10)
    title(start_win, "Select the module that you want to use:", hei=0)
    # 绘制底部空
    y_blank(None, "bottom")
    # 绘制钢琴
    global piano
    img = Image.open('keys2.png')
    piano = ImageTk.PhotoImage(img)
    image_label = tk.Label(window, image=piano)
    image_label.pack(side="bottom")

    # 给两个按钮左右填空
    x_blank(start_win, 'left', 250)
    x_blank(start_win, 'right', 250)
    # 绘制两个按钮
    cpg_button = tk.Button(window, text="CPG", font=('Arial', 25), width=6, height=0, command=cpg_in)
    cpg_button.pack(side="left", expand=True)
    gcpg_button = tk.Button(window, text="GCPG", font=('Arial', 25), width=6, height=0, command=gcpg_in)
    gcpg_button.pack(side="right", expand=True)
    # 给帮助提示填空
    y_blank(start_win, "top", 46)
    # 帮助提示
    help_button = tk.Button(
        window,
        text="Click here to know more\nabout the differences:",
        font=('Arial', 9),
        width=100,
        height=2,
        bd=0,
        background=BG_COLOUR,
        command=for_help)
    help_button.pack(side="top", ipady=0)
    # 向列表添加控件
    start_win.append(cpg_button)
    start_win.append(gcpg_button)
    start_win.append(help_button)
    return


def for_help():
    # TODO: unfinished
    for lable in start_win:
        lable.pack_forget()

    # 将help界面控件隐藏
    def del_help():
        for lable0 in help_win:
            lable0.pack_forget()
        for lable1 in start_win:
            lable1.pack()

    button_frame = tk.Frame(window, bg=BG_COLOUR)
    button_frame.pack(side="top", fill='x', ipadx=0, ipady=0, expand=0)
    help_win.append(button_frame)

    b = tk.Button(button_frame, text="Back", font=('Arial', 15), width=6, height=1, command=del_help)
    b.pack(side="right", expand=0)
    help_win.append(b)
    return


def cpg_in():
    for _ in start_win:
        _.pack_forget()
    title(cpg_win, "Chord Progression Generator:")
    y_colour_block(cpg_win, "top", "black")
    input_piano(cpg_piano)
    _result = cpg_entry_()
    button_frame = cpg_win[8]
    button2(button_frame, cpg_win, generator, text="Launch", font_size=13)
    return _result


def generator():
    global thread_
    """
    Generate Chord Progression, draw.
    生成和弦进行，绘制钢琴卷帘
    :return:
    """
    print_result()
    # 将result中的widget对象转为数字
    l0 = []  # num of notes in chord
    dur1 = []  # duration of chord
    l2 = []  # default note of chord
    for i in result[0]:
        l0.append(int(i.get()))
    for i in result[1]:
        dur1.append(i.get())
    for i in result[2]:
        l2.append(int(i.get()))

    bpm = result[4]
    note_group = l2
    note_num_g = l0
    chords_num = len(result[0])
    model = result[3]
    chord_group = []
    for i in range(chords_num):
        chord = None
        flag = True
        while flag:
            if note_group[i] == 0:
                chord = chorder.Chord(chorder.random_chord(note_num_g[i]))
            if model == 'Melody':
                if note_group[i] == 0:
                    chord = chorder.Chord(chorder.random_chord(note_num_g[i]))
                else:
                    chord = chorder.Chord(chorder.melody_random_chord(note_group[i], note_num_g[i]))
            if model == 'Root':
                if note_group[i] == 0:
                    chord = chorder.Chord(chorder.random_chord(note_num_g[i]))
                else:
                    chord = chorder.Chord(chorder.root_random_chord(note_group[i], note_num_g[i]))
            if model == 'M＆R':
                if note_group[i] == 0:
                    chord = chorder.Chord(chorder.random_chord(note_num_g[i]))
                else:
                    chord = chorder.Chord(chorder.melody_random_chord(note_group[i], note_num_g[i]))
            if model == 'Random':
                chord = chorder.Chord(chorder.random_chord(note_num_g[i]))
            flag = judging(chord, chord_group, span_tolerance=5, same_direction=False, voice_crossing=False)
    for chord in chord_group:
        print(chord.note_grp())
    # 绘制钢琴卷帘
    for i in range(len(note_group)):
        output_piano(generated_blocks, chord_group[i].note_grp())
    thread_ = threading.Thread(target=play_chord_set, args=(player, chord_group, dur1, bpm, "Strings"))  # 新线程，用于分析得到的音频数据
    thread_.daemon = True
    thread_.start()


def gcpg_in():
    for _ in start_win:
        _.pack_forget()
    title(gcpg_win, "Guitar Chord Progression Generator:")
    y_colour_block(cpg_win, "top", "black")


def judging(chord, chord_group, span_tolerance=5, semitone_num_tolerance=2, same_direction=False, voice_crossing=False):
    """
    In this function, we make sure that the given chord is appropriate to be put into chord group.


    :param chord: Judged chord.
    :param chord_group: inside which are class 'Chord' in chorder module.
    :param span_tolerance: The tolerance of span in circle of fifth, the smaller it is, the more harmonic chords are.\
    :param semitone_num_tolerance: Semitone's tolerance.
    :param same_direction: False: Avoid all voices' progression in same direction.
    :param voice_crossing: False: Avoid voice crossing.
    :return: Bool, which will be given to 'flag'.
    """
    # 下面判断是否删除和弦：
    # 通过五度圈值跨度来去掉不和谐的和弦：
    # TODO: span_tolerance的截取方法有待优化，详情见 chorder 文件的 class Chord。
    if chord.span > span_tolerance:
        print(chord.note_grp())
        print("\033[0;31mDissonance\033[0m" + " founded, which will not be selected.")
        return True
    # 通过小二度数量筛选和弦
    if chord.semitone_num > semitone_num_tolerance:
        print(chord.note_grp())
        print("\033[0;31mToo much semitones\033[0m" + " founded, which will not be selected.")
        return True
    # 判断和弦质心是否在中值以上
    if len(chord.note_grp()) > 4 \
            and chord.centroid > chord.note_grp()[-1] / 2 + chord.note_grp()[0] / 2 \
            and chord.note_grp()[0] < chord.note_grp()[-1] - 16:  # TODO: 16 needs to be verified.
        print(chord.note_grp())
        print("\033[0;31mLarge intensity in low voices\033[0m" + " founded, which will not be selected.")
        return True
    # 判断是否已生成过和弦
    last_chord = chord_group[-1] if len(chord_group) != 0 else None
    if len(chord_group) != 0:
        # 判断是否和上一个和弦相同：
        if chord.note_grp() == last_chord.note_grp():
            print(chord.note_grp())
            print("A chord " + "\033[0;31mSame as the last\033[0m" +
                  " one founded, which will not be selected.")
            return True
        # 判断所有声部是否同向：
        elif same_direction is False and len(chord.note_grp()) == len(last_chord.note_grp()) > 2:
            # 定义计数器
            cal = 0
            for i2 in range(len(last_chord.note_grp())):
                if last_chord.note_grp()[i2] > chord.note_grp()[i2]:
                    cal += 1
                if last_chord.note_grp()[i2] > chord.note_grp()[i2]:
                    cal -= 1
            if abs(cal) == len(chord.note_grp()):
                print(chord.note_grp())
                print("All voices are in " + "\033[0;31mSame direction\033[0m" +
                      ", which will not be selected.")
                return True
        elif abs(chord - last_chord) > 7:
            print(chord.note_grp())
            print("The average interval between two chords is too large, which will not be selected.")
            return True
        # 判断是否有声部交错：
        elif voice_crossing is False and chord.note_grp()[0] > chord_group[-1].note_grp()[1]:
            print(chord.note_grp())
            print("\033[0;31mVoice crossing\033[0m" + " founded, which will not be selected.")
            return True
        # 判断低声部进行是否超过五度
        if abs(chord.note_grp()[0] - last_chord.note_grp()[0]) > 8:
            print(chord.note_grp())
            print("\033[0;31mToo large interval\033[0m" +
                  " between lowest voice founded, which will not be selected.")
            return True
        # 判断高声部进行是否超过八度
        if abs(chord.note_grp()[-1] - last_chord.note_grp()[-1]) > 12:
            print(chord.note_grp())
            print("\033[0;31mToo large interval\033[0m" +
                  "between highest voice founded, which will not be selected.")
            return True

    # 通过两个低音判断
    if chord.note_grp()[1] - chord.note_grp()[0] < 4 and chord.note_grp()[1] < 49:
        print(chord.note_grp())
        print(chord.c_type)
        print("\033[0;31mIntense low voice\033[0m" + " founded, which will not be selected.")
        return True
    else:
        print("\033[0;33mYou've got a new chord:\033[0m", end='')
        print(chord.note_grp(), end='   ')
        print(chord.c_type)
        chord_group.append(chord)
        return False


def main():
    print("main")


if __name__ == "__main__":
    # 初始化播放功能
    pg.midi.init()
    player = pg.midi.Output(0)
    freq = 44100
    bit_size = -16
    channels = 2
    buffer = 1024
    pg.mixer.init(freq, bit_size, channels, buffer)
    pg.mixer.music.set_volume(1)
    clock = pg.time.Clock()
    # 定义主窗口对象，名称，图标，大小，防止用户调整尺寸，背景颜色：
    window = tk.Tk()
    window.title('Chord Progression Generator ———Expand your music idea')
    window.iconbitmap('CPG.ico')
    window.geometry('1460x700')
    window.resizable(False, False)
    window.configure(bg=BG_COLOUR)

    starting()  # 开始界面
    thread_ = None
    main()  # 主函数
    window.mainloop()

    # 退出播放插件，程序结束
    del player
    pg.midi.quit()

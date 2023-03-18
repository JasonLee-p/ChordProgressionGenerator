# -*- coding: utf-8 -*-
"""
THis program recognizes pitches in real time.
实时识别音高，不能识别和弦。
"""
import math

import librosa
import pyaudio
import wave
import threading
import queue
import tkinter as tk
import numpy as np
from scipy import signal

hz_array = np.array([32.7, 34.65, 36.71, 38.89, 41.2, 43.65, 46.25, 49.0, 51.91, 55.0, 58.27, 61.74,
                     65.41, 69.3, 73.42, 77.78, 82.41, 87.31, 92.5, 98.0, 103.83, 110.0, 116.54, 123.47,
                     130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.0, 196.0, 207.65, 220.0, 233.08, 246.94,
                     261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.0, 415.3, 440.0, 466.16, 493.88,
                     523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.0, 932.33, 987.77,
                     1046.5, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.0, 1864.66,
                     1975.53, 2093.0])

hz_notename = {32.7: 'C1', 34.65: '#C1', 36.71: 'D1', 38.89: '#D1', 41.2: 'E1', 43.65: 'F1',
               46.25: '#F1', 49.0: 'G1', 51.91: '#G1', 55.0: 'A1', 58.27: '#A1', 61.74: 'B1',
               65.41: 'C2', 69.3: '#C2', 73.42: 'D2', 77.78: '#D2', 82.41: 'E2', 87.31: 'F2',
               92.5: '#F2', 98.0: 'G2', 103.83: '#G2', 110.0: 'A2', 116.54: '#A2', 123.47: 'B2',
               130.81: 'C3', 138.59: '#C3', 146.83: 'D3', 155.56: '#D3', 164.81: 'E3', 174.61: 'F3',
               185.0: '#F3', 196.0: 'G3', 207.65: '#G3', 220.0: 'A3', 233.08: '#A3', 246.94: 'B3',
               261.63: 'C4', 277.18: '#C4', 293.66: 'D4', 311.13: '#D4', 329.63: 'E4', 349.23: 'F4',
               369.99: '#F4', 392.0: 'G4', 415.3: '#G4', 440.0: 'A4', 466.16: '#A4', 493.88: 'B4',
               523.25: 'C5', 554.37: '#C5', 587.33: 'D5', 622.25: '#D5', 659.25: 'E5', 698.46: 'F5',
               739.99: '#F5', 783.99: 'G5', 830.61: '#G5', 880.0: 'A5', 932.33: '#A5', 987.77: 'B5',
               1046.5: 'C6', 1108.73: '#C6', 1174.66: 'D6', 1244.51: '#D6', 1318.51: 'E6', 1396.91: 'F6',
               1479.98: '#F6', 1567.98: 'G6', 1661.22: '#G6', 1760.0: 'A6', 1864.66: '#A6', 1975.53: 'B6', 2093.0: 'C7'}

overtone_columns_intervals = [12, 19, 24, 28, 31, 34, 36, 38, 40, 41, 43]


def find_nearest(array, value):
    """
    This function returns the number in a linear array that is closest to the given number.
    该函数返回 numpy 一维数组内离参数value最近的数。
    """
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx - 1]) < math.fabs(value - array[idx])):
        return array[idx - 1]
    else:
        return array[idx]


# 显示的音符名
def title(title_text_var):
    def _title(belonging, master, font_size=60, wid=35, hei=2):
        title_v = tk.Label(
            master,
            textvariable=title_text_var,  # 标签的文字
            bg=BG_COLOUR,  # 标签背景颜色
            font=('Arial', font_size),  # 字体和字体大小
            width=wid, height=hei)  # 标签长宽
        title_v.pack()  # 固定窗口位置
        if belonging is not None:
            belonging.append(title_v)
        title_text_var.set('')
    return _title


def find_note(ct):  # 该函数暂时没有用
    """
    :param ct: Counter variable.
    :return: A function
    """
    def _find_note(note_value, note_list):
        nonlocal ct
        for compared_note in note_list:
            if compared_note - note_value == overtone_columns_intervals[0]:
                ct += 1
            elif compared_note - note_value == overtone_columns_intervals[1]:
                ct += 0.5
            elif compared_note - note_value == overtone_columns_intervals[2]:
                ct += 0.25
    return _find_note


# 获取录制的数据，放入q
def audio_callback(in_data, *args):
    global ad_rdy_ev
    q.put(in_data)
    ad_rdy_ev.set()
    return None, pyaudio.paContinue


def read_audio_thread(_q, _stream, _frames, _ad_rdy_ev):
    global latest_notes_list

    while _stream.is_active():
        _ad_rdy_ev.wait(timeout=1000)
        if _q.empty():
            _ad_rdy_ev.clear()
            break
        _data = _q.get()
        # 从_q获取音频流数据（_data看起来是wave文件的数据）
        while not _q.empty():
            _q.get()

        # 将数据存入wav文件
        wav_data = b"".join([_data])
        with wave.open("tmp.wav", "wb") as wf1:
            wf1.setnchannels(CHANNELS)
            wf1.setsampwidth(pyaudio.get_sample_size(FORMAT))
            wf1.setframerate(RATE)
            wf1.writeframes(wav_data)

        # 用快速傅里叶变换算出音符频率
        y, sr = librosa.load('tmp.wav')  # 先存为wave文件
        f0 = librosa.yin(y, fmin=60, fmax=400)  # 变换
        f0[np.isnan(f0)] = 0  # 将空值nan换成0
        f0 = [find_nearest(hz_array, i) for i in list(f0)]  # 将频率转化为最近的标准音的频率

        # TODO:下面筛选出音符。（注意，只能识别单音，暂时不能识别和弦）
        # 将标准频率值添加到列表latest notes list内
        for i in f0:
            latest_notes_list.append(float(i))
        # 取6个频率数据，对组内的音进行整体分析
        if len(latest_notes_list) < 5:
            pass
        else:
            """
            这里暂时不用管
            ct = 0
            for _note in latest_notes_list:
                _find_note = find_note(ct)
                _find_note(_note, latest_notes_list)
            """
            max_note = max(latest_notes_list, key=latest_notes_list.count)  # 取数量最大的频率
            if latest_notes_list.count(max_note) > 2:  # 只有数量最多的频率的数量>2，才会输出
                """
                程序得到的数量最多的频率不一定是基频，有可能是泛音，或者五度音，如果这些音也在latest_note_list列表中，则显示这个音。
                先将这些音的频率从 hz array 中取出：
                    （获取max_note在 hz array 中的索引，再根据 索引减去音程得到的值 作为 新音的索引 来寻找这些音）
                """
                f0_possible1 = hz_array[list(hz_array).index(max_note) - 7]  # 五度音
                f0_possible2 = hz_array[list(hz_array).index(max_note) - 12]  # 第一泛音（八度音）
                f0_possible3 = hz_array[list(hz_array).index(max_note) - 19]  # 第二泛音（高八度五度音）
                if f0_possible2 in latest_notes_list:  # 第一泛音的可能性最大，先判断
                    note_text_var.set(str(hz_notename[f0_possible2]))
                elif f0_possible1 in latest_notes_list:  # 其次是五度音
                    note_text_var.set(str(hz_notename[f0_possible1]))
                elif f0_possible3 in latest_notes_list:  # 最后是第二泛音，也就是高八度的五度音
                    note_text_var.set(str(hz_notename[f0_possible3]))
                else:  # 如果上述的音不在列表中，则显示数量最多的音。
                    note_text_var.set(str(hz_notename[max_note]))
            else:  # 如果没有两个以上数量的音，则窗口显示的音符不变，直到下一个音被判断出来。
                # note_text_var.set('')  # ps:这里如果写进去，就会有空白时不时闪烁（因为重新绘制了窗口文字），看起来太丑了/doge
                pass
            latest_notes_list.clear()  # 判定结束，清空列表
        if Recording:
            _frames.append(_data)
        _ad_rdy_ev.clear()


if __name__ == "__main__":
    Recording = False  # 是否在录制
    # 音频基本参数
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "output.wav"

    frames = []
    latest_notes_list = []  # 用于获取得到的音高

    p = pyaudio.PyAudio()  # 创建pyaudio对象
    q = queue.Queue()  # 接受音频流数据的“队列”

    # 音频数据流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=False,
                    frames_per_buffer=CHUNK,
                    stream_callback=audio_callback)

    wf = None
    if Recording:
        # 读取文件，设置基本参数
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

    # 开启音频流，开始录制
    stream.start_stream()

    # 分析数据
    window = signal.hamming(CHUNK)

    ad_rdy_ev = threading.Event()
    thread_ = threading.Thread(target=read_audio_thread, args=(q, stream, frames, ad_rdy_ev))  # 新线程，用于分析得到的音频数据
    thread_.daemon = True
    thread_.start()

    # Tkinter窗口
    BG_COLOUR = 'Beige'
    window_ = tk.Tk()
    window_.title('Pitch recognizer')
    window_.iconbitmap('CPG.ico')
    window_.geometry('300x166')
    # window_.resizable(False, False)
    window_.configure(bg=BG_COLOUR)
    window_widgets = []
    note_text_var = tk.StringVar()
    t = title(note_text_var)
    t(belonging=window_widgets, master=window_)

    window_.mainloop()  # 循环

    # 退出窗口后，停止并且关闭音频流，删除pyaudio对象
    stream.stop_stream()
    stream.close()
    p.terminate()

    if Recording:
        # 将wf的数据还原为初始状态，并关闭
        wf.writeframes(b''.join(frames))
        wf.close()

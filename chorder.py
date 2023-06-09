"""
    In this module, we set some array to fit note strings into numbers,
    which is necessary to fit the program into 'mido'.
    We also set the class 'Chord', whose attribute is quite common in analysing chords,
    and class 'NoteSet', which is a widely acknowledged tool in analysing chords.
"""

import numpy as np
import random

hz_list = [32.7, 34.65, 36.71, 38.89, 41.2, 43.65, 46.25, 49.0, 51.91, 55.0, 58.27, 61.74,
           65.41, 69.3, 73.42, 77.78, 82.41, 87.31, 92.5, 98.0, 103.83, 110.0, 116.54, 123.47,
           130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.0, 196.0, 207.65, 220.0, 233.08,
           246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.0, 415.3, 440.0,
           466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61,
           880.0, 932.33, 987.77, 1046.5, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98,
           1661.22, 1760.0, 1864.66, 1975.53, 2093.0]

hz_notevalue = {
    32.70: 24,
    34.65: 25,
    36.71: 26,
    38.89: 27,
    41.20: 28,
    43.65: 29,
    46.25: 30,
    49.00: 31,
    51.91: 32,
    55.00: 33,
    58.27: 34,
    61.74: 35,
    65.41: 36,
    69.30: 37,
    73.42: 38,
    77.78: 39,
    82.41: 40,
    87.31: 41,
    92.50: 42,
    98.00: 43,
    103.83: 44,
    110.00: 45,
    116.54: 46,
    123.47: 47,
    130.81: 48,
    138.59: 49,
    146.83: 50,
    155.56: 51,
    164.81: 52,
    174.61: 53,
    185.00: 54,
    196.00: 55,
    207.65: 56,
    220.00: 57,
    233.08: 58,
    246.94: 59,
    261.63: 60,
    277.18: 61,
    293.66: 62,
    311.13: 63,
    329.63: 64,
    349.23: 65,
    369.99: 66,
    392.00: 67,
    415.30: 68,
    440.00: 69,
    466.16: 70,
    493.88: 71,
    523.25: 72,
    554.37: 73,
    587.33: 74,
    622.25: 75,
    659.25: 76,
    698.46: 77,
    739.99: 78,
    783.99: 79,
    830.61: 80,
    880.00: 81,
    932.33: 82,
    987.77: 83,
    1046.50: 84,
    1108.73: 85,
    1174.66: 86,
    1244.51: 87,
    1318.51: 88,
    1396.91: 89,
    1479.98: 90,
    1567.98: 91,
    1661.22: 92,
    1760.00: 93,
    1864.66: 94,
    1975.53: 95,
    2093.00: 96
}

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

value_note = {0: 'C', 1: '#C', 2: 'D', 3: '#D', 4: 'E', 5: 'F', 6: '#F', 7: 'G', 8: '#G', 9: 'A', 10: '#A', 11: 'B',
              # 第一行用于计算根音
              21: 'A0', 22: '#A0', 23: 'B0', 24: 'C1', 25: '#C1', 26: 'D1', 27: '#D1', 28: 'E1', 29: 'F1', 30: '#F1',
              31: 'G1', 32: '#G1', 33: 'A1', 34: '#A1', 35: 'B1', 36: 'C2', 37: '#C2', 38: 'D2', 39: '#D2', 40: 'E2',
              41: 'F2', 42: '#F2', 43: 'G2', 44: '#G2', 45: 'A2', 46: '#A2', 47: 'B2', 48: 'C3', 49: '#C3', 50: 'D3',
              51: '#D3', 52: 'E3', 53: 'F3', 54: '#F3', 55: 'G3', 56: '#G3', 57: 'A3', 58: '#A3', 59: 'B3', 60: 'C4',
              61: '#C4', 62: 'D4', 63: '#D4', 64: 'E4', 65: 'F4', 66: '#F4', 67: 'G4', 68: '#G4', 69: 'A4', 70: '#A4',
              71: 'B4', 72: 'C5', 73: '#C5', 74: 'D5', 75: '#D5', 76: 'E5', 77: 'F5', 78: '#F5', 79: 'G5', 80: '#G5',
              81: 'A5', 82: '#A5', 83: 'B5', 84: 'C6', 85: '#C6', 86: 'D6', 87: '#D6', 88: 'E6', 89: 'F6', 90: '#F6',
              91: 'G6', 92: '#G6', 93: 'A6', 94: '#A6', 95: 'B6', 96: 'C7', 97: '#C7', 98: 'D7', 99: '#D7', 100: 'E7',
              101: 'F7', 102: '#F7', 103: 'G7', 104: '#G7', 105: 'A7', 106: '#A7', 107: 'B7', 108: 'C8'}
# 倒过来
n_v = {'A0': 21, '#A0': 22, 'B0': 23, 'C1': 24, '#C1': 25, 'D1': 26, '#D1': 27, 'E1': 28, 'F1': 29, '#F1': 30,
       'G1': 31, '#G1': 32, 'A1': 33, '#A1': 34, 'B1': 35, 'C2': 36, '#C2': 37, 'D2': 38, '#D2': 39, 'E2': 40,
       'F2': 41, '#F2': 42, 'G2': 43, '#G2': 44, 'A2': 45, '#A2': 46, 'B2': 47, 'C3': 48, '#C3': 49, 'D3': 50,
       '#D3': 51, 'E3': 52, 'F3': 53, '#F3': 54, 'G3': 55, '#G3': 56, 'A3': 57, '#A3': 58, 'B3': 59, 'C4': 60,
       '#C4': 61, 'D4': 62, '#D4': 63, 'E4': 64, 'F4': 65, '#F4': 66, 'G4': 67, '#G4': 68, 'A4': 69, '#A4': 70,
       'B4': 71, 'C5': 72, '#C5': 73, 'D5': 74, '#D5': 75, 'E5': 76, 'F5': 77, '#F5': 78, 'G5': 79, '#G5': 80,
       'A5': 81, '#A5': 82, 'B5': 83, 'C6': 84, '#C6': 85, 'D6': 86, '#D6': 87, 'E6': 88, 'F6': 89, '#F6': 90,
       'G6': 91, '#G6': 92, 'A6': 93, '#A6': 94, 'B6': 95, 'C7': 108, '#C7': 97, 'D7': 98, '#D7': 99, 'E7': 100,
       'F7': 101, '#F7': 102, 'G7': 103, '#G7': 104, 'A7': 105, '#A7': 106, 'B7': 107, 'C8': 108,
       # 若输入小写
       'a0': 21, '#a0': 22, 'b0': 23, 'c1': 24, '#c1': 25, 'd1': 26, '#d1': 27, 'e1': 28, 'f1': 29, '#f1': 30,
       'g1': 31, '#g1': 32, 'a1': 33, '#a1': 34, 'b1': 35, 'c2': 36, '#c2': 37, 'd2': 38, '#d2': 39, 'e2': 40,
       'f2': 41, '#f2': 42, 'g2': 43, '#g2': 44, 'a2': 45, '#a2': 46, 'b2': 47, 'c3': 48, '#c3': 49, 'd3': 50,
       '#d3': 51, 'e3': 52, 'f3': 53, '#f3': 54, 'g3': 55, '#g3': 56, 'a3': 57, '#a3': 58, 'b3': 59, 'c4': 60,
       '#c4': 61, 'd4': 62, '#d4': 63, 'e4': 64, 'f4': 65, '#f4': 66, 'g4': 67, '#g4': 68, 'a4': 69, '#a4': 70,
       'b4': 71, 'c5': 72, '#c5': 73, 'd5': 74, '#d5': 75, 'e5': 76, 'f5': 77, '#f5': 78, 'g5': 79, '#g5': 80,
       'a5': 81, '#a5': 82, 'b5': 83, 'c6': 84, '#c6': 85, 'd6': 86, '#d6': 87, 'e6': 88, 'f6': 89, '#f6': 90,
       'g6': 91, '#g6': 92, 'a6': 93, '#a6': 94, 'b6': 95, 'c7': 108, '#c7': 97, 'd7': 98, '#d7': 99, 'e7': 100,
       'f7': 101, '#f7': 102, 'g7': 103, '#g7': 104, 'a7': 105, '#a7': 106, 'b7': 107, 'c8': 108,
       # 如果没有输入音区：
       'C': 60, '#C': 61, 'D': 62, '#D': 63, 'E': 64, 'F': 65,
       '#F': 66, 'G': 67, '#G': 68, 'A': 69, '#A': 70, 'B': 71,
       # 如果没有音区也没有大小写
       'c': 60, '#c': 61, 'd': 62, '#d': 63, 'e': 64, 'f': 65,
       '#f': 66, 'g': 67, '#g': 68, 'a': 69, '#a': 70, 'b': 71}

input_note_list = ['A0', '#A0', 'B0', 'C1', '#C1', 'D1', '#D1', 'E1', 'F1', '#F1', 'G1', '#G1', 'A1', '#A1', 'B1',
                   'C2', '#C2', 'D2', '#D2', 'E2', 'F2', '#F2', 'G2', '#G2', 'A2', '#A2', 'B2',
                   'C3', '#C3', 'D3', '#D3', 'E3', 'F3', '#F3', 'G3', '#G3', 'A3', '#A3', 'B3',
                   'C4', '#C4', 'D4', '#D4', 'E4', 'F4', '#F4', 'G4', '#G4', 'A4', '#A4', 'B4',
                   'C5', '#C5', 'D5', '#D5', 'E5', 'F5', '#F5', 'G5', '#G5', 'A5', '#A5', 'B5',
                   'C6', '#C6', 'D6', '#D6', 'E6', 'F6', '#F6', 'G6', '#G6', 'A6', '#A6', 'B6',
                   'C7', '#C7', 'D7', '#D7', 'E7', 'F7', '#F7', 'G7', '#G7', 'A7', '#A7', 'B7', 'C8',
                   'a0', '#a0', 'b0', 'c1', '#c1', 'd1', '#d1', 'e1', 'f1', '#f1', 'g1', '#g1', 'a1', '#a1', 'b1',
                   'c2', '#c2', 'd2', '#d2', 'e2', 'f2', '#f2', 'g2', '#g2', 'a2', '#a2', 'b2',
                   'c3', '#c3', 'd3', '#d3', 'e3', 'f3', '#f3', 'g3', '#g3', 'a3', '#a3', 'b3',
                   'c4', '#c4', 'd4', '#d4', 'e4', 'f4', '#f4', 'g4', '#g4', 'a4', '#a4', 'b4',
                   'c5', '#c5', 'd5', '#d5', 'e5', 'f5', '#f5', 'g5', '#g5', 'a5', '#a5', 'b5',
                   'c6', '#c6', 'd6', '#d6', 'e6', 'f6', '#f6', 'g6', '#g6', 'a6', '#a6', 'b6',
                   'c7', '#c7', 'd7', '#d7', 'e7', 'f7', '#f7', 'g7', '#g7', 'a7', '#a7', 'b7', 'c8',
                   'C', '#C', 'D', '#D', 'E', 'F', '#F', 'G', '#G', 'A', '#A', 'B',
                   'c', '#c', 'd', '#d', 'e', 'f', '#f', 'g', '#g', 'a', '#a', 'b']

chord_template = {
    """
        三和弦
    """
    # 大三和弦                                     index:
    'C': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],  # 12*0
    '#C': [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    'D': [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    '#D': [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    'E': [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    'F': [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    '#F': [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    'G': [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    'bA': [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    'A': [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    'bB': [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    'B': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    # 小三和弦
    'Cm': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],  # 12*1
    '#Cm': [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    'Dm': [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    '#Dm': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    'Em': [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    'Fm': [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    '#Fm': [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    'Gm': [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    'bAm': [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    'Am': [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    'bBm': [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    'Bm': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    # 减三和弦
    'Cdim': [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],  # 12*2
    '#Cdim': [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    'Ddim': [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    '#Ddim': [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    'Edim': [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'Fdim': [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    '#Fdim': [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    'Gdim': [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    'bAdim': [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    'Adim': [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    'bBdim': [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    'Bdim': [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    # 增三和弦
    'C/E/#Gaug': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # 12*3
    'bDaug/F/A': [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    'D/#F/#Aaug': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    'bD/G/Baug': [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    # 挂二/四和弦
    'Csus2/Gsus4': [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # 4 + 12*3
    '#Csus2/bAsus4': [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    'Dsus2/Asus4': [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    '#Dsus2/bBsus4': [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    'Esus2/Bsus4': [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    'Fsus2/Csus4': [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    '#Fsus2/#Csus4': [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    'Gsus2/Dsus4': [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    'bAsus2/#Dsus4': [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    'Asus2/Esus4': [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    'bBsus2/Fsus4': [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    'Bsus2/#Fsus4': [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    """
        省略音七和弦
    """
    # 大七和弦（或增大七和弦）省略五音
    'CM7,-5': [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],  # 4 + 12*4
    '#CM7,-5': [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    'DM7,-5': [0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    '#DM7,-5': [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    'EM7,-5': [0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    'FM7,-5': [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
    '#FM7,-5': [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
    'GM7,-5': [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    'bAM7,-5': [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    'AM7,-5': [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    'bBM7,-5': [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    'BM7,-5': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    # 小大七和弦省略五音（有没有减大七和弦？）
    'CmM7,-5': [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],  # 4 + 12*5
    '#CmM7,-5': [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    'DmM7,-5': [0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    '#DmM7,-5': [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    'EmM7,-5': [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
    'FmM7,-5': [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
    '#FmM7,-5': [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
    'GmM7,-5': [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0],
    'bAmM7,-5': [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
    'AmM7,-5': [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    'bBmM7,-5': [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    'BmM7,-5': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    # 属七和弦（或增小七和弦）省略五音
    'C7,-5': [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],  # 4 + 12*6
    '#C7,-5': [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    'D7,-5': [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    '#D7,-5': [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    'E7,-5': [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    'F7,-5': [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    '#F7,-5': [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    'G7,-5': [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    'bA7,-5': [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    'A7,-5': [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    'bB7,-5': [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    'B7,-5': [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    # 属七和弦（或小七和弦）省略三音
    'C7,-3': [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],  # 4 + 12*7
    '#C7,-3': [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    'D7,-3': [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    '#D7,-3': [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    'E7,-3': [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    'F7,-3': [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    '#F7,-3': [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    'G7,-3': [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    'bA7,-3': [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
    'A7,-3': [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
    'bB7,-3': [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    'B7,-3': [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    # 小七和弦（或半减七和弦）省略五音
    'Cm7,-5': [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],  # 4 + 12*8
    '#Cm7,-5': [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    'Dm7,-5': [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    '#Dm7,-5': [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    'Em7,-5': [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    'Fm7,-5': [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
    '#Fm7,-5': [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    'Gm7,-5': [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    'bAm7,-5': [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    'Am7,-5': [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    'bBm7,-5': [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    'Bm7,-5': [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    # 半减七和弦省略三音
    'Cm7-3': [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],  # 4 + 12*9
    '#Cm7-3': [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    'Dm7-3': [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    '#Dm7-3': [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    'Em7-3': [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    'Fm7-3': [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    '#Fm7-3': [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    'Gm7-3': [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    'bAm7-3': [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    'Am7-3': [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    'bBm7-3': [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
    'Bm7-3': [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    """
        七和弦
    """
    # 大七和弦
    'CM7': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],  # 4 + 12*10
    '#CM7': [1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    'DM7': [0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    '#DM7': [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    'EM7': [0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
    'FM7': [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
    '#FM7': [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
    'GM7': [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    'bAM7': [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
    'AM7': [0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
    'bBM7': [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0],
    'BM7': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1],
    # 增大七和弦（半增七和弦）
    'Caug7': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],  # 4 + 12*11
    '#Caug7': [1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    'Daug7': [0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    '#Daug7': [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    'Eaug7': [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    'Faug7': [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
    '#Faug7': [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0],
    'Gaug7': [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1],
    'bAaug7': [1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0],
    'Aaug7': [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
    'bBaug7': [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0],
    'Baug7': [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1],
    # 小大七和弦
    'CmM7': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],  # 4 + 12*12
    '#CmM7': [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    'DmM7': [0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    '#DmM7': [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    'EmM7': [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
    'FmM7': [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
    '#FmM7': [0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
    'GmM7': [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0],
    'bAmM7': [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1],
    'AmM7': [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
    'bBmM7': [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0],
    'BmM7': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    # 属七和弦
    'C7': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],  # 4 + 12*13
    '#C7': [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    'D7': [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    '#D7': [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    'E7': [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    'F7': [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    '#F7': [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    'G7': [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    'bA7': [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
    'A7': [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
    'bB7': [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    'B7': [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
    # 小七和弦
    'Cm7': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],  # 4 + 12*14
    '#Cm7': [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    'Dm7': [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    '#Dm7': [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    'Em7': [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    'Fm7': [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
    '#Fm7': [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    'Gm7': [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    'bAm7': [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
    'Am7': [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
    'bBm7': [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    'Bm7': [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    # 半减七和弦（导七和弦，旧名减小七和弦）
    'Cm7-5': [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],  # 4 + 12*15
    '#Cm7-5': [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    'Dm7-5': [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    '#Dm7-5': [0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    'Em7-5': [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'Fm7-5': [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    '#Fm7-5': [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    'Gm7-5': [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    'bAm7-5': [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    'Am7-5': [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    'bBm7-5': [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
    'Bm7-5': [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    # 减七和弦
    'C /#D/#F/A  dim7': [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],  # 4 + 12*16
    '#C/E /G /bB dim7': [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'D /F /bA/B  dim7': [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    """
        省略音九和弦：
    """
    # 大九和弦省略七音（或加九音）
    'Cadd9': [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],  # 7 + 12*16
    '#Cadd9': [0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
    'Dadd9': [0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    '#Dadd9': [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
    'Eadd9': [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    'Fadd9': [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
    '#Fadd9': [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    'Gadd9': [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    'bAadd9': [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    'Aadd9': [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    'bBadd9': [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    'Badd9': [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    # 大九和弦省略三音（也是五音的大三和弦加四音）
    'C9,-3': [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],  # 7 + 12*17
    '#C9,-3': [1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    'D9,-3': [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    '#D9,-3': [0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    'E9,-3': [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1],
    'F9,-3': [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
    '#F9,-3': [0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
    'G9,-3': [0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0],
    'bA9,-3': [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
    'A9,-3': [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    'bB9,-3': [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0],
    'B9,-3': [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    # 大九和弦（小九和弦）省略五音
    'C9,-5': [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],  # 7 + 12*18
    '#C9,-5': [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    'D9,-5': [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    '#D9,-5': [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0],
    'E9,-5': [0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0],
    'F9,-5': [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0],
    '#F9,-5': [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0],
    'G9,-5': [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
    'bA9,-5': [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
    'A9,-5': [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    'bB9,-5': [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    'B9,-5': [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
}


def chord_type(note_group):
    pass


"""The circle of fifth value of a pitch-class."""
note_cof_value = {0: 0, 1: -5, 2: 2, 3: -3, 4: 4, 5: -1, 6: 6, 7: 1, 8: -4, 9: 3, 10: -2, 11: 5}
# 紧张度计算的音程预设值
note_tension = {0: 0, 1: 32, 2: 8, 3: 4, 4: 2, 5: 1, 6: 16, 7: 1, 8: 2, 9: 4, 10: 8, 11: 32}

"""
    Following functions are used in class Chord:
"""


# 根据预设音域生成随机音符
def random_note(lo, hi):
    if lo < 21:
        lo = 21
    if hi > 108:
        hi = 108
    return random.randint(lo, hi)


# 根据和弦音符数量生成一个随机和弦
def random_chord(number_of_notes_in_chord):
    # 初始化音符列表
    chord_note = []
    # 添加音符
    while len(chord_note) != number_of_notes_in_chord + 1:
        n = random.randint(30, 80)
        if n not in chord_note:
            chord_note.append(n)  # 30-90是音域限制，60为C4(440Hz)
    return sorted(chord_note)


# 根据旋律音与和弦音符数量生成一个随机和弦，机制如上
def melody_random_chord(melody_note, n_of_notes_in_chord):
    chord_note = [melody_note]
    while len(chord_note) != n_of_notes_in_chord:
        n = random.randint(30, melody_note - 1)
        if n not in chord_note:
            chord_note.append(n)  # 30是根音的下限
    return sorted(chord_note)


# 根据根音与和弦音符数量生成一个随机和弦，机制如上
def root_random_chord(root, n_of_notes_in_chord):
    chord_note = [root]
    while len(chord_note) != n_of_notes_in_chord:
        n = random.randint(root + 4, 90)
        if n not in chord_note:
            chord_note.append(n)
    return sorted(chord_note)


# 根据旋律音，根音与和弦音符数量生成一个随机和弦，机制如上
def melody_root_random_chord(melody, root, n_of_notes_in_chord):
    # 判断旋律音和根音是否合法
    if melody + 2 - n_of_notes_in_chord < root:
        return None
    chord_note = [melody, root]
    while len(chord_note) != n_of_notes_in_chord:
        n = random.randint(root + 1, melody - 1)
        if n not in chord_note:
            chord_note.append(n)  # 25是旋律音相对根音的上限
    return sorted(chord_note)


# 音集(已按大小排序)
def c_interval(n_group):
    interval_g = []
    for n in n_group:
        interval = n % 12
        if interval not in interval_g:
            interval_g.append(interval)
    return sorted(interval_g)


# 计算音集中小二度的数量
def semitone_num(c_itv):
    output = 0
    if c_itv[-1] - c_itv[0] == 11:
        output += 1
    for ii in range(len(c_itv)):
        if ii != len(c_itv) - 1 and c_itv[ii + 1] - c_itv[ii] == 1:
            output += 1
    return output


# 色值计算需要五度圈关系
def c_colour(interval):
    spans = []
    for n in interval:
        spans.append(note_cof_value[n])
    return np.mean(spans)


# 五度圈跨度计算需要五度圈关系
def c_span(interval):
    """

    :param interval: Note set
    :return:
    """
    spans = []
    for n in interval:
        spans.append(note_cof_value[n])
    span_g = []
    for i1 in range(len(spans)):
        spans[0] = spans[0] + 12
        span = np.max(spans) - np.min(spans)
        spans.sort()
        span_g.append(span)
    return np.min(span_g)


# 判断和弦类型
def c_type(n_g):
    """

    :param n_g: Note group in a chord.
    :return: type = str (The type of the chord)
    """
    output = ''
    if len(n_g) == 2:
        if n_g[0] + 3 == n_g[1] or n_g[0] + 9 == n_g[1]:
            output = "这可能是一个小三和弦(省略五音)"
        elif n_g[0] + 4 == n_g[1] or n_g[0] + 8 == n_g[1]:
            output = "这可能是一个大三和弦(省略五音)"
        else:
            output = "\033[0;31mIt's just an interval\033[0m"
    elif len(n_g) == 3:
        # 大三和弦
        if n_g[0] + 7 == n_g[1] + 3 == n_g[2]:
            output = "这是一个大三和弦,主音是：" + str(value_note[n_g[0]])
            return str(value_note[n_g[0] % 12])
        elif n_g[0] + 9 == n_g[1] + 4 == n_g[2]:
            output = "这是一个大三和弦,主音是：" + str(value_note[n_g[1]])
            return str(value_note[n_g[1] % 12])
        elif n_g[0] + 8 == n_g[1] + 5 == n_g[2]:
            output = "这是一个大三和弦,主音是：" + str(value_note[n_g[2]])
            return str(value_note[n_g[2] % 12])
        # 小三和弦
        elif n_g[0] + 7 == n_g[1] + 4 == n_g[2]:
            output = "这是一个小三和弦,主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 8 == n_g[1] + 3 == n_g[2]:
            output = "这是一个小三和弦,主音是：" + str(value_note[n_g[1]])
        elif n_g[0] + 9 == n_g[1] + 5 == n_g[2]:
            output = "这是一个小三和弦,主音是：" + str(value_note[n_g[2]])
        # 增三和弦
        elif n_g[0] + 8 == n_g[1] + 4 == n_g[2]:
            output = "这是一个增三和弦,或者增增七和弦"
        # 减三和弦
        elif n_g[0] + 6 == n_g[1] + 6 == n_g[2] or n_g[0] + 9 == n_g[1] + 6 == n_g[2] \
                or n_g[0] + 9 == n_g[1] + 3 == n_g[2]:
            output = "这是一个减三和弦,或者减七和弦"
        # 挂四/二和弦
        elif n_g[0] + 7 == n_g[1] + 5 == n_g[2] or n_g[0] + 7 == n_g[1] + 2 == n_g[2] \
                or n_g[0] + 10 == n_g[1] + 5 == n_g[2]:
            output = "这是一个挂四/二和弦"
        # 小小七和弦/导七和弦
        elif n_g[0] + 5 == n_g[1] + 3 == n_g[2]:
            output = "这是一个小小七和弦(省略五音),或者半减七和弦(也叫减小七和弦,导七和弦)(省略五音),主音是：" \
                     + str(value_note[n_g[1]])
        elif n_g[0] + 9 == n_g[1] + 2 == n_g[2]:
            output = "这是一个小小七和弦(省略五音),或者半减七和弦(也叫减小七和弦,导七和弦)(省略五音),主音是：" \
                     + str(value_note[n_g[2]])
        elif n_g[0] + 10 == n_g[1] + 7 == n_g[2]:
            output = "这是一个小小七和弦(省略五音),或者半减七和弦(也叫减小七和弦,导七和弦)(省略五音),主音是：" \
                     + str(value_note[n_g[0]])
        # 大七和弦/增大七和弦
        elif n_g[0] + 5 == n_g[1] + 4 == n_g[2]:
            output = "这是一个大七和弦(省略五音),或者增大七和弦(省略五音),主音是：" + str(value_note[n_g[1]])
        elif n_g[0] + 8 == n_g[1] + 1 == n_g[2]:
            output = "这是一个大七和弦(省略五音),或者增大七和弦(省略五音),主音是：" + str(value_note[n_g[2]])
        elif n_g[0] + 11 == n_g[1] + 7 == n_g[2]:
            output = "这是一个大七和弦(省略五音),或者增大七和弦(省略五音),主音是：" + str(value_note[n_g[0]])
        # 属七和弦/增小七和弦
        elif n_g[0] + 6 == n_g[1] + 4 == n_g[2]:
            output = "这是一个属七和弦(省略五音),或者增小七和弦(省略五音),主音是：" + str(value_note[n_g[1]])
        elif n_g[0] + 8 == n_g[1] + 2 == n_g[2]:
            output = "这是一个属七和弦(省略五音),或者增小七和弦(省略五音),主音是：" + str(value_note[n_g[2]])
        elif n_g[0] + 10 == n_g[1] + 6 == n_g[2]:
            output = "这是一个属七和弦(省略五音),或者增小七和弦(省略五音),主音是：" + str(value_note[n_g[0]])
        # 属七和弦/小小七和弦
        elif n_g[0] + 5 == n_g[1] + 2 == n_g[2]:
            output = "这是一个属七和弦(省略三音),或者小小七和弦(省略三音),主音是：" + str(value_note[n_g[2]])
        elif n_g[0] + 9 == n_g[1] + 7 == n_g[2]:
            output = "这是一个属七和弦(省略三音),或者小小七和弦(省略三音),主音是：" + str(value_note[n_g[1]])
        elif n_g[0] + 10 == n_g[1] + 3 == n_g[2]:
            output = "这是一个属七和弦(省略三音),或者小小七和弦(省略三音),主音是：" + str(value_note[n_g[0]])
        # 导七和弦
        elif n_g[0] + 6 == n_g[1] + 2 == n_g[2]:
            output = "这是一个半减七和弦(也叫减小七和弦,导七和弦)(省略三音),主音是：" + str(value_note[n_g[2]])
        elif n_g[0] + 8 == n_g[1] + 6 == n_g[2]:
            output = "这是一个半减七和弦(也叫减小七和弦,导七和弦)(省略三音),主音是：" + str(value_note[n_g[1]])
        elif n_g[0] + 10 == n_g[1] + 4 == n_g[2]:
            output = "这是一个半减七和弦(也叫减小七和弦,导七和弦)(省略三音),主音是：" + str(value_note[n_g[0]])
        # 增大七和弦
        elif n_g[0] + 4 == n_g[1] + 1 == n_g[2]:
            output = "这是一个增大七和弦(省略三音),主音是：" + str(value_note[n_g[2]])
        elif n_g[0] + 9 == n_g[1] + 8 == n_g[2]:
            output = "这是一个增大七和弦(省略三音),主音是：" + str(value_note[n_g[1]])
        elif n_g[0] + 11 == n_g[1] + 3 == n_g[2]:
            output = "这是一个增大七和弦(省略三音),主音是：" + str(value_note[n_g[0]])
        # 小七/大七
        elif n_g[0] + 5 == n_g[1] + 1 == n_g[2]:
            output = "这是一个小七和弦(省略三音),或者大七和弦(省略三音),主音是：" + str(value_note[n_g[2]])
        elif n_g[0] + 8 == n_g[1] + 7 == n_g[2]:
            output = "这是一个小七和弦(省略三音),或者大七和弦(省略三音),主音是：" + str(value_note[n_g[1]])
        elif n_g[0] + 11 == n_g[1] + 4 == n_g[2]:
            output = "这是一个小七和弦(省略三音),或者大七和弦(省略三音),主音是：" + str(value_note[n_g[0]])
        # 小七
        elif n_g[0] + 4 == n_g[1] + 4 == n_g[2]:
            output = "这是一个小七和弦(省略五音),主音是：" + str(value_note[n_g[1]])
        elif n_g[0] + 9 == n_g[1] + 1 == n_g[2]:
            output = "这是一个小七和弦(省略五音),主音是：" + str(value_note[n_g[2]])
        elif n_g[0] + 11 == n_g[1] + 8 == n_g[2]:
            output = "这是一个小七和弦(省略五音),主音是：" + str(value_note[n_g[0]])
        else:
            output = "\033[0;31mUnable to recognize\033[0m"
    elif len(n_g) == 4:
        if n_g[0] + 9 == n_g[1] + 6 == n_g[2] + 3 == n_g[3]:
            output = "这是一个减七和弦"
        elif n_g[0] + 10 == n_g[1] + 7 == n_g[2] + 4 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 6 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 5 == n_g[2] + 3 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 6 == n_g[2] + 3 == n_g[3]:
            output = "这是一个半减七和弦,主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 10 == n_g[1] + 7 == n_g[2] + 3 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 5 == n_g[2] + 3 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 7 == n_g[2] + 4 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 5 == n_g[2] + 2 == n_g[3]:
            output = "这是一个小小七和弦,主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 10 == n_g[1] + 6 == n_g[2] + 3 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 5 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 6 == n_g[2] + 4 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 7 == n_g[2] + 3 == n_g[3]:
            output = "这是一个属七和弦,主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 10 == n_g[1] + 6 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 8 == n_g[2] + 4 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 6 == n_g[2] + 4 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 4 == n_g[2] + 2 == n_g[3]:
            output = "这是一个增小七和弦,主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 11 == n_g[1] + 7 == n_g[2] + 4 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 5 == n_g[2] + 1 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 7 == n_g[2] + 3 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 5 == n_g[2] + 4 == n_g[3]:
            output = "这是一个大七和弦,主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 11 == n_g[1] + 8 == n_g[2] + 4 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 5 == n_g[2] + 1 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 7 == n_g[2] + 4 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 4 == n_g[2] + 3 == n_g[3]:
            output = "这是一个小七和弦,主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 11 == n_g[1] + 7 == n_g[2] + 3 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 4 == n_g[2] + 1 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 8 == n_g[2] + 4 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 5 == n_g[2] + 4 == n_g[3]:
            output = "这是一个增大七和弦,主音是：" + str(value_note[n_g[0]])
        # 七和弦结束，九和弦开始
        # 大九和弦
        elif n_g[0] + 7 == n_g[1] + 5 == n_g[2] + 3 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 8 == n_g[2] + 5 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 7 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 4 == n_g[2] + 2 == n_g[3]:
            output = "这是一个大九和弦(省略七音),主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 11 == n_g[1] + 9 == n_g[2] + 7 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 8 == n_g[2] + 1 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 3 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 5 == n_g[1] + 4 == n_g[2] + 2 == n_g[3]:
            output = "这是一个大九和弦(省略五音),主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 11 == n_g[1] + 9 == n_g[2] + 4 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 5 == n_g[2] + 1 == n_g[3] \
                or n_g[0] + 7 == n_g[1] + 3 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 7 == n_g[2] + 5 == n_g[3]:
            output = "这是一个大/小九和弦(省略三音),主音是：" + str(value_note[n_g[0]])
        # 小九和弦
        elif n_g[0] + 7 == n_g[1] + 5 == n_g[2] + 4 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 9 == n_g[2] + 5 == n_g[3] \
                or n_g[0] + 11 == n_g[1] + 7 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 3 == n_g[2] + 1 == n_g[3]:
            output = "这是一个小九和弦(省略七音),主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 10 == n_g[1] + 8 == n_g[2] + 7 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 9 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 11 == n_g[1] + 4 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 5 == n_g[1] + 3 == n_g[2] + 1 == n_g[3]:
            output = "这是一个小九和弦(省略五音),主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 10 == n_g[1] + 8 == n_g[2] + 3 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 5 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 7 == n_g[1] + 4 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 7 == n_g[2] + 5 == n_g[3]:
            output = "这是一个小九和弦(省略三音),主音是：" + str(value_note[n_g[0]])
        # 属九和弦
        elif n_g[0] + 10 == n_g[1] + 8 == n_g[2] + 7 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 9 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 11 == n_g[1] + 4 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 5 == n_g[1] + 3 == n_g[2] + 1 == n_g[3]:
            output = "这是一个属九和弦(省略五音),主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 10 == n_g[1] + 8 == n_g[2] + 3 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 5 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 7 == n_g[1] + 4 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 7 == n_g[2] + 5 == n_g[3]:
            output = "这是一个属九和弦(省略三音),主音是：" + str(value_note[n_g[0]])
        # 减九和弦
        elif n_g[0] + 6 == n_g[1] + 4 == n_g[2] + 3 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 9 == n_g[2] + 6 == n_g[3] \
                or n_g[0] + 11 == n_g[1] + 8 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 3 == n_g[2] + 1 == n_g[3]:
            output = "这是一个减九和弦(省略七音),主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 9 == n_g[1] + 7 == n_g[2] + 6 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 9 == n_g[2] + 3 == n_g[3] \
                or n_g[0] + 11 == n_g[1] + 5 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 6 == n_g[1] + 3 == n_g[2] + 1 == n_g[3]:
            output = "这是一个减九和弦(省略五音),主音是：" + str(value_note[n_g[0]])
        elif n_g[0] + 9 == n_g[1] + 7 == n_g[2] + 3 == n_g[3] \
                or n_g[0] + 10 == n_g[1] + 6 == n_g[2] + 3 == n_g[3] \
                or n_g[0] + 8 == n_g[1] + 5 == n_g[2] + 2 == n_g[3] \
                or n_g[0] + 9 == n_g[1] + 6 == n_g[2] + 4 == n_g[3]:
            output = "这是一个减九和弦(省略三音),主音是：" + str(value_note[n_g[0]])
        else:
            output = "\033[0;31mUnable to recognize\033[0m"
    return output


# 该函数需要先创建空列表以导出值
def c_tension(sorted_chord, tension_g):
    interval = []
    for n1 in sorted_chord:
        for n2 in sorted_chord:
            x = n2 - n1
            if x > 0:
                interval.append(note_tension[x])
    tension = np.mean(interval)
    tension_g.append(tension)
    print("均紧张度：" + str(tension))
    return tension_g


# 计算和弦质心：
def centroid(sorted_chord):
    return np.mean(sorted_chord)


# TODO: 根据网上 Paul Hindemith 的根音计算方式把该函数写完
def root_note(note_g):
    possible_root = []
    if note_g[1] - note_g[0] == 7 or 19:
        return note_g[0]
    if note_g[1] - note_g[0] == 5:
        return note_g[1]
    for j in range(len(note_g)):
        for jj in range(len(note_g)):
            if abs(note_g[j] - note_g[jj]) == 7 or note_g[j] - note_g[jj] == 19:
                possible_root.append(note_g[jj])

    return note_g[0]


# TODO: 除了五度圈跨度 (self.span) 之外，为了保证增三和弦能被加入 CPG 和 GCPG 的产物，应当对其 span_tolerance 的算法进行优化，取加权平均数。
class Chord:
    def __init__(self, note_g):
        self.note_group = note_g
        self.c_type = c_type(note_g)
        self.interval = c_interval(note_g)
        self.span = c_span(c_interval(note_g))
        self.colour = c_colour(c_interval(note_g))
        self.semitone_num = semitone_num(c_interval(note_g))
        self.centroid = centroid(note_g)
        self.root_note = root_note(note_g)

    def note_grp(self):
        return self.note_group

    def __sub__(self, other):
        return np.mean(self.note_group) - np.mean(other.note_group)

    def __gt__(self, other):
        if np.mean(self.note_group) > np.mean(other.note_group):
            return True

    def __lt__(self, other):
        if np.mean(self.note_group) < np.mean(other.note_group):
            return True

    def __eq__(self, other):
        if np.mean(self.note_group) == np.mean(other.note_group):
            return self == other


if __name__ == '__main__':
    """
    num_of_note = int(input("How much note do you want to put in the chord?\n"))
    note_group = []
    for i in range(num_of_note):
        note = ''
        while note not in input_note_list:
            note = input("Please enter the " + "\033[0;36mnote\033[0m" +
                         " in appropriate format(like #A4):\n")
        note = int(n_v[note])
        note_group.append(note)
    """
    key_list = list(hz_notevalue.keys())
    print(key_list)

"""
    'gcpg' refers to Guitar Chord Progression Generator.
    Limited by our finger's span, we can't play chords freely on guitar, that's why we made GCPG.
    This module defines the way to generate chords available in guitar playing.
"""

import webbrowser
import numpy as np
import GF
import chorder
from itertools import combinations

# 吉他基本和弦
guitar_basic_chord = {"C": (48, 52, 55, 60, 64), "Cm": (43, 48, 55, 60, 63, 67), "#C": (44, 49, 56, 61, 65, 68),
                      "#Cm": (44, 49, 56, 61, 64, 68), "D": (42, 45, 50, 57, 62, 66), "Dm": (45, 50, 57, 62, 65),
                      "#D": (46, 51, 58, 63, 67, 70), "#Dm": (46, 51, 58, 63, 66, 70), "E": (40, 47, 52, 56, 59, 64),
                      "Em": (40, 47, 52, 55, 59, 64), "F": (41, 48, 53, 57, 60, 65), "Fm": (41, 48, 53, 56, 60, 65),
                      "#F": (42, 49, 54, 58, 61, 66), "#Fm": (42, 49, 54, 58, 60, 66), "G": (42, 46, 49, 55, 59, 67),
                      "Gm": (43, 50, 55, 58, 62, 67), "#G": (44, 51, 56, 59, 64, 68), "#Gm": (44, 51, 56, 59, 63, 68),
                      "A": (40, 45, 52, 57, 61, 64), "Am": (40, 45, 52, 57, 60, 64), "#A": (41, 46, 53, 58, 62, 65),
                      "#Am": (41, 46, 53, 58, 61, 65), "B": (42, 47, 54, 59, 63, 66), "Bm": (42, 47, 54, 59, 62, 66)}


# 判断是否输入了整型，参数：(文字，最大值，超过最大值时输出的文字)
def input_int(text, max_l, beyond_lim_text):
    while True:
        n_of_c = input(text)
        try:
            n_of_c = abs(int(n_of_c))
            if n_of_c <= max_l:
                return int(n_of_c)
            else:
                print(beyond_lim_text)
                continue
        except ValueError:
            pass


# 输入调弦类型，返回空弦音的值(基于mido)
def input_tuning_type():
    t_type = ""
    while t_type not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        t_type = input(
            "\033[0;33m——————————————————————————————\033[0m"
            "\033[0;33m\nPlease enter the tuning type you want to use:\033[0m"
            "\033[0;35m(Enter number!)\n\033[0m"
            "Options:     " + "\033[0;35m1.  Standard E\033[0m" + "             6.  Open E\n"
            "             2.  Drop D  (6th)          7.  Open C\n"
            "             3.  Drop C  (6th)          8.  D-A-D-G-A-D\n"
            "             4.  Drop #C (6th)          9.  D-G-C-G-C-D\n"
            "             5.  Open D                 " + "\033[0;35m10. Customize\n\033[0m"
            "\033[0;37mEnter\033[0m"
            "\033[0;35m 'help' \033[0m"
            "\033[0;37mto know more about Alternative Tuning (in CH)\n\033[0m"
            "\033[0;35m——————————————————————————————\n\033[0m"
        )
        if t_type == 'help':
            webbrowser.open("https://www.zhihu.com/question/283900745")
    if t_type == '1':
        return [40, 45, 50, 55, 59, 64]
    if t_type == '2':
        return [38, 45, 50, 55, 59, 64]
    if t_type == '3':
        return [36, 45, 50, 55, 59, 64]
    if t_type == '4':
        return [37, 45, 50, 55, 59, 64]
    if t_type == '5':
        return [38, 45, 50, 54, 57, 62]
    if t_type == '6':
        return [40, 47, 52, 56, 59, 64]
    if t_type == '7':
        return [36, 43, 48, 55, 55, 64]
    if t_type == '8':
        return [38, 45, 50, 55, 57, 62]
    if t_type == '9':
        return [38, 43, 48, 55, 60, 62]
    # 用户输入自定义的调弦
    if t_type == '10':
        string_group = []
        print("Please enter the note of strings" + "\033[0;36m one by one\033[0m"
              + " in correct format(like #A3):\n(1st string in " + "\033[0;36mStandard Tuning\033[0m" + " is E4)")
        for i in range(6):
            s_note = str(input())
            string_group.append(chorder.n_v[s_note])
        return list(sorted(string_group))


def input_capo_character():
    i_c_c = ""
    while i_c_c not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        i_c_c = input(
            "\033[0;33m——————————————————————————————\033[0m"
            "\033[0;33m\nPlease enter the capo's character:\033[0m"
            "\033[0;35m(Enter number!)\n\033[0m"
            "\033[0;35m——————————————————————————————\n\033[0m"
        )
    return int(i_c_c)


class GCPG:
    def __init__(self):
        # 调弦类型
        self.tuning_type = input_tuning_type()
        # 变调夹品位
        self.capo_character = input_int("Please enter the character number of capo:\n"
                                        "If no capo, enter '0'",
                                        12,
                                        "Please enter an integer no more than 12:")
        # 可用的和弦(受限于手指跨度)
        self.available_chords = []


def main():
    while True:
        #
        tuning_type = input_tuning_type()
        capo_character = input_capo_character()
        span_tlr = 7
        available_barre_chord = GF.barre_chord(tuning_type, capo_character, span_tlr) \
            + GF.five_barre_chord_fts(tuning_type, capo_character, span_tlr)\
            + GF.four_barre_chord_fts(tuning_type, capo_character, span_tlr)

        available_barre_chord = np.unique(available_barre_chord)
        for ch in available_barre_chord:
            print(ch)
        print(len(available_barre_chord))
        # 判断是否退出
        flag = input(
            "\033[0;33m——————————————————————————————\n\033[0m"
            "Enter '" + "\033[0;32myes\033[0m" + "' to play GCPG again:\n"
        )
        if flag == 'yes':
            continue
        else:
            print(
                "\033[0;33m——————————————————————————————\n\033[0m"
                "\033[0;33m                Thank you for using GCPG!\033[0m"
            )
            break


if __name__ == "__main__":
    main()

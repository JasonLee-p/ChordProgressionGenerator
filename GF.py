"""
    'GF' refers to Guitar Fingering, it works in module GCPG.
    This module defines all the available fingerings in guitar playing, which is used by GCPG.
"""

import itertools

import chorder

"""
    This function defines a dictionary of barre chord's finger types and its range.
    该函数定义全封闭和弦指法组，返回所有可能的和弦
    Attention:
        the subset of finger type set, which can be regarded as half barre chord, is not included in the set.
    注意：
        可以看作半封闭和弦的指法组子集（即有从6弦开始，有连续的，没演奏的弦），是不被包含在这个和弦指法组内的。
"""


def barre_chord(tuning_type, capo_character=0, span_tolerance=7):
    """

    :param tuning_type: Tuning type, which could be predefined in GCPG.
    :param capo_character: Capo character, which could be predefined in GCPG.
    :param span_tolerance: The tolerance of span in circle of fifth, the smaller it is, the more harmonic chords are.
    :return: Available barre chords' list.
    """
    # 初始化和弦指法组和数组
    finger_type_set = []
    # 先定义没有演奏的弦
    unplayed_string = None
    # 通过排列组合生成所有的和弦指法组
    for e in itertools.product([2, 1, 0, unplayed_string], repeat=6):
        # 初始化计数器（递归计算没有手指摁弦的弦数，计算空弦数）
        cal_no_finger = 0
        cal_empty_string = 0
        for n in e:
            if n == 0 or n == unplayed_string:
                cal_no_finger += 1
            if n == unplayed_string:
                cal_empty_string += 1
        # 加入到指法组的条件：用到三个以下的手指；和弦音符数量 >= 4；6弦有音符
        if cal_no_finger > 2 \
                and cal_empty_string < 3 \
                and e[0] != unplayed_string:
            finger_type_set.append(e)

    # 将指法组改为和弦组
    available_cg_6 = []
    for ft in finger_type_set:
        # 初始化要导出的和弦
        chord = []
        # 从指法组向和弦内添加音符
        for i in range(len(ft)):
            if ft[i] is not None:
                chord.append(tuning_type[i] + ft[i])
        # 创建chorder中的Chord实例
        chord1 = chorder.Chord(chord)
        # 用chorder中的方法判断音集是否有两个以上的小二度，用c_span方法判断其和谐程度：
        if chord1.semitone_num < 2 \
                and chord1.span <= span_tolerance\
                and chord[1] - chord[0] > 2 \
                and chord[2] - chord[1] > 2:
            # 依次升高12品，将得到的和弦加入和弦组
            for ii in range(capo_character, 12):
                available_cg_6.append(list(note + ii for note in chord))
    return available_cg_6


# TODO: span_tolerance的截取方法有待优化，详情见 chorder 文件的 class Chord。
def five_barre_chord_fts(tuning_type, capo_character=0, span_tolerance=7):
    """

    :param tuning_type: Tuning type, which could be predefined in GCPG.
    :param capo_character: Capo character, which could be predefined in GCPG.
    :param span_tolerance: The tolerance of span in circle of fifth, the smaller it is, the more harmonic chords are.
    :return: Available five-strings' half barre chords' list.
    """
    # 初始化和弦指法组和数组
    finger_type_set = []
    # 先定义没有演奏的弦
    unplayed_string = None
    # 通过排列组合生成所有的和弦指法组
    for e in itertools.product([2, 1, 0, unplayed_string], repeat=5):
        # 初始化计数器（递归计算没有手指摁弦的弦数，计算空弦数）
        cal_no_finger = 0
        cal_empty_string = 0
        for n in e:
            if n == 0 or n == unplayed_string:
                cal_no_finger += 1
            if n == unplayed_string:
                cal_empty_string += 1
        # 加入到指法组的条件：用到三个以下的手指；和弦音符数量 >= 4；5弦有音符
        if cal_no_finger > 2 \
                and cal_empty_string < 3 \
                and e[0] != unplayed_string:
            finger_type_set.append(e)

    # 将指法组改为和弦组
    available_gc = []
    for ft in finger_type_set:
        # 初始化要导出的和弦
        chord = []
        # 从指法组向和弦内添加音符
        for i in range(len(ft)):
            if ft[i] is not None:
                chord.append(tuning_type[i + 1] + ft[i])
        for ii in range(capo_character, 12):
            chord0 = (list(note + ii for note in chord))
            chord0.append(tuning_type[0] + capo_character)
            chord0 = sorted(chord0)
            # 创建chorder中的Chord实例
            chord1 = chorder.Chord(chord0)
            # 用chorder中的方法判断音集是否有两个以上的小二度，用c_span方法判断其和谐程度：
            if chord1.semitone_num < 2 \
                    and chord1.span <= span_tolerance \
                    and chord0[1] - chord0[0] > 2 \
                    and chord0[2] - chord0[1] > 2:
                available_gc.append(chord0)
    return available_gc


def four_barre_chord_fts(tuning_type, capo_character=0, span_tolerance=7):
    """

    :param tuning_type: Tuning type, which could be predefined in GCPG.
    :param capo_character: Capo character, which could be predefined in GCPG.
    :param span_tolerance: The tolerance of span in circle of fifth, the smaller it is, the more harmonic chords are.
    :return: Available four-strings' half barre chords' list.
    """
    # 初始化和弦指法组和数组
    finger_type_set = []
    # 先定义没有演奏的弦
    unplayed_string = None
    # 通过排列组合生成所有的和弦指法组
    for e in itertools.product([2, 1, 0, unplayed_string], repeat=4):
        # 初始化计数器（递归计算没有手指摁弦的弦数，计算空弦数）
        cal_no_finger = 0
        cal_empty_string = 0
        for n in e:
            if n == 0 or n == unplayed_string:
                cal_no_finger += 1
            if n == unplayed_string:
                cal_empty_string += 1
        # 加入到指法组的条件：用到三个以下的手指；和弦音符数量 >= 4；5弦有音符
        if cal_no_finger > 2 \
                and cal_empty_string < 3 \
                and e[0] != unplayed_string:
            finger_type_set.append(e)

    # 将指法组改为和弦组
    available_gc = []
    for ft in finger_type_set:
        # 初始化要导出的和弦
        chord = []
        # 从指法组向和弦内添加音符
        for i in range(len(ft)):
            if ft[i] is not None:
                chord.append(tuning_type[i + 2] + ft[i])
        for ii in range(capo_character, 12):
            chord0 = (list(note + ii for note in chord))
            chord0.append(tuning_type[0] + capo_character)
            chord0.append(tuning_type[1] + capo_character)
            chord0 = sorted(chord0)
            # 创建chorder中的Chord实例
            chord1 = chorder.Chord(chord0)
            # 用chorder中的方法判断音集是否有两个以上的小二度，用c_span方法判断其和谐程度：
            if chord1.semitone_num < 2 \
                    and chord1.span <= span_tolerance \
                    and chord0[1] - chord0[0] > 2 \
                    and chord0[2] - chord0[1] > 2:
                available_gc.append(chord0)
    return available_gc


def other_finger_types(tuning_type, capo_character, span_tolerance=7):
    """

    :param tuning_type: Tuning type, which could be predefined in GCPG.
    :param capo_character: Capo character, which could be predefined in GCPG.
    :param span_tolerance: The tolerance of span in circle of fifth, the smaller it is, the more harmonic chords are.
    :return: Available none-barred chords' list.
    """
    return


if __name__ == "__main__":
    g6 = barre_chord([40, 45, 50, 55, 59, 64], 5)
    g5 = five_barre_chord_fts([40, 45, 50, 55, 59, 64], 5)
    g4 = four_barre_chord_fts([40, 45, 50, 55, 59, 64], 5)
    print(g4)
    print(len(g6))
    print(len(g5))
    print(len(g4))

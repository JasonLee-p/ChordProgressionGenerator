"""
    This module defines attributes in Pitches-class set theory.

    Attention:
        As mido module consider C4 as 60, in this module, we consider C4's pitch space as 60 instead of 0.
        If an attribute's end is "group", it means that it's disordered.
        If an attribute's end is "segment", it means that it's ordered and contains pitches' or pitch sets' duration.
"""
import chorder
from chorder import note_cof_value
import numpy as np
import random


# 音集（有序或无序）的键位音级集（若不含重复，即repeat = False，可算作无序；反之可算作有序）
def c_n_s(pitch_group, repeat = False):
    cns = []
    for n in pitch_group:
        interval = n % 12
        if repeat is False and interval in cns:
            continue
        else:
            cns.append(interval)
    return cns


# 音集（有序或无序）的五度圈音级集（有序）
def circle_of_fifth_n_s(pitch_group):
    c_o_f_n_s = []
    cofns12 = []
    cofns_12 = []
    for n in pitch_group:
        cof_value = note_cof_value[n % 12]
        c_o_f_n_s.append(cof_value)
        cofns12.append(cof_value + 12)
        cofns_12.append(cof_value - 12)
    return [c_o_f_n_s, cofns12, cofns_12]


# 音集截段的加权平均音高
def pitches_weighed_average(pitch_segment):
    # 从segment获取音符集合
    pitches = pitch_segment[0]
    # 从segment获取时值集合
    duration_list = pitch_segment[1]
    result_list = []
    for i in range(len(pitches)):
        result_list.append(pitches[i] * duration_list[i] / sum(duration_list))
    return sum(result_list)


# 音集（有序无时值）的轮廓截段
def pitches_counter(pitch_series):
    pitch_set = pitch_series[0]
    result = []
    for pitch in pitch_set:
        cal = 0
        for compared_pitch in pitch_set:
            if pitch > compared_pitch:
                cal += 1
        result.append(cal)
    return result


# 音集截段的倾向性（音高，音符密集度）
def tendentiousness(pitch_segment):
    """
    When you use this function, the segment shouldn't be too short. If too short, it's pitch tend might be meaningless.
    :param pitch_segment: A list with two lists: note group(type = int) and its duration(beat, type = float)
    :return: Pitch Tendentiousness and Rhythm Intensity Tendentiousness (type = list).
    """
    # 确保传入的参数是含两个相同长度列表的列表，并且长度大于等于3，否则报错
    if len(pitch_segment[0]) != len(pitch_segment[1]):
        raise RuntimeError("Segment's two lists' length should be the same.")
    if len(pitch_segment[0]) < 3:
        raise RuntimeError("The segment should contain at least 3 notes")
    # 从segment获取音符集合
    pitches = pitch_segment[0]
    # 从segment获取时值集合
    duration_list = pitch_segment[1]
    # 通过时值把segment分成最平均的两半：
    # 先获取分割线split：
    group1 = [duration_list[0]]
    group2 = [duration_list[-1]]
    flag_dict = {}
    for i in range(1, len(duration_list)):
        for i1 in range(0, i + 1):
            group1.append(duration_list[i1])
        for i2 in range(i + 1, len(duration_list)):
            group2.append(duration_list[i2])
        flag_dict[i] = abs(np.sum(group1) - np.sum(group2))
    # 暂时先把最小差值赋给split
    split = min(flag_dict.values())
    # 遍历键，若值等于最小值就返回键
    for n in flag_dict.keys():
        if list(flag_dict.values())[n - 1] == split:
            # 给split正式赋值为分割点
            split = n
            break
    """     Pitch Tendentiousness
            获取完了分割线之后，开始计算分割线前后的音符平均值   """
    pitches1 = []
    pitches2 = []
    durations1 = []
    durations2 = []
    for i in range(split):
        pitches1.append(pitches[i])
        durations1.append(duration_list[i])
    for i in range(split, len(pitches)):
        pitches2.append(pitches[i])
        durations2.append(duration_list[i])
    wa1 = pitches_weighed_average([pitches1, durations1])
    wa2 = pitches_weighed_average([pitches2, durations2])
    # 取加权平均值的差，得到结果
    result = [wa2 - wa1]
    """     Rhythm Intensity Tendentiousness:
            开始计算密集度倾向值：                         """
    t1 = []
    t2 = []
    for i in range(split):
        t1.append(duration_list[i])
    for i in range(split, len(duration_list)):
        t2.append(duration_list[i])
    # 取平均值倒数的差，即每拍的音符数量之差，得到结果
    result.append(1 / np.mean(t2) - 1 / np.mean(t1))
    return result


# 音级集（有序或无序均可）的Transportation操作
def transport(pitch_class_group, num):
    result = []
    for pitch_set in pitch_class_group:
        return_set = (pitch_set + num) % 12
        result.append(return_set)
    return result


# 音级集（有序或无序均可）的Inversion倒影操作,num是以0为轴倒影后加的数字
def inversion(pitch_class_group, num):
    result_g = []
    for pitch_class in pitch_class_group:
        result = 12 - pitch_class + num
        result_g.append(result)
    return result_g


# 截段的分割（position只属于后面一段）
#　TODO: Unfinished
def cut(pitch_segment, position):
    if len(pitch_segment[0]) < 4:
        raise RuntimeError("The minimum of pitch_segment's length is 4.")
    if int(position) >= len(pitch_segment[0]) - 2 or position < 2:
        raise RuntimeError("The 'position' attribute should cut the pitch_segment into two parts that contains at least two notes.")
    return


# 有序的音集（截段）
class PitchSegment:
    """ Attribute 'segment' should be a list of two lists.  """

    def __init__(self, segment):
        self.pitch_group = segment[0]
        self.duration_group = segment[1]
        self.w_average = pitches_weighed_average(segment)
        segment_result = tendentiousness(segment)
        self.pitch_tend = segment_result[0]
        self.rhythm_intensity_tend = segment_result[1]

    def get_average(self):
        return self.w_average

    def get_pitch_tend(self):
        return self.pitch_tend

    def get_rhythm_intensity_tend(self):
        return self.rhythm_intensity_tend

    def transportation(self, num):
        result = []
        for pitch in self.pitch_group:
            return_pitch = pitch + num
            result.append(return_pitch)
        return [result, self.duration_group]


# 无序的音集（音组）
class PitchSet(chorder.Chord):
    def __init__(self, note_g):
        super().__init__(note_g)
        self.note_group = note_g
        self.c_type = chorder.c_type(note_g)
        self.interval = chorder.c_interval(note_g)
        self.span = chorder.c_span(chorder.c_interval(note_g))
        self.colour = chorder.c_colour(chorder.c_interval(note_g))
        self.semitone_num = chorder.semitone_num(chorder.c_interval(note_g))
        self.root_note = chorder.root_note(note_g)


# 轮廓截段
class ContourSegment:
    def __init__(self, segment):
        self.pitch_set = segment[0]


# 音集序列
class PitchClassSeries:
    def __init__(self, segment):
        self.pitch_class_series = c_n_s(segment[0], True)
        self.duration_list = segment[1]


# 音级集合
class PitchClassSet:
    # TODO: unfinished
    def __init__(self, note_g):
        self.note_g = note_g
        # 为了防止每调用一次都计算函数，先把结果存进变量
        ns = sorted(c_n_s(note_g))
        dns = c_n_s(note_g, repeat=True)
        cns = circle_of_fifth_n_s(note_g)
        dcns = circle_of_fifth_n_s(note_g)[1]
        self.note_set = ns
        self.disordered_note_set = dns
        self.cof_note_set = cns
        self.default_cof_note_set = dcns

    def __add__(self, cal_set):
        """
        :param cal_set: The set that you want to add to note set. It has to be as long as the note set.
        """
        result = []
        if len(self.note_set) != len(cal_set):
            raise RuntimeError("The cal_set's length should be equal to note set's length.")
        else:
            for ns in range(len(cal_set)):
                result.append((self.note_set[ns] + cal_set[ns]) % 12)
            return result

    # 比较向位集，向位集的元素数量必须相等
    def compare_cal_set(self, c_set1, c_set2):
        result1 = []
        result2 = []
        if len(c_set1) == len(c_set2):
            for ns in range(len(c_set1)):
                result1.append((self.note_set[ns] + c_set1[ns]) % 12)
            for ns in range(len(c_set2)):
                result2.append((self.note_set[ns] + c_set2[ns]) % 12)
            if result1 == result2:
                return True
        else:
            raise RuntimeError("The compared two c_sets' length should be the same.")


if __name__ == '__main__':
    # chord1_ns = ChordPitchClassSet([50, 60, 65])
    # print(chord1_ns.note_set)
    segment1 = PitchSegment([[60, 64, 67, 59, 60, 62, 60], [2, 1, 1, 1.5, 0.25, 0.25, 2]])
    segment2 = PitchSegment([[60, 64, 67], [2, 1, 1]])
    a1 = segment1.get_average()
    a2 = segment2.get_average()
    pt1 = segment1.get_pitch_tend()
    pt2 = segment2.get_pitch_tend()
    rit1 = segment1.get_rhythm_intensity_tend()
    rit2 = segment2.get_rhythm_intensity_tend()
    print(a1)
    print(pt1)
    print(rit1)
    print(a2)
    print(pt2)
    print(rit2)

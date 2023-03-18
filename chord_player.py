"""
    'CP' refers to Chord Player.
    This module defines how to play chords (in midi file).
"""

from mido import Message, MidiFile, MidiTrack
import pygame
import pygame.midi as pm

pm.init()  # init midi _player
BPM = 120


def play_midi_(chord_group, n_time=1200, duration=False):
    """

    :param chord_group: The chord progression that you want to put into midi.
    :param n_time: The duration of note(ms)
    :param duration: Weather duration is considered or not.
     If not, it should be False; else, it should be a list of [[duration list] and bpm].
    :return: None. But the function saves the midi file and play it.
    """
    # 获取最长和弦组的长度
    mid = MidiFile()
    len_of_chords = []
    for c in chord_group:
        len_of_chords.append(len(c.note_grp()))
    # 创建轨道
    for i in range(max(len_of_chords)):
        track = MidiTrack()
        mid.tracks.append(track)
        # 创建音色
        track.append(Message('program_change', channel=0, program=49, time=0))
    """
    遍历和弦组中的和弦
    """
    for chd_num in range(len(chord_group)):
        beat = eval(duration[0][chd_num])
        """遍历和弦中的音，将其添加到轨道"""
        for n in range(max(len_of_chords)):
            # 和弦音组
            note_g = chord_group[chd_num].note_grp()
            # 初始化数组
            nums = []
            # 算出该和弦的音数，导入数组
            for cal in range(len(note_g)):
                nums.append(cal)
            print(nums)
            # 判断音符编号是否在数组内
            if n in nums:
                # 音符起始
                mid.tracks[n].append(Message('note_on', note=note_g[n], velocity=40, time=1, channel=0))
                mid.tracks[n].append(Message('note_off', note=note_g[n], velocity=40,
                                             time=n_time
                                             if duration is False
                                             else int(60000 * beat / duration[1]),
                                             channel=0))
            else:
                mid.tracks[n].append(Message('note_on', note=21, velocity=0,
                                             time=n_time
                                             if duration is False
                                             else int(60000 * beat / duration[1]),
                                             channel=0))
                mid.tracks[n].append(Message('note_off', note=21, velocity=0, time=0, channel=0))
    mid.save("Chord Progression.mid")
    print("saved")
    """
    Play midi file:
    """
    freq = 22050
    bit_size = -16
    channels = 2
    buffer = 1024
    pygame.mixer.init(freq, bit_size, channels, buffer)
    pygame.mixer.music.set_volume(1)
    clock = pygame.time.Clock()
    pygame.mixer.music.load("Chord Progression.mid")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(30)


def play_chord(_player, note_list, duration, bpm):
    for note in note_list:
        _player.note_on(note, bpm)
    pygame.time.wait(60000 * eval(duration) // bpm)
    for note in note_list:
        _player.note_off(note, bpm)


def play_chord_set(_player, chord_set, duration_set, bpm, instrument):
    """

    :param _player: Pygame.midi.Output(int) variable.
    :param chord_set: A set of class Chord (in 'chorder' model) variable.
    :param duration_set: A set of notes' durations.
    :param bpm: Beats per minutes.
    :param instrument: 'Piano' or 'Strings'
    :return: None
    """
    if _player is None:
        _player = pygame.midi.Output(0)
    if instrument == 'Piano':
        _player.set_instrument(0)
    if instrument == 'Strings':
        _player.set_instrument(44)
    for i in range(len(chord_set)):
        note_list = chord_set[i].note_grp()
        duration = duration_set[i]
        play_chord(_player, note_list, duration, bpm)


if __name__ == "__main__":
    player = pm.Output(0)

"""
    'cpg' refers to chord progression generator.
    This is a part of CPG which can randomly generate chord progression
"""

import sys
# import threading
import chord_player as CP
import chorder
import pygame_module as pgm
import pygame
import os

os.system('')


# 确保用户输入了整型
def input_int(text, limitation, beyond_lim_text):
    while True:
        n_of_c = input(text)
        try:
            n_of_c = abs(int(n_of_c))
            if n_of_c <= limitation:
                return int(n_of_c)
            else:
                print(beyond_lim_text)
                continue
        except ValueError:
            pass


# 打印生成结果(每次生成完一个和弦组后运行)
def print_result(chord_group):
    print("\033[0;35mGenerated progression:\033[0m")
    print("\033[0;33m——————————————————————————————\033[0m")
    for cd in chord_group:
        for n in cd.note_grp():
            if n == cd.note_grp()[-1]:
                print(n)
            else:
                print(n, end=', ')
    print("\033[0;33m——————————————————————————————\033[0m")


# 旋律音模式
def melody_model(glb_counter, nu_of_chord, chord_group, span_tolerance, same_direction, voice_crossing):
    """

    :param glb_counter: Has been predefined, which counts the chord that the function has generated.
    :param nu_of_chord: Has been predefined.
    :param chord_group: Should have been initialized as an empty list.
    :param span_tolerance: Should be eq to span_tolerance in create_harmonic_progression() function.
    :param same_direction: Should be eq to same_direction in create_harmonic_progression() function.
    :param voice_crossing: Should be eq to voice_crossing in create_harmonic_progression() function.
    :return: Chord group, inside which are class 'Chord' in Chorder.
    """
    while glb_counter != nu_of_chord:
        # 输入旋律音
        # draw_th.start()
        m_note = ''
        while m_note not in chorder.input_note_list:
            m_note = input(
                "\033[0;33m——————————————————————————————\n\033[0m"
                "Please enter the melody " + "\033[0;33mnote\033[0m" +
                " in appropriate format(like #A4):\n\n\n"
            )
            if m_note == "quit":
                return 0
        m_note = int(chorder.n_v[m_note])
        # 输入音符数
        n_of_note = input_int("Please enter the desire " + "\033[0;33mnumber\033[0m" + " of notes in this chord:\n",
                              15, "\033[0;31mYou can at most generate 15 notes in a chord.\033[0m")
        while True:
            # 新建chord实例
            chord = chorder.Chord(chorder.melody_random_chord(m_note, n_of_note))
            # 重命名chord_group[-1]，即上一个和弦：
            last_chord = chord_group[-1] if len(chord_group) != 0 else None
            # 下面判断是否删除和弦：

            # 通过五度圈值跨度来去掉不和谐的和弦：
            # TODO: span_tolerance的截取方法有待优化，详情见 chorder 文件的 class Chord。
            if chord.span > span_tolerance:
                print(chord.note_grp())
                print("\033[0;31mDissonance\033[0m" + " founded, which will not be selected.")
                continue
            # 判断是否已生成过和弦
            if len(chord_group) != 0:
                # 判断是否和上一个和弦相同：
                if chord.note_grp() == last_chord.note_grp():
                    print(chord.note_grp())
                    print("A chord " + "\033[0;31mSame as the last\033[0m" +
                          " one founded, which will not be selected.")
                    continue
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
                        continue
                elif abs(chord - last_chord) > 7:
                    print(chord.note_grp())
                    print("The average interval between two chords is too large, which will not be selected.")
                    continue
                # 判断是否有声部交错：
                elif voice_crossing is False and chord.note_grp()[0] > chord_group[-1].note_grp()[1]:
                    print(chord.note_grp())
                    print("\033[0;31mVoice crossing\033[0m" + " founded, which will not be selected.")
                    continue
                # 判断低声部进行是否超过五度
                if abs(chord.note_grp()[0] - last_chord.note_grp()[0]) > 8:
                    print(chord.note_grp())
                    print("\033[0;31mToo large interval\033[0m" +
                          "between lowest voice founded, which will not be selected.")
                    continue
            # 通过两个低音判断
            if chord.note_grp()[1] - chord.note_grp()[0] < 4 and chord.note_grp()[1] < 49:
                print(chord.note_grp())
                print(chord.c_type)
                print("\033[0;31mIntense low voice\033[0m" + " founded, which will not be selected.")
                continue
            else:
                glb_counter += 1
                print("\033[0;33mYou've got a new chord:\033[0m", end='')
                print(chord.note_grp(), end='   ')
                print(chord.c_type)
                chord_group.append(chord)
                break
    # 打印结果：
    print_result(chord_group)
    return chord_group


# 根音模式
def root_model(glb_counter, nu_of_chord, chord_group, span_tolerance, same_direction, voice_crossing):
    """

    :param glb_counter: Has been predefined, which counts the chord that the function has generated.
    :param nu_of_chord: Has been predefined.
    :param chord_group: Should have been initialized as an empty list.
    :param span_tolerance: Should be eq to span_tolerance in create_harmonic_progression() function.
    :param same_direction: Should be eq to same_direction in create_harmonic_progression() function.
    :param voice_crossing: Should be eq to voice_crossing in create_harmonic_progression() function.
    :return: Chord group, inside which are class 'Chord' in Chorder.
    """
    while glb_counter != nu_of_chord:
        # 输入根音，并通过chorder转化为数字
        r_note = ''
        flag0 = True
        while flag0:
            if r_note not in chorder.input_note_list:
                r_note = input(
                    "\033[0;33;1m——————————————————————————————\n\033[0m"
                    "Please enter the root " + "\033[0;33mnote\033[0m" +
                    " in appropriate format(like #A2):\n\n\n"
                )
            # 防止用户输入的根音跨度过大
            if glb_counter != 0 and abs(chorder.n_v[r_note] - chord_group[-1].note_grp()[0]) > 8:
                print("\033[0;31mToo large interval\033[0m" + "between root notes, Please enter another note:")
                continue
            if r_note == "quit":
                return 0
            else:
                flag0 = False
        r_note = int(chorder.n_v[r_note])
        # 输入音符数
        nu_of_note = input_int("Please enter the desire " + "\033[0;33mnumber\033[0m" + " of notes in this chord:\n",
                               15, "\033[0;31mYou can at most generate 15 notes in a chord.\033[0m")
        while True:
            # 新建chord实例
            chord = chorder.Chord(chorder.root_random_chord(r_note, nu_of_note))
            # 重命名chord_group[-1]，即上一个和弦：
            last_chord = chord_group[-1] if len(chord_group) != 0 else None
            # 下面判断是否删除和弦：

            # TODO: span_tolerance的截取方法有待优化，详情见 chorder 文件的 class Chord。
            # 通过五度圈值跨度来去掉不和谐的和弦：
            if chord.span > span_tolerance:
                print(chord.note_grp())
                print("\033[0;31mDissonance\033[0m" + " founded, which will not be selected.")
                continue
            # 判断是否已生成过和弦
            if len(chord_group) != 0:
                # 判断是否和上一个和弦相同：
                if chord.note_grp() == last_chord.note_grp():
                    print(chord.note_grp())
                    print("A chord " + "\033[0;31mSame as the last\033[0m" +
                          " one founded, which will not be selected.")
                    continue
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
                        continue
                elif abs(chord - last_chord) > 7:
                    print(chord.note_grp())
                    print("The average interval between two chords is too large, which will not be selected.")
                    continue
                # 判断是否有声部交错：
                elif voice_crossing is False and chord.note_grp()[0] > chord_group[-1].note_grp()[1]:
                    print(chord.note_grp())
                    print("\033[0;31mVoice crossing\033[0m" + " founded, which will not be selected.")
                    continue
            else:
                glb_counter += 1
                print("\033[0;33mYou've got a new chord:\033[0m", end='')
                print(chord.note_grp())
                chord_group.append(chord)
                break
    # 打印结果：
    print_result(chord_group)
    return chord_group


# 旋律音+根音模式
def both_model(glb_counter, nu_of_chord, chord_group, span_tolerance, same_direction, voice_crossing):
    """

        :param glb_counter: Has been predefined, which counts the chord that the function has generated.
        :param nu_of_chord: Has been predefined.
        :param chord_group: Should have been initialized as an empty list.
        :param span_tolerance: Should be eq to span_tolerance in create_harmonic_progression() function.
        :param same_direction: Should be eq to same_direction in create_harmonic_progression() function.
        :param voice_crossing: Should be eq to voice_crossing in create_harmonic_progression() function.
        :return: Chord group, inside which are class 'Chord' in Chorder.
        """
    return glb_counter, nu_of_chord, chord_group, span_tolerance, same_direction, voice_crossing


# 随机模式
def random_model(glb_counter, nu_of_chord, chord_group, span_tolerance, same_direction, voice_crossing):
    """

    :param glb_counter: Has been predefined, which counts the chord that the function has generated.
    :param nu_of_chord: Has been predefined.
    :param chord_group: Should have been initialized as an empty list.
    :param span_tolerance: Should be eq to span_tolerance in create_harmonic_progression() function.
    :param same_direction: Should be eq to same_direction in create_harmonic_progression() function.
    :param voice_crossing: Should be eq to voice_crossing in create_harmonic_progression() function.
    :return: Chord group, inside which are class 'Chord' in Chorder.
    """
    while glb_counter != nu_of_chord:
        # 输入音符数
        n_of_note = input_int(
            "\033[0;33;1m——————————————————————————————\n\033[0m"
            "Please enter the desire " + "\033[0;33mnumber\033[0m" + " of notes in this chord:\n\n\n",
            15, "\033[0;31mYou can at most generate 15 notes in a chord.\033[0m"
        )
        while True:
            # 新建chord实例
            chord = chorder.Chord(chorder.random_chord(n_of_note))
            # 重命名chord_group[-1]，即上一个和弦：
            last_chord = chord_group[-1] if len(chord_group) != 0 else None
            # 下面判断是否删除和弦：

            # TODO: span_tolerance的截取方法有待优化，详情见 chorder 文件的 class Chord。
            # 通过五度圈值跨度来去掉不和谐的和弦：
            if chord.span > span_tolerance:
                print(chord.note_grp())
                print("\033[0;31mDissonance\033[0m" + " founded, which will not be selected.")
                continue
            # 判断是否已生成过和弦
            if len(chord_group) != 0:
                # 判断是否和上一个和弦相同：
                if chord.note_grp() == last_chord.note_grp():
                    print(chord.note_grp())
                    print("A chord " + "\033[0;31mSame as the last\033[0m" +
                          " one founded, which will not be selected.")
                    continue
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
                        continue
                elif abs(chord - last_chord) > 7:
                    print(chord.note_grp())
                    print("The average interval between two chords is too large, which will not be selected.")
                    continue
                # 判断是否有声部交错：
                elif voice_crossing is False and chord.note_grp()[0] > chord_group[-1].note_grp()[1]:
                    print(chord.note_grp())
                    print("\033[0;31mVoice crossing\033[0m" + " founded, which will not be selected.")
                    continue
                # 判断低声部进行是否超过五度
                if abs(chord.note_grp()[0] - last_chord.note_grp()[0]) > 8:
                    print(chord.note_grp())
                    print("\033[0;31mToo large interval\033[0m" +
                          "between lowest voice founded, which will not be selected.")
                    continue
            # 通过两个低音判断
            if chord.note_grp()[1] - chord.note_grp()[0] < 4 and chord.note_grp()[1] < 49:
                print(chord.note_grp())
                print("\033[0;31mIntense low voice\033[0m" + " founded, which will not be selected.")
                continue
            else:
                glb_counter += 1
                print(
                    "\033[0;35m——————————————————————————————\n\033[0m"
                    "\033[0;33mYou've got a new chord:\033[0m", end='')
                print(chord.note_grp())
                chord_group.append(chord)
                break
    # 打印结果：
    print_result(chord_group)
    return chord_group


# 主函数
def create_harmonic_progression(span_tolerance=6, same_direction=False, voice_crossing=False):
    """

    :param span_tolerance: The tolerance of span in circle of fifth, the smaller it is, the more harmonic chords are.
    :param same_direction: False: Avoid all voices' progression in same direction.
    :param voice_crossing: False: Avoid voice crossing.
    :return: Chord group, inside which are class 'Chord' in Chorder module.
    """
    # 确保用户输入了正确的生成方式
    g_c_type = ""
    while g_c_type not in ['m', 'r', 'b', 'n', '1', '2', '3', '4']:
        g_c_type = input(
            "\033[0;33m——————————————————————————————\033[0m"
            "\033[0;33m\n Please enter the model you want to use:\033[0m"
            "\033[0;35m(Enter alphabet!)\n\033[0m"
            "\nOptions: You are likely to generate chord progression from:\n\n"
            "         1. "
            "\033[7mm\033[0m"
            "elody note         2. "
            "\033[7mr\033[0m"
            "oot note\n\n"
            "         3. "
            "\033[7mb\033[0m"
            "oth above          4. "
            "\033[7mn\033[0m"
            "one\n"
            "\033[0;35m\n——————————————————————————————\n\033[0m"
        )
    # 从函数取出和弦数量
    nu_of_chord = input_int(
        "\033[0;33m——————————————————————————————\n\033[0m"
        "Please enter your desired " + "\033[0;33mnumber\033[0m" + " of chords\n",
        32,
        "\033[0;31mYou can at most generate 32 chords.\033[0m")
    # 初始化和弦列表
    chord_group = []
    glb_cal = 0
    # 初始化要播放的和弦组
    cg = []
    if g_c_type == "m":
        cg = melody_model(glb_cal, nu_of_chord, chord_group, span_tolerance, same_direction, voice_crossing)
    if g_c_type == "r":
        cg = root_model(glb_cal, nu_of_chord, chord_group, span_tolerance, same_direction, voice_crossing)
    if g_c_type == "n":
        cg = random_model(glb_cal, nu_of_chord, chord_group, span_tolerance, same_direction, voice_crossing)
    CP.play_midi_(cg)
    return cg


def create_the_screen():
    pygame.init()
    screen = pygame.display.set_mode((1500, 200))
    # img = pygame.image.load('工艺战舰图标.ico')
    # pygame.display.set_icon(img)
    pygame.display.set_caption('Chord Generator  ———Expand your music idea')
    screen.fill((230, 230, 230))
    img = pygame.image.load("keys.png")
    screen.blit(img, (50, 50))
    pygame.display.flip()
    return screen


# font0 = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 30)


# 给旋律音赋值
def draw():
    """

    :return: None
    """
    # 通过create_t_s返回的screen，用s把screen传给下面的white_key.selected()函数
    sc = create_the_screen()
    pgm.prt(sc, "Please enter the melody note:", 30, 700, 20)
    # global event
    while True:
        for event in pygame.event.get():
            w_k_g = []
            for i in range(52):
                key = pgm.WKey(i)
                w_k_g.append(key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for k in w_k_g:
                    n_v = k.selected(sc, event)
                    if type(n_v) == int:
                        print(n_v)
                        return n_v
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def main():
    # 主循环：
    while True:
        create_harmonic_progression(span_tolerance=6)
        flag = input(
            "\033[0;33m——————————————————————————————\n\033[0m"
            "Enter '" + "\033[0;32myes\033[0m" + "' to play CPG again:\n"
        )
        if flag == 'yes':
            continue
        else:
            print(
                "\033[0;33m——————————————————————————————\n\033[0m"
                "\033[0;33m                Thank you for using CPG!\033[0m"
            )
            pygame.quit()
            break


if __name__ == "__main__":
    # draw_keys = False
    # draw_th = threading.Thread(group=None, target=draw, name="draw", args=(draw()), kwargs={}, daemon=draw_keys)
    main()

"""
    This is the main part of the program.
"""

import CPG_cpg
import CPG_gcpg
import time
# 解决彩色文字显示失败的问题
import os
os.system('')


# 启动画面
def start():
    print(
        "\033[0;33m\n——————————————————————————————"
        "\n           Welcome to Chord Progression Generator!\n\033[0m"
        "\033[0;35m\n       You can use the tool to expand your music idea."
        "\n——————————————————————————————\033[0m"
        )
    time.sleep(2)


# 选择模块，返回模块名
def select_module():
    """

    :return: type = int (the name of selected module)
    """
    input_module = ""
    while input_module not in ['CPG', 'GCPG', '1', '2']:
        input_module = input(
                       "\033[0;33;1m——————————————————————————————\n\033[0m"
                       "\033[0;33;1m          Please enter the module you want to use:\n\033[0m"
                       "\033[0;37mOptions:\n\033[0m"
                       "                  "
                       "\033[7m CPG \033[0m"
                       "            "
                       "\033[7m GCPG \033[0m"
                       "\n"
                       "\033[0;37mEnter 'help' to know more details\n\033[0m"
                       "\033[0;35m——————————————————————————————\n\033[0m"
                       )
        if input_module == 'help':
            print(
                "\033[0;35m———————————————————————————————————————————————\n\033[0m"
                "\033[0;35m'CPG'\033[0m"
                "  refers to Chord Progression Generator, which can randomly generate chord progression.\n"
                "\033[0;35m'GCPG'\033[0m"
                " refers to Guitar Chord Progression Generator.\n"
                "   Limited by our finger's span, we can't play chords freely on guitar, that's why we made GCPG.\n"
                "   GCPG only generates chords that can be played on guitar.\n"
                "\033[0;35m———————————————————————————————————————————————\033[0m"
                )
            input("\033[0;33;1mPress \033[0m"
                  "\033[5;33;1m'Enter'\033[0m"
                  "\033[0;33;1m to continue:\033[0m")
    return input_module


# 判断是否退出程序，返回布尔值
def quit_():
    """

    :return: type = bool (Whether quit the program or not, which is used in flag of main function's main loop)
    """
    f = input(
        "\033[0;33m——————————————————————————————\n\033[0m"
        "\033[0;33m           Do you want to quit the whole program?\n\033[0m"
        "\033[0;33m                    Enter 'quit' to quit.\n\033[0m"
    )
    if f == 'quit':
        return False
    else:
        return True


if __name__ == "__main__":
    start()
    flag0 = True
    while flag0:
        model = select_module()
        if model in ['CPG', '1']:
            CPG.main()
            flag0 = quit_()
        if model in ['GCPG', '2']:
            GCPG.main()
            flag0 = quit_()
    print(
        "\033[0;33m——————————————————————————————\n\033[0m"
        "                    Good bye!"
    )
    time.sleep(0.5)

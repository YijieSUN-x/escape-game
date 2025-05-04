# pygame_suite/
# ├── game1.py       # 第一个小游戏：问答测验
# ├── game2.py       # 第二个小游戏：猫与警察AI
# ├── game3.py       # 第三个小游戏：逃脱打字
# └── main.py        # 主程序，按123顺序运行游戏





# 文件：main.py
from game1 import run_quiz_game
from game2 import run_cat_police_game
from game3 import run_escape_game
import sys

def main():
    # 按顺序运行游戏，失败则重头开始，三游戏胜利后退出
    while True:
        if not run_quiz_game():
            continue
        if not run_cat_police_game():
            continue
        if not run_escape_game():
            continue
        break

if __name__ == "__main__":
    main()

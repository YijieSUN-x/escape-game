import pygame
import time
import random

def run_escape_game():
    pygame.init()
    WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escape Game")
    clock = pygame.time.Clock()

    # 定义颜色
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE  = (0, 0, 255)

    # 初始化小偷与警察的状态
    thief = {"x": 300, "y": 200, "speed": 5}      # 小偷初始位置与速度
    police = {"x": 50, "y": 200, "speed": 0.5}     # 警察初始位置与速度（较慢）

    # 输入相关状态记录
    input_text = {
        "current": "",                     # 当前输入内容
        "correct_word": "escape",          # 当前目标单词
        "start_time": None                 # 本轮开始输入的时间
    }
    word_list = ["escape", "run", "freedom", "hide"]  # 单词列表（每轮随机）

    font = pygame.font.Font(None, 36)     # 设置字体
    game_over = False                     # 游戏是否结束
    game_started = False                  # 是否已经开始（第一次按键）
    result = False                        # 游戏结果，默认失败

    # 绘制游戏界面（小偷、警察、输入信息）
    def draw():
        screen.fill(WHITE)  # 清屏
        # 画小偷（蓝色圆圈）
        pygame.draw.circle(screen, BLUE, (thief["x"], thief["y"]), 20)
        # 画警察（红色圆圈）
        pygame.draw.circle(screen, RED, (police["x"], police["y"]), 20)

        # 比较当前输入是否匹配目标单词的前缀
        correct_part = input_text["correct_word"][:len(input_text["current"])]
        color = GREEN if input_text["current"] == correct_part else RED

        # 渲染输入内容
        input_surface = font.render("Input: " + input_text["current"], True, color)
        # 渲染目标单词
        target_surface = font.render("Target: " + input_text["correct_word"], True, BLACK)

        # 显示到屏幕上
        screen.blit(input_surface, (50, 300))
        screen.blit(target_surface, (50, 340))

    # 检查输入正确后更新游戏状态（小偷移动、切换目标单词）
    def check_typing():
        nonlocal input_text, thief
        # 第一次输入时记录开始时间
        if input_text["start_time"] is None:
            input_text["start_time"] = time.time()
        elapsed = time.time() - input_text["start_time"]
        if elapsed == 0: elapsed = 0.001  # 避免除以0
        speed = len(input_text["correct_word"]) / elapsed * 60  # 计算每分钟输入字符数
        # 根据速度决定小偷的前进距离
        move_dist = thief["speed"] * (5 if speed >= 30 else 2)
        thief["x"] += move_dist

        # 重置输入状态，并随机生成下一个单词
        input_text["current"] = ""
        input_text["start_time"] = None
        input_text["correct_word"] = random.choice(word_list)

    # 主循环
    while True:
        # 处理事件（键盘输入、退出等）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 用户关闭窗口
                game_over = True
                result = False
                break
            elif event.type == pygame.KEYDOWN:
                if not game_started:
                    game_started = True  # 任意键开始游戏

                if event.key == pygame.K_BACKSPACE:
                    input_text["current"] = input_text["current"][:-1]  # 删除一个字符
                elif event.key == pygame.K_RETURN:
                    # 如果输入正确，调用 check_typing() 更新状态
                    if input_text["current"] == input_text["correct_word"]:
                        if input_text["start_time"] is None:
                            input_text["start_time"] = time.time()
                        check_typing()
                elif event.unicode.isprintable():
                    # 处理普通字符输入
                    input_text["current"] += event.unicode

        # 如果游戏还没结束，更新警察位置和判断输赢
        if not game_over:
            if police["x"] < thief["x"]:
                police["x"] += police["speed"]  # 警察追小偷

            # 判断是否被追上
            if police["x"] >= thief["x"] - 20:
                game_over = True
                result = False
                message = "Game Over!"  # 失败
            # 判断是否成功逃脱
            elif thief["x"] >= WIDTH - 50:
                game_over = True
                result = True
                message = "You Win!"  # 成功

        # 绘制界面
        draw()

        # 游戏结束时显示胜负信息
        if game_over:
            color = RED if not result else GREEN
            msg_surf = font.render(message, True, color)
            screen.blit(msg_surf, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            break  # 跳出主循环

        pygame.display.update()
        clock.tick(30)  # 控制帧率

    # 游戏结束界面
    screen.fill(WHITE)
    finish_text = font.render("Game Finished!", True, BLACK)
    screen.blit(finish_text, finish_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()

    return result  # 返回游戏结果（True 胜利，False 失败）



import pygame

def run_quiz_game():
    """问答小游戏：全部答对返回 True，窗口关闭返回 False"""
    import pygame
    print("DEBUG: Entering run_quiz_game")
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Quiz Game")
    clock = pygame.time.Clock()

    WHITE, BLACK, RED = (255,255,255), (0,0,0), (255,0,0)
    font = pygame.font.Font(None, 40)
    big  = pygame.font.Font(None, 60)

    questions = [
        {"q":"2 + 2 = ?", "a":"4"},
        {"q":"Sky color?", "a":"blue"},
        {"q":"Cat has how many legs?", "a":"4"},
    ]

    mode = "start"            # start / ask
    idx  = 0
    answer = ""
    running = True

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); return False
            if mode == "start" and e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                mode = "ask"; idx = 0; answer = ""
            elif mode == "ask" and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    answer = answer[:-1]
                elif e.key == pygame.K_RETURN:
                    if answer.strip().lower() == questions[idx]["a"]:
                        idx += 1; answer = ""
                        if idx >= len(questions):
                            mode = "done"; break
                    else:
                        mode = "start"    # 重来
                elif e.unicode.isprintable():
                    answer += e.unicode

        # 如果已经完成，跳出主循环去显示完成界面
        if mode == "done":
            break

        # ---- 绘制 -------------------------------------------------------
        screen.fill(WHITE)
        if mode == "start":
            txt = big.render("Press any key to start", True, BLACK)
            screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2)))
        elif mode == "ask":
            q = questions[idx]["q"]
            q_s = font.render(q, True, BLACK)
            a_s = font.render("Answer: " + answer, True, BLACK)
            screen.blit(q_s, (100, 200))
            screen.blit(a_s, (100, 260))
        pygame.display.flip()
        clock.tick(30)

    # ------ 完成界面，等待任意键 -------------------------------------------
    screen.fill(WHITE)
    done_txt = big.render("Quiz Completed!", True, BLACK)
    screen.blit(done_txt, done_txt.get_rect(center=(WIDTH//2, HEIGHT//2)))
    pygame.display.flip()
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); return False
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False
        clock.tick(10)
    pygame.quit(); return True


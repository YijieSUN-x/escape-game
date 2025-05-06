import pygame
import time
import random

def run_escape_game():
    pygame.init()
    WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escape Game")
    clock = pygame.time.Clock()

    # Colors and game objects
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE  = (0, 0, 255)

    thief = {"x": 300, "y": 200, "speed": 5}
    police = {"x": 50, "y": 200, "speed": 0.5}
    input_text = {"current": "", "correct_word": "escape", "start_time": None}
    word_list = ["escape", "run", "freedom", "hide"]

    font = pygame.font.Font(None, 36)
    game_over = False
    game_started = False
    result = False  # 默认失败

    def draw():
        screen.fill(WHITE)
        pygame.draw.circle(screen, BLUE, (thief["x"], thief["y"]), 20)
        pygame.draw.circle(screen, RED, (police["x"], police["y"]), 20)
        correct_part = input_text["correct_word"][:len(input_text["current"])]
        color = GREEN if input_text["current"] == correct_part else RED
        input_surface = font.render("Input: " + input_text["current"], True, color)
        target_surface = font.render("Target: " + input_text["correct_word"], True, BLACK)
        screen.blit(input_surface, (50, 300))
        screen.blit(target_surface, (50, 340))

    def check_typing():
        nonlocal input_text, thief
        if input_text["start_time"] is None:
            input_text["start_time"] = time.time()
        elapsed = time.time() - input_text["start_time"]
        if elapsed == 0: elapsed = 0.001
        speed = len(input_text["correct_word"]) / elapsed * 60
        move_dist = thief["speed"] * (5 if speed >= 30 else 2)
        thief["x"] += move_dist
        input_text["current"] = ""
        input_text["start_time"] = None
        input_text["correct_word"] = random.choice(word_list)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                result = False
                break
            elif event.type == pygame.KEYDOWN:
                if not game_started:
                    game_started = True
                if event.key == pygame.K_BACKSPACE:
                    input_text["current"] = input_text["current"][:-1]
                elif event.key == pygame.K_RETURN:
                    if input_text["current"] == input_text["correct_word"]:
                        if input_text["start_time"] is None:
                            input_text["start_time"] = time.time()
                        check_typing()
                elif event.unicode.isprintable():
                    input_text["current"] += event.unicode

        if not game_over:
            if police["x"] < thief["x"]:
                police["x"] += police["speed"]
            if police["x"] >= thief["x"] - 20:
                game_over = True
                result = False
                message = "Game Over!"
            elif thief["x"] >= WIDTH - 50:
                game_over = True
                result = True
                message = "You Win!"
                

        draw()
        if game_over:
            # 显示结算
            color = RED if not result else GREEN
            msg_surf = font.render(message, True, color)
            screen.blit(msg_surf, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            break

        pygame.display.update()
        clock.tick(30)

    screen.fill(WHITE)
    finish_text = font.render("Game Finished!", True, BLACK)
    screen.blit(finish_text, finish_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    return result


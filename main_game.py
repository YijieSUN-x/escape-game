# main_game.py

import time
import pygame
import os
import json
from game1 import run_quiz_game
from game2 import run_cat_police_game
from game3 import run_escape_game

# ---------- Utility Functions ----------

def ensure_screen():
    """
    Ensure pygame is initialized and return a valid screen surface.
    Re-inits if a sub-game called pygame.quit().
    """
    if not pygame.get_init():
        pygame.init()
    if not pygame.font.get_init():
        pygame.font.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Midnight Phantom")
    return screen

def show_transition(screen, title, description, duration=3000, image_name=None):
    """
    Display a transition scene with title, multiline description,
    optional image (scaled to 200×200), for `duration` milliseconds.
    Image is looked up relative to this script's directory.
    """
    screen.fill((0, 0, 0))
    font_title = pygame.font.SysFont(None, 48)
    font_text  = pygame.font.SysFont(None, 32)

    # Render title
    title_surf = font_title.render(title, True, (255, 215, 0))
    screen.blit(title_surf, ((800 - title_surf.get_width()) // 2, 80))

    # Render description lines
    for i, line in enumerate(description.split("\n")):
        text_surf = font_text.render(line, True, (255, 255, 255))
        screen.blit(text_surf, ((800 - text_surf.get_width()) // 2, 160 + i * 40))

   
    pygame.display.flip()
    pygame.time.delay(duration)

def get_player_name(screen, font, prompt):
    """
    Show `prompt` and collect text input in pygame window.
    Return entered name when Enter is pressed.
    """
    name = ""
    clock = pygame.time.Clock()
    pygame.event.clear()
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                return name.strip()
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == pygame.K_RETURN:
                    return name.strip()
                elif evt.unicode.isprintable():
                    name += evt.unicode

        screen.fill((0, 0, 0))
        prompt_surf = font.render(prompt, True, (255, 215, 0))
        name_surf   = font.render(name,   True, (255, 255, 255))
        screen.blit(prompt_surf, ((800 - prompt_surf.get_width()) // 2, 200))
        screen.blit(name_surf,   ((800 - name_surf.get_width())   // 2, 260))
        pygame.display.flip()
        clock.tick(30)

# ---------- Main Program ----------

def main():
    # Prologue transition (no image)
    screen = ensure_screen()
    show_transition(
        screen,
        "Prologue",
        "In the hush of night, a meticulously planned heist unfolds.\n"
        "Your mission: infiltrate billionaire Aldridge’s estate and seize the\n"
        "bonds hidden in his underground vault—assets powerful enough to shake\n"
        "the financial world.",
        duration=6000
    )

    total_start = time.time()

    # Run through the three stages
    while True:
        # Stage 1 transition + vault.png
        screen = ensure_screen()
        show_transition(
            screen,
            "Stage 1: Vault Breach",
            "You approach the mansion’s back door.\n"
            "Hack the security system and override the locks\n"
            "to access the underground vault.",
            duration=4000,
            image_name="vault.png"
        )
        if not run_quiz_game():
            continue

        # Stage 2 transition + guards.png
        screen = ensure_screen()
        show_transition(
            screen,
            "Stage 2: Guard Chase",
            "Silent alarm triggered!\n"
            "Armed guards are sweeping the grounds.\n"
            "Evade them and escape the estate.",
            duration=4000,
            image_name="guards.png"
        )
        if not run_cat_police_game():
            continue

        # Stage 3 transition + car_chase.png
        screen = ensure_screen()
        show_transition(
            screen,
            "Stage 3: Highway Pursuit",
            "You’ve hijacked a supercar!\n"
            "Police are in hot pursuit on the highway.\n"
            "Outrun them and disappear into the night.",
            duration=4000,
            image_name="car_chase.png"
        )
        if not run_escape_game():
            continue

        break  # all stages complete

    # Calculate total time
    total_elapsed = time.time() - total_start

    # Load or initialize leaderboard
    lb_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.json")
    if os.path.exists(lb_file):
        with open(lb_file, "r", encoding="utf-8") as f:
            leaderboard = json.load(f)
    else:
        leaderboard = []

    # Prompt for player name
    screen = ensure_screen()
    font_entry = pygame.font.SysFont(None, 36)
    name = get_player_name(screen, font_entry, "Enter your name for the leaderboard:")
    if not name:
        name = "Player"

    # Append and sort
    leaderboard.append({"name": name, "time": total_elapsed})
    leaderboard.sort(key=lambda x: x["time"])
    with open(lb_file, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=2)

    # Display top 5 leaderboard
    screen = ensure_screen()
    font_title = pygame.font.SysFont(None, 48)
    font_entry = pygame.font.SysFont(None, 36)
    screen.fill((0, 0, 0))

    msg_surf = font_title.render(
        f"Congratulations, {name}! Total time: {total_elapsed:.2f}s",
        True, (255, 255, 255)
    )
    screen.blit(msg_surf, ((800 - msg_surf.get_width()) // 2, 40))

    lb_title = font_title.render("Leaderboard (Top 5)", True, (255, 215, 0))
    screen.blit(lb_title, ((800 - lb_title.get_width()) // 2, 100))

    ords = ["1st", "2nd", "3rd", "4th", "5th"]
    for i, entry in enumerate(leaderboard[:5]):
        line = font_entry.render(
            f"{ords[i]}. {entry['name']} - {entry['time']:.2f}s",
            True, (255, 255, 255)
        )
        screen.blit(line, ((800 - line.get_width()) // 2, 160 + i * 40))

    pygame.display.flip()

    # Wait for exit
    while True:
        for ev in pygame.event.get():
            if ev.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                pygame.quit()
                return

if __name__ == "__main__":
    main()


# game2.py  —— “猫逃跑”小游戏，可被 main_game.py 调用
import pygame, math, sys
from collections import deque

GRID_SIZE, CELL_SIZE, MARGIN = 7, 40, 20
WIDTH, HEIGHT = 800, 600
EMPTY, OBSTACLE, CAT = 0, 1, 2


# ── 几何与工具 ───────────────────────────────────────────────────────────────
def hex_corner(center, size, i):
    ang = math.radians(60 * i - 30)
    return center[0] + size*math.cos(ang), center[1] + size*math.sin(ang)

def hex_center(r, c):
    return (CELL_SIZE*1.5*c + MARGIN,
            CELL_SIZE*math.sqrt(3)*(r + .5*(c&1)) + MARGIN)

def neighbours(r, c):
    even = [(-1,0),(-1,1),(0,-1),(0,1),(1,0),(1,1)]
    odd  = [(-1,-1),(-1,0),(0,-1),(0,1),(1,-1),(1,0)]
    dirs = even if r%2==0 else odd
    return [(r+dr, c+dc) for dr,dc in dirs
            if 0<=r+dr<GRID_SIZE and 0<=c+dc<GRID_SIZE]

def at_edge(rc): return rc[0] in (0,GRID_SIZE-1) or rc[1] in (0,GRID_SIZE-1)


# ── AI：给猫最短路的下一个格子加墙 ────────────────────────────────────────────
def bfs_path(grid, start):
    q, par, seen = deque([start]), {}, {start}
    while q:
        cur = q.popleft()
        if at_edge(cur):                      # 抵达边缘
            path = [cur]
            while cur in par:
                cur = par[cur]; path.append(cur)
            return list(reversed(path))
        for nb in neighbours(*cur):
            if nb not in seen and grid[nb[0]][nb[1]] == EMPTY:
                seen.add(nb); par[nb] = cur; q.append(nb)
    return None                               # 被围死

def ai_put_wall(grid, cat):
    path = bfs_path(grid, tuple(cat))
    if path and len(path) > 1:
        x,y = path[1]; grid[x][y] = OBSTACLE


# ── *** 对外接口：被主程序调用 *** ─────────────────────────────────────────────
def run_cat_police_game():
    """
    猫逃跑小游戏：
        返回 True  -> 猫成功触碰到棋盘边缘（玩家胜）
        返回 False -> 猫被围住 或 用户关窗口（玩家败）
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chat en Fuite avec Police AI")
    clock, font = pygame.time.Clock(), pygame.font.SysFont(None, 36)

    # 初始化棋盘
    grid = [[EMPTY]*GRID_SIZE for _ in range(GRID_SIZE)]
    cat = [GRID_SIZE//2]*2
    grid[cat[0]][cat[1]] = CAT
    game_over = win = False

    def draw_board():
        screen.fill((255,255,255))
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                val = grid[r][c]
                col = (230,230,230) if val==EMPTY else (100,100,100) if val==OBSTACLE else (255,165,0)
                ctr = hex_center(r,c)
                pts = [hex_corner(ctr, CELL_SIZE, i) for i in range(6)]
                pygame.draw.polygon(screen, col, pts)
                pygame.draw.polygon(screen, (0,0,0), pts, 2)

    def wait_any(msg):
        txt = font.render(msg, True, (200,0,0))
        rect = txt.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(txt, rect); pygame.display.flip()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); return None
                if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN): return

    while True:
        draw_board(); pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); return False
            if ev.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mx,my = ev.pos
                # 找最近格子（简单够用）
                click = min(((r,c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)),
                            key=lambda rc: (hex_center(*rc)[0]-mx)**2 + (hex_center(*rc)[1]-my)**2)
                if click in neighbours(*cat) and grid[click[0]][click[1]] == EMPTY:
                    grid[cat[0]][cat[1]] = EMPTY
                    cat[:] = click; grid[cat[0]][cat[1]] = CAT
                    if at_edge(cat): game_over = win = True
                    else:
                        ai_put_wall(grid, cat)
                        if not any(grid[nx][ny]==EMPTY for nx,ny in neighbours(*cat)):
                            game_over = win = False

        if game_over:
            wait_any("Victoire!" if win else "Échec!")
            pygame.quit(); return win

        clock.tick(30)


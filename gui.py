import pygame
import sys
import math
import copy
import time

from mancala import MancalaBoard, Game, Play

pygame.init()
WIDTH, HEIGHT = 980, 520
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pink Mancala")

# Colors
BLUE_LIGHT = (230, 245, 255)
BLUE_ACCENT = (190, 225, 255)
BLUE_SOFT = (210, 235, 250)
BG = BLUE_LIGHT
PINK_DARK = (219, 112, 147)
PINK_MED = (255, 105, 180)
PINK_LIGHT = (255, 192, 203)
PINK2 = (255, 160, 190)
ACCENT = BLUE_SOFT
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)

FONT = pygame.font.SysFont("arial", 22)
BIGFONT = pygame.font.SysFont("arial", 36)
SMALL = pygame.font.SysFont("arial", 18)

FPS = 30
CLOCK = pygame.time.Clock()

# Layout
PIT_RADIUS = 36
pit_positions = {
    "A": (220, 370), "B": (320, 370), "C": (420, 370), "D": (520, 370), "E": (620, 370), "F": (720, 370),
    "L": (220, 120), "K": (320, 120), "J": (420, 120), "I": (520, 120), "H": (620, 120), "G": (720, 120),
}
store_positions = {"S1": (80, 240), "S2": (880, 240)}

def draw_button(text, rect, base_color, hover_color, mouse_pos, text_color=WHITE):
    x, y, w, h = rect
    hovered = x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h
    color = hover_color if hovered else base_color
    pygame.draw.rect(WIN, color, rect, border_radius=12)
    label = FONT.render(text, True, text_color)
    WIN.blit(label, (x + w//2 - label.get_width()//2, y + h//2 - label.get_height()//2))
    return hovered

def center_text(text, y, font=BIGFONT, color=PINK_DARK):
    label = font.render(text, True, color)
    WIN.blit(label, (WIDTH//2 - label.get_width()//2, y))

def draw_board(board: MancalaBoard, highlight_moves=None):
    if highlight_moves is None:
        highlight_moves = []
    WIN.fill(BG)

    # Stores
    pygame.draw.rect(WIN, BLUE_ACCENT, (30, 90, 100, 300), border_radius=18)
    pygame.draw.rect(WIN, BLUE_ACCENT, (850, 90, 100, 300), border_radius=18)

    # Store counts
    s1 = FONT.render(str(board.board["S1"]), True, WHITE)
    s2 = FONT.render(str(board.board["S2"]), True, WHITE)
    WIN.blit(s1, (store_positions["S1"][0] - s1.get_width()//2, store_positions["S1"][1] - s1.get_height()//2))
    WIN.blit(s2, (store_positions["S2"][0] - s2.get_width()//2, store_positions["S2"][1] - s2.get_height()//2))

    # Pits
    for pit, pos in pit_positions.items():
        if pit in highlight_moves:
            pygame.draw.circle(WIN, ACCENT, pos, PIT_RADIUS + 6)
        pygame.draw.circle(WIN, PINK_MED, pos, PIT_RADIUS)
        pygame.draw.circle(WIN, PINK_LIGHT, pos, PIT_RADIUS - 6)

        seeds = board.board[pit]
        txt = FONT.render(str(seeds), True, BLACK)
        WIN.blit(txt, (pos[0] - txt.get_width()//2, pos[1] - txt.get_height()//2))

    # Labels
    center_text("Player 2 side (G-L)", 60, FONT, PINK_DARK)
    center_text("Player 1 side (A-F)", 440, FONT, PINK_DARK)

def pit_at_pos(mouse_pos):
    x, y = mouse_pos
    for pit, center in pit_positions.items():
        cx, cy = center
        if (x - cx)**2 + (y - cy)**2 <= PIT_RADIUS**2:
            return pit
    return None

try:
    BOW_IMG = pygame.image.load("bow.png").convert_alpha()
    BOW_IMG = pygame.transform.smoothscale(BOW_IMG, (32, 32))
except:
    BOW_IMG = None

def main_menu():
    while True:
        CLOCK.tick(FPS)
        mouse = pygame.mouse.get_pos()
        WIN.fill(BG)
        title = BIGFONT.render("Pink Mancala", True, PINK_DARK)
        WIN.blit(title, (WIDTH//2 - title.get_width()//2 - 20, 10))
        if BOW_IMG:
            WIN.blit(BOW_IMG, (WIDTH//2 + title.get_width()//2 - 10, 12))

        btn_w, btn_h = 360, 60
        bx = WIDTH//2 - btn_w//2
        b1 = (bx, 180, btn_w, btn_h)
        b2 = (bx, 260, btn_w, btn_h)
        b3 = (bx, 340, btn_w, btn_h)

        hovered1 = draw_button("Human vs Computer (H1)", b1, PINK2, PINK_DARK, mouse)
        hovered2 = draw_button("Computer vs Computer (H1 vs H2)", b2, PINK2, PINK_DARK, mouse)
        hovered3 = draw_button("Exit", b3, PINK2, PINK_DARK, mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hovered1:
                    configure_hvc()
                elif hovered2:
                    configure_cvc()
                elif hovered3:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def configure_hvc():
    # Step 1: choose side
    chosen_side = None
    while chosen_side is None:
        CLOCK.tick(FPS)
        mouse = pygame.mouse.get_pos()
        WIN.fill(BG)
        center_text("Choose your side", 30)
        center_text("Player 1 (A-F) moves first", 80, SMALL, PINK_DARK)

        bx = WIDTH//2 - 140
        b1 = (bx, 160, 280, 70)
        b2 = (bx, 250, 280, 70)
        hovered1 = draw_button("Play as Player 1 (A-F)", b1, PINK2, PINK_DARK, mouse)
        hovered2 = draw_button("Play as Player 2 (G-L)", b2, PINK2, PINK_DARK, mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hovered1:
                    chosen_side = 1
                elif hovered2:
                    chosen_side = 2
        pygame.display.update()

    # Step 2: choose depth
    chosen_depth = None
    depths = [3,4,5,6,7,8,9,10]
    btns = []
    start_x = WIDTH//2 - (len(depths)*60)//2 - 10
    y = 220
    for i,d in enumerate(depths):
        btns.append((start_x + i*60, y, 52, 44, d))

    while chosen_depth is None:
        CLOCK.tick(FPS)
        mouse = pygame.mouse.get_pos()
        WIN.fill(BG)
        center_text("Choose search depth for COMPUTER", 40)
        center_text("(Computer will use H1 heuristic)", 75, SMALL, PINK_DARK)
        center_text("Depth controls AI lookahead - recommended 4-7", 105, SMALL, PINK_DARK)

        for rect in btns:
            x,y_pos,w,h,d = rect
            hovered = draw_button(str(d), (x,y_pos,w,h), PINK2, PINK_DARK, mouse)
            if hovered and pygame.mouse.get_pressed(num_buttons=3)[0]:
                chosen_depth = d

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        pygame.display.update()

    run_hvc_game(human_side=chosen_side, comp_depth=chosen_depth)

def run_hvc_game(human_side: int, comp_depth: int):
    # Computer uses H1 in Human vs Computer mode
    play = Play(human_side=human_side, heuristic="H1")
    game = play.game
    turn_side = 1

    running = True
    while running:
        CLOCK.tick(FPS)
        
        # Check game over BEFORE drawing
        if game.gameOver():
            winner, diff = game.findWinner(is_cvc_mode=False)
            show_result_screen(game.state, winner, diff, "Human vs Computer (H1)")
            return

        # Draw board with highlights if it's human's turn
        if turn_side == game.playerSide[-1]:
            draw_board(game.state, highlight_moves=game.state.possibleMoves(human_side))
        else:
            draw_board(game.state)
        
        # Info text
        info = f"Human is {'Player 1 (A-F)' if human_side==1 else 'Player 2 (G-L)'} | Computer depth: {comp_depth} (H1)"
        center_text(info, 8, SMALL, PINK_DARK)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if turn_side == game.playerSide[-1]:
                # Human turn
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = pit_at_pos(event.pos)
                    if clicked and clicked in game.state.possibleMoves(human_side):
                        game.state.doMove(human_side, clicked)
                        turn_side = 1 if turn_side == 2 else 2
            else:
                # Computer turn - execute once
                pygame.time.delay(220)
                side = game.playerSide[1]
                other_side = 1 if side == 2 else 2
                temp_board = copy.deepcopy(game.state)
                temp_game = Game(temp_board, human_side=other_side, heuristic="H1")
                val, pit = play.MinimaxAlphaBetaPruning(temp_game, 1, comp_depth, -math.inf, math.inf)
                
                moves = game.state.possibleMoves(side)
                if not moves:
                    turn_side = 1 if turn_side == 2 else 2
                    continue
                if pit is None:
                    pit = moves[0]
                game.state.doMove(side, pit)
                turn_side = 1 if turn_side == 2 else 2

def configure_cvc():
    # Step 1: depth for Player 1
    depth1 = None
    depth_options = [3,4,5,6,7,8,9,10]
    while depth1 is None:
        CLOCK.tick(FPS)
        mouse = pygame.mouse.get_pos()
        WIN.fill(BG)
        center_text("Computer vs Computer - Configure", 20)
        center_text("Choose depth for Computer 1 (Player 1 / A-F, uses H1)", 60, SMALL, PINK_DARK)

        start_x = WIDTH//2 - (len(depth_options)*60)//2 - 10
        y = 140
        for i,d in enumerate(depth_options):
            rect = (start_x + i*60, y, 52, 44)
            hovered = draw_button(str(d), rect, PINK2, PINK_DARK, mouse)
            if hovered and pygame.mouse.get_pressed(num_buttons=3)[0]:
                depth1 = d

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        pygame.display.update()

    # Step 2: depth for Player 2
    depth2 = None
    while depth2 is None:
        CLOCK.tick(FPS)
        mouse = pygame.mouse.get_pos()
        WIN.fill(BG)
        center_text("Computer vs Computer - Configure", 20)
        center_text("Choose depth for Computer 2 (Player 2 / G-L, uses H2)", 60, SMALL, PINK_DARK)

        start_x = WIDTH//2 - (len(depth_options)*60)//2 - 10
        y = 140
        for i,d in enumerate(depth_options):
            rect = (start_x + i*60, y, 52, 44)
            hovered = draw_button(str(d), rect, PINK2, PINK_DARK, mouse)
            if hovered and pygame.mouse.get_pressed(num_buttons=3)[0]:
                depth2 = d

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        pygame.display.update()

    # Step 3: delay
    delay = None
    buffer = ""
    while delay is None:
        CLOCK.tick(FPS)
        mouse = pygame.mouse.get_pos()
        WIN.fill(BG)
        center_text("Computer vs Computer - Configure", 20)
        center_text("Enter delay between moves (seconds). Example: 0.3", 60, SMALL, PINK_DARK)

        label = FONT.render("Delay (sec): " + (buffer if buffer != "" else "0.5"), True, PINK_DARK)
        WIN.blit(label, (WIDTH//2 - label.get_width()//2, 160))
        center_text("Press Backspace to clear, Enter to confirm", 220, SMALL, PINK_DARK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        if buffer.strip() == "":
                            delay = 0.5
                        else:
                            v = float(buffer)
                            if v < 0: v = 0.0
                            delay = v
                    except:
                        buffer = ""
                elif event.key == pygame.K_BACKSPACE:
                    buffer = buffer[:-1]
                else:
                    ch = event.unicode
                    if ch.isdigit() or (ch == '.' and '.' not in buffer):
                        buffer += ch
        pygame.display.update()

    run_cvc_game(depth1=depth1, depth2=depth2, delay=delay)

def run_cvc_game(depth1: int, depth2: int, delay: float):
    # Computer1 uses H1, Computer2 uses H2
    play = Play(human_side=1, heuristic="H1")
    game = play.game
    board = game.state
    turn_side = 1

    while True:
        CLOCK.tick(FPS)
        
        # Check game over BEFORE drawing
        if game.gameOver():
            winner, diff = game.findWinner(is_cvc_mode=True)
            show_result_screen(board, winner, diff, f"CvC: P1(H1,d={depth1}) vs P2(H2,d={depth2})")
            return

        # Draw board
        draw_board(board)
        info = f"CvC: P1(H1, depth={depth1}) vs P2(H2, depth={depth2}) | Delay={delay}s"
        center_text(info, 10, SMALL, PINK_DARK)
        pygame.display.update()

        # Determine side and heuristic
        if turn_side == 1:
            depth = depth1
            side = 1
            heuristic = "H1"
        else:
            depth = depth2
            side = 2
            heuristic = "H2"

        # Create temp game with appropriate heuristic
        other_side = 1 if side == 2 else 2
        temp_board = copy.deepcopy(board)
        temp_game = Game(temp_board, human_side=other_side, heuristic=heuristic)
        val, pit = play.MinimaxAlphaBetaPruning(temp_game, 1, depth, -math.inf, math.inf)

        moves = board.possibleMoves(side)
        if not moves:
            turn_side = 1 if turn_side == 2 else 2
            continue

        if pit is None:
            pit = moves[0]

        # Perform move
        board.doMove(side, pit)
        
        # Redraw after move
        draw_board(board)
        center_text(info, 10, SMALL, PINK_DARK)
        pygame.display.update()

        # Wait
        wait_ms = int(max(0, delay) * 1000)
        pygame.time.delay(wait_ms)

        turn_side = 1 if turn_side == 2 else 2

def show_result_screen(board: MancalaBoard, winner: str, diff: int, mode_info: str):
    """
    Fixed result screen - no more flickering
    """
    # Create a static surface with the final board once
    final_surface = pygame.Surface((WIDTH, HEIGHT))
    final_surface.fill(BG)
    
    # Draw stores on final surface
    pygame.draw.rect(final_surface, BLUE_ACCENT, (30, 90, 100, 300), border_radius=18)
    pygame.draw.rect(final_surface, BLUE_ACCENT, (850, 90, 100, 300), border_radius=18)
    
    s1 = FONT.render(str(board.board["S1"]), True, WHITE)
    s2 = FONT.render(str(board.board["S2"]), True, WHITE)
    final_surface.blit(s1, (store_positions["S1"][0] - s1.get_width()//2, store_positions["S1"][1] - s1.get_height()//2))
    final_surface.blit(s2, (store_positions["S2"][0] - s2.get_width()//2, store_positions["S2"][1] - s2.get_height()//2))
    
    # Draw pits on final surface
    for pit, pos in pit_positions.items():
        pygame.draw.circle(final_surface, PINK_MED, pos, PIT_RADIUS)
        pygame.draw.circle(final_surface, PINK_LIGHT, pos, PIT_RADIUS - 6)
        seeds = board.board[pit]
        txt = FONT.render(str(seeds), True, BLACK)
        final_surface.blit(txt, (pos[0] - txt.get_width()//2, pos[1] - txt.get_height()//2))
    
    # Labels
    label1 = FONT.render("Player 2 side (G-L)", True, PINK_DARK)
    final_surface.blit(label1, (WIDTH//2 - label1.get_width()//2, 60))
    label2 = FONT.render("Player 1 side (A-F)", True, PINK_DARK)
    final_surface.blit(label2, (WIDTH//2 - label2.get_width()//2, 440))
    
    # Overlay box
    overlay_rect = pygame.Rect(200, 150, 580, 220)
    pygame.draw.rect(final_surface, BG, overlay_rect, border_radius=14)
    pygame.draw.rect(final_surface, PINK_DARK, overlay_rect, 3, border_radius=14)
    
    # Game over text
    title_label = BIGFONT.render("Game Over", True, PINK_DARK)
    final_surface.blit(title_label, (WIDTH//2 - title_label.get_width()//2, 165))
    
    # Winner text
    if winner is None:
        msg = "It's a tie!"
    else:
        msg = f"Winner: {winner} (score difference: {diff})"
    winner_label = FONT.render(msg, True, PINK_DARK)
    final_surface.blit(winner_label, (WIDTH//2 - winner_label.get_width()//2, 210))
    
    # Mode info
    mode_label = SMALL.render(mode_info, True, PINK_DARK)
    final_surface.blit(mode_label, (WIDTH//2 - mode_label.get_width()//2, 250))
    
    # Now just display this static surface and handle the button
    while True:
        CLOCK.tick(FPS)
        mouse = pygame.mouse.get_pos()
        
        # Blit the static surface
        WIN.blit(final_surface, (0, 0))
        
        # Draw button on top
        btn = (WIDTH//2 - 120, 290, 240, 56)
        hovered = draw_button("Return to Menu", btn, PINK2, PINK_DARK, mouse)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hovered:
                    return
        
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
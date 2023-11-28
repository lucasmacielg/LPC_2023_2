import sys
import pygame
from back import main
from back import not_robot_playing
from back import robot_playing
from button import Button

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (237, 233, 255)
BLUE = (25, 140, 255)

WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

BG = pygame.image.load("assets/Background.jpeg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
OP = pygame.image.load("assets/Options.jpeg")
OP = pygame.transform.scale(OP, (725, 300))
surface = pygame.display.set_mode((WIDTH, HEIGHT))

volume = 0.3
select = pygame.mixer.Sound('assets/select.wav')
select.set_volume(volume)

def get_font_players(size):
    return pygame.font.Font("assets/font_player.TTF", size)

def get_font_button(size):
    return pygame.font.Font("assets/font.ttf", size)
def get_font_play(size):
    return pygame.font.Font("assets/font_arcade.TTF", size)

def draw_text(surface, font, text, color, rect, max_width):
    words = text.split(' ')
    space_width, _ = font.size(' ')

    lines = []
    current_line = []

    current_width = 0
    word_height = 0
    for word in words:
        word_width, word_height = font.size(word)
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width + space_width
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width + space_width

    lines.append(' '.join(current_line))

    y = rect.y
    for line in lines:
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (rect.x, y))
        y += word_height


def how_to_play():
    original_screen = pygame.display.get_surface()
    how_to_play_screen = pygame.display.set_mode((800, 600))
    how_to_play_screen.fill(WHITE)

    PLAY_TEXT = get_font_players(40).render("HOW TO PLAY?", True, WHITE)
    PLAY_RECT = PLAY_TEXT.get_rect(center=(WIDTH // 3.2, 100))

    RULES_TEXT = get_font_button(30).render("RULES", True, WHITE)
    RULES_RECT = RULES_TEXT.get_rect(center=(WIDTH // 5.9, 160))

    GOAL_TEXT = get_font_button(30).render("GOAL", True, WHITE)
    GOAL_RECT = GOAL_TEXT.get_rect(center=(WIDTH // 2.05, 165))

    background_image = pygame.image.load("assets/How_to_play.jpeg")
    background_image = pygame.transform.scale(background_image, (800, 600))
    how_to_play_screen.blit(background_image, (0, 0))

    font = pygame.font.Font(None, 36)
    INSTRUCTION1_TEXT = "Instruction 1: The game is played by one or two players, each controlling a vertical bar on the opposite side of the screen (control by 'w' and 's' or 'arrow' keys)."
    INSTRUCTION2_TEXT = "Instruction 2: Be careful not to let the ball go past your bar. The player who scores 5 points first wins the game."
    INSTRUCTION3_TEXT = "The objective of Pong is to score points by getting the ball past the opponent's bar."
    INSTRUCTION1_RECT = pygame.Rect(60, 200, 800, 600)
    INSTRUCTION2_RECT = pygame.Rect(60, 370, 800, 600)
    INSTRUCTION3_RECT = pygame.Rect(540, 205, 800, 600)

    draw_text(how_to_play_screen, get_font_button(17), INSTRUCTION1_TEXT, WHITE, INSTRUCTION1_RECT, 350)
    draw_text(how_to_play_screen, get_font_button(17), INSTRUCTION2_TEXT, WHITE, INSTRUCTION2_RECT, 350)
    draw_text(how_to_play_screen, get_font_button(17), INSTRUCTION3_TEXT, WHITE, INSTRUCTION3_RECT, 220)


    SCREEN.blit(PLAY_TEXT, PLAY_RECT)
    SCREEN.blit(RULES_TEXT, RULES_RECT)
    SCREEN.blit(GOAL_TEXT, GOAL_RECT)

    back_button = Button(image=None, pos=(150, 555),
                         text_input="Back", font=pygame.font.Font(None, 40), base_color=WHITE,
                         hovering_color=GRAY, border_color=0, border_width=0)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        MOUSE_POS = pygame.mouse.get_pos()

        back_button.changeColor(MOUSE_POS)
        back_button.update(how_to_play_screen, MOUSE_POS)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(MOUSE_POS):
                    pygame.display.set_mode(original_screen.get_size())
                    return

        pygame.display.update()

def play():
    main()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        pygame.mixer.music.pause()
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font_button(100).render("MAIN MENU", True, WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH // 2, 100))

        PONG_TEXT = get_font_button(60).render("PONG GAME", True, WHITE)
        PONG_RECT = PONG_TEXT.get_rect(center=(WIDTH // 2, 658))

        HOW_TO_PLAY = Button(image=None, pos=(WIDTH // 1.16, HEIGHT // 1 - 62),
                             text_input="HOW TO PLAY", font=get_font_button(28), base_color=WHITE,
                             hovering_color=GRAY, border_color=0, border_width=0)

        ONE_PLAYER_BUTTON = Button(image=None, pos=(WIDTH // 2, HEIGHT // 2 - 85),
                                   text_input="ONE PLAYER", font=get_font_players(70), base_color=WHITE,
                                   hovering_color=BLUE, border_color=BLUE, border_width=3)

        TWO_PLAYER_BUTTON = Button(image=None, pos=(WIDTH // 2.01, HEIGHT // 2 + 50),
                                   text_input="TWO PLAYERS", font=get_font_players(63), base_color=WHITE,
                                   hovering_color=BLUE, border_color=BLUE, border_width=3)

        QUIT_BUTTON = Button(image=None, pos=(WIDTH // 7.8, HEIGHT - 60), text_input="QUIT", font=get_font_button(50),
                             base_color=WHITE, hovering_color=GRAY, border_color=0, border_width=0)

        OP_RECT = OP.get_rect(center=(WIDTH // 2, HEIGHT // 2.1))

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(PONG_TEXT, PONG_RECT)
        SCREEN.blit(OP, OP_RECT)

        for button in [ONE_PLAYER_BUTTON, TWO_PLAYER_BUTTON, QUIT_BUTTON, HOW_TO_PLAY]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN, MENU_MOUSE_POS)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ONE_PLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    robot_playing()
                    select.play()
                    pygame.time.delay(200)
                    pygame.mixer.music.load("assets/runaway.wav")
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play()
                    play()
                if TWO_PLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    not_robot_playing()
                    select.play()
                    pygame.time.delay(200)
                    pygame.mixer.music.load("assets/runaway2.wav")
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play()
                    play()
                if HOW_TO_PLAY.checkForInput(MENU_MOUSE_POS):
                    how_to_play()
                    pygame.display.set_mode((WIDTH, HEIGHT))
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    select.play()
                    pygame.time.delay(500)
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    while True:
        main_menu()
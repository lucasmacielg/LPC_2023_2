import pygame
import sys
from button import Button
from back import main
from back import robot_playing
from back import not_robot_playing

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

BG = pygame.image.load("assets/Background.png")
surface = pygame.display.set_mode((WIDTH, HEIGHT))


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def play():
    main()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        pygame.mixer.music.pause()

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        ONE_PLAYER_BUTTON = Button(image=None, pos=(WIDTH // 2, HEIGHT // 2 - 100),
                                   text_input="ONE PLAYER", font=get_font(60), base_color=WHITE,
                                   hovering_color="green")

        TWO_PLAYER_BUTTON = Button(image=None, pos=(WIDTH // 2, HEIGHT // 2 + 50),
                                   text_input="TWO PLAYERS", font=get_font(60), base_color=WHITE,
                                   hovering_color="green")

        QUIT_BUTTON = Button(image=None, pos=(WIDTH // 2, HEIGHT - 100), text_input="QUIT", font=get_font(50),
                             base_color=WHITE, hovering_color="green")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [ONE_PLAYER_BUTTON, TWO_PLAYER_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ONE_PLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    robot_playing()
                    pygame.mixer.music.play()
                    play()
                if TWO_PLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    not_robot_playing()
                    pygame.mixer.music.play()
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
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

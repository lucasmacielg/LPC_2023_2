import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

FPS = 60

PADDLE_WIDTH, PADDLE_HEIGHT = 40, 200
BALL_RADIUS = 17

FONT = pygame.font.Font('assets/PressStart2P.ttf', 70)
WINNING_SCORE = 2


class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 8
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(screen, paddles, ball, left_score, right_score):
    screen.fill(BLACK)

    left_score_text = FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = FONT.render(f"{right_score}", 1, WHITE)
    screen.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    screen.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(screen)

    ball.draw(screen)
    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')

    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                bounce_sound_effect.play()
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                bounce_sound_effect.play()
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel



def movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def restart_game():
    restart = True
    pygame.mixer.music.stop()
    play_again_font = pygame.font.Font('assets/PressStart2P.ttf', 40)
    text_play_again = "PRESS SPACE TO PLAY AGAIN"
    play_again_text = play_again_font.render(text_play_again, 1, WHITE)
    SCREEN.blit(play_again_text,
                (WIDTH // 2 - play_again_text.get_width() // 2, HEIGHT // 2 - play_again_text.get_height()
                 // 2 + 200))
    pygame.display.update()

    while restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                restart = False


def main():
    game_loop = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while game_loop:
        scoring_sound = pygame.mixer.Sound('assets/scoring_music.wav')
        victory_sound = pygame.mixer.Sound('assets/win_music.wav')
        defeat_sound = pygame.mixer.Sound('assets/lose_music.wav')

        clock.tick(FPS)
        draw(SCREEN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                restart_game()
                ball.reset()
                left_paddle.reset()
                right_paddle.reset()
                left_score = 0
                right_score = 0
                pygame.display.update()

        keys = pygame.key.get_pressed()
        movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0 and ball.x_vel < 0:
            right_score += 1
            ball.reset()
            scoring_sound.play()
        elif ball.x > WIDTH and ball.x_vel > 0:
            left_score += 1
            ball.reset()
            scoring_sound.play()

        won = False
        if left_score == WINNING_SCORE:
            won = True
            win_text = "PLAYER 1 WINS!"
        elif right_score == WINNING_SCORE:
            won = True
            win_text = "PLAYER 2 WINS!"

        if won:
            victory_sound.play() if left_score == WINNING_SCORE else defeat_sound.play()
            text = FONT.render(win_text, 1, WHITE)
            SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 100))
            restart_game()


if __name__ == '__main__':
    main()

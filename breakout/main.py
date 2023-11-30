import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255 * 65536 + 165 * 256 + 0)
YELLOW = (255, 255, 0)
PADDLE_COLOR = (142, 135, 123)
TEXT_COLOR = (78, 81, 139)

WIDTH, HEIGHT = 600, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

FPS = 60

PADDLE_WIDTH, PADDLE_HEIGHT = 65, 15
BALL_RADIUS = 8

FONT = pygame.font.Font('assets/font.ttf', 40)
WINNING_SCORE = 336
restart = False

volume = 0.3


class Paddle:
    COLOR = WHITE
    VEL = 5

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
            self.x -= self.VEL
        else:
            self.x += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 11
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = 2
        self.y_vel = self.MAX_VEL

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.radius)

    def set_vel(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel = 0
        self.y_vel *= -1


def draw(screen, paddles, ball, score):
    screen.fill(BLACK)
    score_text = FONT.render(f"{score}", 1, TEXT_COLOR)
    screen.blit(score_text, (WIDTH - 100 - score_text.get_width() // 2, 40))

    for paddle in paddles:
        paddle.draw(screen)

    ball.draw(screen)
    pygame.display.update()


def collision(ball, paddle):
    bounce_sound = pygame.mixer.Sound('assets/bounce.wav')
    bounce_sound.set_volume(volume)
    if ball.x - BALL_RADIUS <= 0 or ball.x + BALL_RADIUS >= WIDTH:
        ball.set_vel(ball.x_vel * -1, ball.y_vel)
        bounce_sound.play()
    if ball.y + BALL_RADIUS >= HEIGHT or ball.y - BALL_RADIUS <= 0:
        ball.set_vel(ball.x_vel, ball.y_vel * -1)
        bounce_sound.play()
    if ball.x - ball.radius >= WIDTH or ball.x + ball.radius <= 0:
        ball.x_vel *= -1
        bounce_sound.play()

    if (paddle.y <= ball.y <= paddle.y + paddle.height and
            paddle.x <= ball.x <= paddle.x + paddle.width):
        ball.y_vel *= -1
        bounce_sound.play()


def movement(keys, paddle):
    if keys[pygame.K_a] and paddle.x - paddle.VEL >= 0:
        paddle.move(up=True)
    if keys[pygame.K_d] and paddle.x + paddle.width + paddle.VEL <= WIDTH:
        paddle.move(up=False)


def restart_game(ball, paddle, score):
    ball.reset()
    paddle.reset()
    score = 000
    return ball, paddle, score


pygame.mixer.music.load("assets/i_wonder.wav")
scoring_sound = pygame.mixer.Sound('assets/point.wav')
victory_sound = pygame.mixer.Sound('assets/win_music.wav')
defeat_sound = pygame.mixer.Sound('assets/lose_music.wav')
pygame.mixer.music.set_volume(0.3)
scoring_sound.set_volume(volume)
victory_sound.set_volume(volume)
defeat_sound.set_volume(volume)


def main():
    game_loop = True
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1)

    paddle = Paddle(WIDTH // 2, HEIGHT - 125, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    won = False
    score = 000
    restart_text_font = pygame.font.Font('assets/font.ttf', 20)
    restart_text = restart_text_font.render("PRESS SPACE TO RESTART", 1, WHITE)

    while game_loop:

        clock.tick(FPS)
        draw(SCREEN, [paddle], ball, score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball, paddle, score = restart_game(
                        ball, paddle, score)

        keys = pygame.key.get_pressed()
        movement(keys, paddle)
        ball.move()
        collision(ball, paddle)

        if ball.x + ball.radius < 0:
            score += 3
            scoring_sound.play()

        win_text = " "
        if score == WINNING_SCORE:
            won = True
            win_text = "YOU WON!"
            victory_sound.play()

        if won:
            pygame.mixer.music.pause()
            SCREEN.fill(BLACK)
            SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 -
                                       restart_text.get_height() // 2 + 200))
            text = FONT.render(win_text, 1, WHITE)
            SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 100))
            won = False
            pygame.display.update()

            space_pressed = False
            while not space_pressed:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_loop = False
                        space_pressed = True
                        pygame.mixer.pause()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            pygame.mixer.pause()
                            pygame.mixer.music.play()
                            ball, paddle, score = restart_game(
                                ball, paddle, score)
                            draw(SCREEN, [paddle], ball, score)
                            pygame.display.update()
                            space_pressed = True


if __name__ == '__main__':
    main()

import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 600, 800
TOP_BLACK_SPACE = 50
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT + TOP_BLACK_SPACE))
pygame.display.set_caption("Breakout Game")

FPS = 60

PADDLE_WIDTH, PADDLE_HEIGHT = 70, 10
BALL_RADIUS = 6

FONT = pygame.font.Font("assets/font.ttf", 40)

WINNING_SCORE = 104
restart = False

volume = 0.3

class Paddle:   
    COLOR = WHITE
    VEL = 8

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, left=True):
        if left:
            self.x -= self.VEL
        else:
            self.x += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    VEL = 3
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = 2
        self.y_vel = self.VEL
        self.rect = pygame.Rect(x - radius, y - radius, 2 * radius, 2 * radius)

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.radius)

    def set_vel(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel = 2
        self.y_vel = self.VEL
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)

    def check_bottom_collision(self):
        return self.y + self.radius > HEIGHT - 15

    def check_paddle_collision(self, paddle):
        if (
            self.y + self.radius > paddle.y and
            self.y - self.radius < paddle.y + paddle.height and
            self.x + self.radius > paddle.x and
            self.x - self.radius < paddle.x + paddle.width
        ):
            self.y_vel *= -1
            self.increase_speed()
            return True
        return False

    def check_brick_collision(self, brick_list):
        for brick in brick_list:
            if self.rect.colliderect(brick.rect):
                self.y_vel *= -1
                brick_list.remove(brick)
                self.increase_speed()
                return True
        return False

    def increase_speed(self):
        self.x_vel = self.x_vel * 1.01
        self.y_vel = self.y_vel * 1.01

class Brick:
    COLORS = [RED, ORANGE, GREEN, YELLOW]

    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x + 15, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def reset(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.color = BLACK

bricks = []

def create_bricks():
    global bricks
    bricks = []
    brick_width = (WIDTH - 81) // 13
    brick_height = 10
    top_offset = 100

    for row in range(8):
        brick_color = Brick.COLORS[row // 2 % len(Brick.COLORS)]
        for col in range(13):
            brick = Brick(col * (brick_width + 5), top_offset + row * (brick_height + 5), brick_width, brick_height, brick_color)
            bricks.append(brick)

def draw_bricks(screen):
    for brick in bricks:
        brick.draw(screen)

def collision(ball, paddle, brick_list, score):
    bounce_sound = pygame.mixer.Sound('assets/bounce.wav')
    bounce_sound.set_volume(volume)

    if ball.check_paddle_collision(paddle):
        if ball.y_vel > 0:
            ball.y_vel *= -1
            ball.y = paddle.y - ball.radius - 1
        bounce_sound.play()

    if ball.x - ball.radius <= 15 or ball.x + ball.radius >= WIDTH - 15:
        ball.set_vel(ball.x_vel * -1, ball.y_vel)
        bounce_sound.play()

    if ball.y + ball.radius >= HEIGHT - 15 or ball.y - ball.radius <= 15:
        ball.set_vel(ball.x_vel, ball.y_vel * -1)
        bounce_sound.play()

    if ball.check_bottom_collision():
        return True, False, score

    if ball.check_brick_collision(brick_list):
        bounce_sound.play()
        score += 1

        if score == WINNING_SCORE:
            return True, True, score

    return False, False, score

def movement(keys, paddle):
    if keys[pygame.K_a] and paddle.x - paddle.VEL >= 0:
        paddle.move(left=True)
    if keys[pygame.K_d] and paddle.x + paddle.width + paddle.VEL <= WIDTH:
        paddle.move(left=False)

def restart_game():
    global bricks, ball, paddle, score
    bricks = []
    create_bricks()
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    paddle = Paddle(WIDTH // 2, HEIGHT - 125, PADDLE_WIDTH, PADDLE_HEIGHT)
    score = 0
    return ball, paddle, bricks, score

scoring_sound = pygame.mixer.Sound('assets/point.wav')
pygame.mixer.music.set_volume(0.3)
scoring_sound.set_volume(volume)


def draw(screen, paddles, ball, score, lost):
    screen.fill(WHITE)

    pygame.draw.rect(screen, BLACK, (15, 15, WIDTH - 30, TOP_BLACK_SPACE + 15))
    pygame.draw.rect(screen, BLACK, (15, TOP_BLACK_SPACE, WIDTH - 30, HEIGHT - 15))

    if not lost:
        score_text = FONT.render(f"{score}", True, WHITE)
        screen.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))
    else:
        score_text = FONT.render(str(score), True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, TOP_BLACK_SPACE + 10))

    draw_bricks(screen)

    for paddle in paddles:
        paddle.draw(screen)

    ball.draw(screen)

    pygame.display.update()

def main():
    global bricks
    game_loop = True
    clock = pygame.time.Clock()
    paddle = Paddle(WIDTH // 2, HEIGHT - 125, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    create_bricks()
    lost = False
    score = 0
    restart_text_font = pygame.font.Font(None, 20)
    restart_text = restart_text_font.render("PRESS SPACE TO RESTART", True, WHITE)

    victory = False

    while game_loop:
        clock.tick(FPS)

        if not lost:
            draw(SCREEN, [paddle], ball, score, lost)       

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_loop = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        ball, paddle, bricks, score = restart_game()

            keys = pygame.key.get_pressed()
            movement(keys, paddle)
            ball.move()

            game_over, victory, score= collision(ball, paddle, bricks, score)

            if game_over:
                pygame.mixer.music.pause()
                SCREEN.fill(BLACK)
                pygame.display.update()
                lost = True

            if victory:
                pygame.mixer.music.pause()
                SCREEN.fill(BLACK)
                win_text = 'YOU WIN!'
                SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - restart_text.get_height() // 2))
                text = FONT.render(win_text, True, WHITE)
                SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 200))
                pygame.display.update()
                pygame.time.delay(3000)
                ball, paddle, bricks, score = restart_game()

            if lost:
                pygame.mixer.music.pause()
                SCREEN.fill(BLACK)
                SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - restart_text.get_height() // 2))
                text = FONT.render("YOU LOST!", True, WHITE)
                SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 200))
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
                                ball, paddle, bricks, score = restart_game()
                                draw(SCREEN, [paddle], ball, score, lost)
                                pygame.display.update()
                                lost = False
                                space_pressed = True

if __name__ == '__main__':
    create_bricks()
    main()

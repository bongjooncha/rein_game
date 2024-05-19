import pygame
import random

# 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arkanoid Clone")

# 패들 클래스 정의
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([100, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH // 2) - 50
        self.rect.y = SCREEN_HEIGHT - 20
        self.speed_x = 0

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

# 공 클래스 정의
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -4

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - self.rect.width:
            self.speed_x *= -1
        if self.rect.y <= 0:
            self.speed_y *= -1
        if self.rect.y >= SCREEN_HEIGHT:
            self.rect.x = SCREEN_WIDTH // 2
            self.rect.y = SCREEN_HEIGHT // 2
            self.speed_y = -4
            return True
        return False

# 블록 클래스 정의
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

def create_blocks():
    blocks = pygame.sprite.Group()
    block_colors = [BLUE, GREEN, RED]
    for row in range(3):
        for column in range(7):
            block = Block(block_colors[row], 100, 30)
            block.rect.x = 60 + column * 110
            block.rect.y = 60 + row * 40
            all_sprites.add(block)
            blocks.add(block)
    return blocks

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# 폰트 초기화
font = pygame.font.Font(None, 36)

# 게임 초기화
def init_game():
    global paddle, ball, all_sprites, blocks, score, lives
    paddle = Paddle()
    ball = Ball()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle)
    all_sprites.add(ball)
    blocks = create_blocks()
    score = 0
    lives = 3

# 초기화면 함수
def show_start_screen():
    screen.fill(BLACK)
    draw_text('Arkanoid Clone', font, WHITE, screen, 300, 250)
    draw_text('Press any key to start', font, WHITE, screen, 280, 300)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# 게임 루프
running = True
clock = pygame.time.Clock()

while running:
    show_start_screen()
    init_game()
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle.speed_x = -6
                elif event.key == pygame.K_RIGHT:
                    paddle.speed_x = 6
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    paddle.speed_x = 0

        all_sprites.update()

        if pygame.sprite.collide_rect(ball, paddle):
            ball.speed_y *= -1

        block_hit_list = pygame.sprite.spritecollide(ball, blocks, True)
        for block in block_hit_list:
            ball.speed_y *= -1
            score += 10

        if ball.update():
            lives -= 1
            if lives == 0:
                game_over = True

        if len(blocks) == 0:
            game_over = True

        screen.fill(BLACK)
        all_sprites.draw(screen)

        # 점수와 목숨 표시
        draw_text(f"Score: {score}", font, WHITE, screen, 10, 10)
        draw_text(f"Lives: {lives}", font, WHITE, screen, SCREEN_WIDTH - 100, 10)

        pygame.display.flip()

        clock.tick(60)

pygame.quit()

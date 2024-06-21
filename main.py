import pygame
from pygame.locals import *
import sys
import random
from player import Player

# Global variables
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
GROUND_HEIGHT = 45
PLAYER_HEIGHT = 50

ACC = 0.5
FRIC = -0.12
FPS = 60
GRAVITY = 0.5

score = 0

pygame.init()
vec = pygame.math.Vector2
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Infinite Runner")

FramePerSec = pygame.time.Clock()

# Ground is a transparent surface that acts as a platform
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        self.rect = self.surface.get_rect(bottomleft = (0, SCREEN_HEIGHT))
        self.image = self.surface

rock_1 = pygame.image.load("assets/rock-1.png").convert_alpha()
rock_1 = pygame.transform.scale(rock_1, (55, 100))
rock_2 = pygame.image.load("assets/rock-2.png").convert_alpha()
rock_2 = pygame.transform.scale(rock_2, (60, 60))
rock_3 = pygame.image.load("assets/rock-3.png").convert_alpha()
rock_3 = pygame.transform.scale(rock_3, (60, 140))
vine = pygame.image.load("assets/vine.png").convert_alpha()
vine_height = SCREEN_HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT - 10
vine = pygame.transform.scale(vine, (30, vine_height))
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        color = (59, 28, 4)

        # Generate top obstacles
        if random.randint(1, 5) == 1:
            self.image = vine
            self.rect = self.image.get_rect(
                topleft = (random.randint(SCREEN_WIDTH + 10, SCREEN_WIDTH + 100), 0))
            return

        random_obstacle = random.choice([rock_1, rock_2, rock_3])
        self.image = random_obstacle

        self.rect = self.image.get_rect(
            bottomleft = (random.randint(SCREEN_WIDTH + 10, SCREEN_WIDTH + 100), SCREEN_HEIGHT - GROUND_HEIGHT))

    def update(self):
        self.move()

    def move(self):
        global score
        self.rect.x -= 4
        if self.rect.right < 0:
            score += 1
            self.kill()

# Game functions
def draw_text(text, position = (10, 10), font_size = 20, center = False):
    my_font = pygame.font.SysFont("monospace", font_size)
    text_render = my_font.render(text, True, (0, 0, 0))

    if center:
        text_rect = text_render.get_rect(center = position)
        screen.blit(text_render, text_rect)
        return text_render

    screen.blit(text_render, position)
    return text_render


def generate_obstacles():
    random_screen_x = random.randint(SCREEN_WIDTH - 600, SCREEN_WIDTH - 220)
    if len(obstacles) == 0 or obstacles.sprites()[-1].rect.right < random_screen_x:
        obs = Obstacle()
        obstacles.add(obs)
        all_sprites.add(obs)

# Load images
background_image = pygame.image.load("assets/forest-background.jpg").convert()
scaled_background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
player_sheet = pygame.image.load("assets/player-spritesheet.png").convert_alpha()

ground = Ground()

# Add sprites to groups
all_sprites = pygame.sprite.Group()
all_sprites.add(ground)

platforms = pygame.sprite.Group()
platforms.add(ground)

obstacles = pygame.sprite.Group()

settings = {
    "screen_width": SCREEN_WIDTH,
    "screen_height": SCREEN_HEIGHT,
    "player_height": PLAYER_HEIGHT,
    "ground_height": GROUND_HEIGHT,
    "gravity": GRAVITY,
    "acc": ACC,
    "fric": FRIC,
    "player_sheet": player_sheet
}
game = {
    "score": 0,
    "platforms": platforms
}
player_1 = Player(settings, game)
all_sprites.add(player_1)

game_over = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player_1.cancel_jump()

    screen.blit(scaled_background, (0, 0))

    if game_over:
        center_width = SCREEN_WIDTH / 2
        center_height = SCREEN_HEIGHT / 2
        draw_text("Game Over!", (center_width, center_height - 80), 40, center=True)
        draw_text("Score: " + str(score), (center_width, center_height), 40, center=True)
        pygame.display.update()
        continue

    draw_text("Score: " + str(score))

    generate_obstacles()

    player_hits_obstacle = pygame.sprite.spritecollide(player_1, obstacles, False)
    if player_hits_obstacle:
        for entity in all_sprites:
            entity.kill()
        game_over = True

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    FramePerSec.tick(FPS)
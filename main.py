import pygame
from pygame.locals import *
import sys
import random
from Player import Player
from Obstacle import Obstacle
from Ground import Ground

# Global variables
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
GROUND_HEIGHT = 45
PLAYER_HEIGHT = 50
ACC = 0.5
FRIC = -0.12
FPS = 60
GRAVITY = 0.5

# Initialize pygame
pygame.init()
vec = pygame.math.Vector2
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Infinite Runner")
FramePerSec = pygame.time.Clock()

# Load images
background_image = pygame.image.load("assets/forest-background.jpg").convert()
scaled_background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
player_sheet = pygame.image.load("assets/player-spritesheet.png").convert_alpha()

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Creating settings and game objects that
# will be passed to sprite classes for initialization
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
    "platforms": platforms,
    "over": False,
    "start": False
}
player_1 = Player(settings, game)
all_sprites.add(player_1)

ground = Ground(settings)
all_sprites.add(ground)
platforms.add(ground)


def generate_obstacles():
    random_screen_x = random.randint(SCREEN_WIDTH - 600, SCREEN_WIDTH - 220)
    if len(obstacles) == 0 or obstacles.sprites()[-1].rect.right < random_screen_x:
        obs = Obstacle(settings, game, pygame)
        obstacles.add(obs)
        all_sprites.add(obs)


def draw_text(text, position = (10, 10), font_size = 20, center = False):
    my_font = pygame.font.SysFont("monospace", font_size)
    text_render = my_font.render(text, True, (0, 0, 0))

    if center:
        text_rect = text_render.get_rect(center = position)
        screen.blit(text_render, text_rect)
        return text_render

    screen.blit(text_render, position)
    return text_render


def start_game():
    global game, all_sprites, platforms, obstacles, player_1, ground
    game["over"] = False
    game["score"] = 0
    all_sprites.empty()
    platforms.empty()
    obstacles.empty()
    player_1 = Player(settings, game)
    all_sprites.add(player_1)
    ground = Ground(settings)
    all_sprites.add(ground)
    platforms.add(ground)
    game["start"] = True


def game_over_screen():
    center_width = SCREEN_WIDTH / 2
    center_height = SCREEN_HEIGHT / 2
    text_background = pygame.Surface((300, 150))
    text_background.fill((255, 255, 255))
    text_background.set_alpha(200)
    screen.blit(text_background, (center_width - 150, center_height - 120))
    draw_text("Game Over!", (center_width, center_height - 80), 40, center=True)
    draw_text("Score: " + str(game["score"]), (center_width, center_height), 40, center=True)
    pygame.display.update()


def game_start_screen():
    center_width = SCREEN_WIDTH / 2
    center_height = SCREEN_HEIGHT / 2
    text_background = pygame.Surface((300, 150))
    text_background.fill((255, 255, 255))
    text_background.set_alpha(200)
    screen.blit(text_background, (center_width - 150, center_height - 120))
    draw_text("Press SPACE to start", (center_width, center_height - 80), 40, center=True)
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game["start"]:
                player_1.jump()
            elif event.key == pygame.K_SPACE and (game["over"] or not game["start"]):
                start_game()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player_1.cancel_jump()

    screen.blit(scaled_background, (0, 0))

    if game["over"]:
        game_over_screen()
        continue

    if not game["start"]:
        game_start_screen()
        continue

    draw_text("Score: " + str(game["score"]))

    generate_obstacles()

    player_hits_obstacle = pygame.sprite.spritecollide(player_1, obstacles, False)
    if player_hits_obstacle:
        for entity in all_sprites:
            entity.kill()
        game["over"] = True
        game["start"] = False

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    FramePerSec.tick(FPS)
import pygame
from pygame.locals import *
import sys
import random
from Player import Player
from Obstacle import Obstacle
from Ground import Ground
from TextHelper import TextHelper

# Global variables
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
GROUND_HEIGHT = 45
PLAYER_HEIGHT = 90
ACC = 0.5
FRIC = -0.12
FPS = 60
GRAVITY = 0.5

DEFAULT_FONT = "skia"

# Initialize pygame
pygame.init()
vec = pygame.math.Vector2
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Infinite Runner")
FramePerSec = pygame.time.Clock()

# Background image
background_image = pygame.image.load("assets/forest-background.jpg").convert()
scaled_background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Obstacle images
rock_sprites = []
for i in range(1, 4):
    rock = pygame.image.load(f"assets/rock-{i}.png").convert_alpha()
    rock_sprites.append(rock)
rock_sprites[0] = pygame.transform.scale(rock_sprites[0], (55, 100))
rock_sprites[1] = pygame.transform.scale(rock_sprites[1], (60, 60))
rock_sprites[2] = pygame.transform.scale(rock_sprites[2], (60, 140))
vine = pygame.image.load("assets/vine.png").convert_alpha()
vine_height = SCREEN_HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT - 10
vine = pygame.transform.scale(vine, (30, vine_height))

# Player images
runner_sprites = []
for i in range(1, 9):
    runner_image = pygame.image.load(f"assets/running_man_{i}.png").convert_alpha()
    runner_sprites.append(runner_image)
runner_sprites.reverse()

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
    "running_images": runner_sprites,
    "game_speed": 4
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


obstacle_sprites = {
    "rocks": rock_sprites,
    "vine": vine
}
def generate_obstacles():
    random_screen_x = random.randint(SCREEN_WIDTH - 600, SCREEN_WIDTH - 220)
    if len(obstacles) == 0 or obstacles.sprites()[-1].rect.right < random_screen_x:
        obs = Obstacle(settings, game, obstacle_sprites)
        obstacles.add(obs)
        all_sprites.add(obs)


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


text_settings = {"font_size": 40, "font": DEFAULT_FONT}

def game_over_screen():
    text = TextHelper(pygame, screen, text_settings)
    text.draw("Game Over!").background((255, 255, 255)).center().render()
    text.draw("Score: " + str(game["score"])).background((255, 255, 255))
    text.center().set_offset((0, 70)).render()
    pygame.display.update()


def game_start_screen():
    text = TextHelper(pygame, screen, text_settings)
    text.draw("Press Space to start").background((255, 255, 255))
    text.center().render()
    pygame.display.update()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            for entity in all_sprites:
                entity.kill()
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

    generate_obstacles()

    player_hits_obstacle = pygame.sprite.spritecollide(player_1, obstacles, False)
    if player_hits_obstacle:
        for entity in all_sprites:
            entity.kill()
        game["over"] = True
        game["start"] = False

    all_sprites.update()
    all_sprites.draw(screen)

    # Display current score
    text = TextHelper(pygame, screen, {"font_size": 20, "font": DEFAULT_FONT})
    text.draw("Score: " + str(game["score"])).set_cords((50, 20)).render()

    pygame.display.flip()
    FramePerSec.tick(FPS)
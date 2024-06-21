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

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Generate top obstacles
        if random.randint(1, 5) == 1:
            height = SCREEN_HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT - 10
            self.surface = pygame.Surface((20, height))
            self.surface.fill((115, 16, 13))
            self.image = self.surface
            self.rect = self.surface.get_rect(
                topleft = (random.randint(SCREEN_WIDTH + 10, SCREEN_WIDTH + 100), 0))
            return

        height = random.randint(70, 100)
        self.surface = pygame.Surface((20, height))
        self.surface.fill((115, 16, 13))
        self.image = self.surface

        self.rect = self.surface.get_rect(
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


# Extract a frame from the spritesheet
def get_frame(spritesheet, frame_rect):
    frame = pygame.Surface((frame_rect[2], frame_rect[3]), pygame.SRCALPHA)
    frame.blit(spritesheet, (0, 0), frame_rect)
    return frame

# Load images
background_image = pygame.image.load("assets/forest-background.jpg").convert()
scaled_background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_sheet = pygame.image.load("assets/player-spritesheet.png").convert_alpha()

walk_frames = []
walk_frames.append(pygame.Rect(0, 18, 15, 15))
walk_frames.append(pygame.Rect(15, 18, 15, 15))
jump_frames = []
jump_frames.append(pygame.Rect(0, 45, 15, 15))
jump_frames.append(pygame.Rect(0, 60, 15, 15))
for i in range(0, len(walk_frames)):
    walk_frames[i] = get_frame(player_sheet, walk_frames[i])
for i in range(0, len(jump_frames)):
    jump_frames[i] = get_frame(player_sheet, jump_frames[i])

player_frames = {
    "walk": walk_frames,
    "jump": jump_frames
}


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
    "fric": FRIC
}
game = {
    "score": 0,
    "platforms": platforms
}
player_1 = Player(player_frames, settings, game)
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
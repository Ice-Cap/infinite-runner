import pygame
from pygame.locals import *
import sys
import random
import time

# Global variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

ACC = 0.5
FRIC = -0.12
FPS = 65
GRAVITY = 0.5

score = 0

pygame.init()
vec = pygame.math.Vector2
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Infinite Runner")

FramePerSec = pygame.time.Clock()

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((30, 30))
        self.surface.fill((10, 171, 74))
        self.rect = self.surface.get_rect(center = (10, 420))

        self.pos = vec((30, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False

    def move(self):
        self.acc = vec(0, GRAVITY)

        pressed_keys = pygame.key.get_pressed()

        # Acceleration is added when keys are pressed
        # Fricition is applied as a constant to movement in the x direction
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = SCREEN_WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos

    def check_stop_falling(self):
        # When hitting a platform, stop falling
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and self.vel.y > 0 and self.pos.y < hits[0].rect.bottom:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
            self.jumping = False

    def jump(self):
        # Can only jump if on a platform
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping and self.vel.y < -3:
            self.vel.y = -3

    def update(self):
        self.move()
        self.check_stop_falling()

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((SCREEN_WIDTH, 20))
        self.surface.fill((0, 0, 0))
        self.rect = self.surface.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 10))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Generate top obstacles
        if random.randint(1, 5) == 1:
            height = SCREEN_HEIGHT - 50
            self.surface = pygame.Surface((20, height))
            self.surface.fill((115, 16, 13))
            self.rect = self.surface.get_rect(
                topleft = (random.randint(SCREEN_WIDTH + 10, SCREEN_WIDTH + 100), 0))
            return

        height = random.randint(70, 100)
        self.surface = pygame.Surface((20, height))
        self.surface.fill((115, 16, 13))

        self.rect = self.surface.get_rect(
            bottomleft = (random.randint(SCREEN_WIDTH + 10, SCREEN_WIDTH + 100), SCREEN_HEIGHT - 20))

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

# Create ground and player objects
ground = Ground()
player_1 = Player()

# Add sprites to groups
all_sprites = pygame.sprite.Group()
all_sprites.add(ground)
all_sprites.add(player_1)

platforms = pygame.sprite.Group()
platforms.add(ground)

obstacles = pygame.sprite.Group()

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

    screen.fill((230, 230, 230))

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

    for entity in all_sprites:
        entity.update()
        screen.blit(entity.surface, entity.rect)

    pygame.display.flip()
    FramePerSec.tick(FPS)
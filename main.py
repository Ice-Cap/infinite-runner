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
FPS = 60
GRAVITY = 0.5

pygame.init()
vec = pygame.math.Vector2
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Infinite Runner")

my_font = pygame.font.SysFont("monospace", 20)

FramePerSec = pygame.time.Clock()

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((30, 30))
        self.surface.fill((128, 255, 40))
        self.rect = self.surface.get_rect(center = (10, 420))

        self.pos = vec((10, 385))
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
        y = SCREEN_HEIGHT - 10
        height = 100
        if random.randint(1, 8) == 1:
            y = (SCREEN_HEIGHT - 60) / 2
            height = SCREEN_HEIGHT - 60

        self.surface = pygame.Surface((20, height))
        self.surface.fill((0, 0, 0))
        self.rect = self.surface.get_rect(center = (SCREEN_WIDTH - 10, y))

    def update(self):
        self.move()

    def move(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

# Game functions
def draw_text(text):
    text_render = my_font.render(text, True, (0, 0, 0))
    screen.blit(text_render, (10, 10))

def generate_obstacles():
    random_screen_x = random.randint(round(SCREEN_WIDTH / 2) - 160, SCREEN_WIDTH - 220)
    if len(obstacles) == 0 or obstacles.sprites()[-1].rect.right < random_screen_x:
        obs = Obstacle()
        obstacles.add(obs)
        all_sprites.add(obs)

# Create ground and player objects
ground = Ground()
player_1 = Player()

obs_1 = Obstacle()

# Add sprites to groups
all_sprites = pygame.sprite.Group()
all_sprites.add(ground)
all_sprites.add(player_1)

platforms = pygame.sprite.Group()
platforms.add(ground)

obstacles = pygame.sprite.Group()

game_on = True
while game_on:
    for event in pygame.event.get():
        if event.type == QUIT:
            game_on = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player_1.cancel_jump()

    screen.fill((255, 255, 255))

    generate_obstacles()

    player_hits_obstacle = pygame.sprite.spritecollide(player_1, obstacles, False)
    if player_hits_obstacle:
        for entity in all_sprites:
            entity.kill()
        time.sleep(1)
        screen.fill((255,0,0))
        pygame.display.update()
        time.sleep(1)
        game_on = False
        pygame.quit()
        sys.exit()

    for entity in all_sprites:
        entity.update()
        screen.blit(entity.surface, entity.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)
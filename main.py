import pygame
import sys

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Infinite Runner")

my_font = pygame.font.SysFont("monospace", 20)

# Global variables
x = 10
y = 500
velocity = 0
gravity = 0.5
game_on = True
floor_y = 500
jumping = False
direction = None

# Game functions
def draw_player():
    pygame.draw.rect(screen, (0, 0, 255), (x, y, 50, 100))

def draw_text(text):
    text_render = my_font.render(text, True, (0, 0, 0))
    screen.blit(text_render, (10, 10))

while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
            pygame.quit()
            sys.exit()

    # Handle jumping and falling
    if direction == "up":
        y -= velocity
        velocity -= gravity
        if velocity <= 0:
            direction = "down"
    if direction == "down":
        y += velocity
        velocity += gravity
        if y >= floor_y:
            y = floor_y
            velocity = 0
            direction = None
            jumping = False

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        x -= 2
    if key[pygame.K_RIGHT]:
        x += 2
    if key[pygame.K_UP] and not jumping:
        velocity = 12
        direction = "up"
        jumping = True
    if key[pygame.K_DOWN] and jumping:
        y += 2

    screen.fill((255, 255, 255))

    draw_player()

    pygame.display.flip()
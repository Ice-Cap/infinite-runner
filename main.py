import pygame
import sys

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Game")

my_font = pygame.font.SysFont("monospace", 20)

x = 10
y = 500
velocity = 0
direction = None
gravity = 0.2
game_on = True
floor_y = 500

while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
            pygame.quit()
            sys.exit()

    if direction == "up":
        y -= velocity
        velocity -= gravity
        if velocity <= 0:
            direction = "down"
    if direction == "down":
        y += velocity
        velocity += gravity
        if y >= floor_y:
            velocity = 0
            direction = None

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        x -= 1
    if key[pygame.K_RIGHT]:
        x += 1
    if key[pygame.K_UP]:
        velocity = 2
        direction = "up"
        y -= 1
    if key[pygame.K_DOWN]:
        y += 1

    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (0, 0, 255), (x, y, 50, 100))

    x_y = my_font.render(f"x: {round(x)} y: {round(y)}", True, (0, 0, 0))
    screen.blit(x_y, (10, 10))
    velocity_render = my_font.render(f"velocity: {round(velocity)}", True, (0, 0, 0))
    screen.blit(velocity_render, (10, 40))
    direction_render = my_font.render(f"direction: {direction}", True, (0, 0, 0))
    screen.blit(direction_render, (10, 70))

    pygame.display.flip()
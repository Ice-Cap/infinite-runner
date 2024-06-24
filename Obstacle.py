import random
import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, settings, game, sprites):
        super().__init__()

        self.game = game
        self.settings = settings

        # Generate Vine
        if random.randint(1, 5) == 1:
            self.image = sprites["vine"]
            self.rect = self.image.get_rect(
                topleft = (random.randint(settings["screen_width"] + 10, settings["screen_width"] + 100), 0))
            return

        # Generate Rock
        random_obstacle = random.choice(sprites["rocks"])
        self.image = random_obstacle

        self.rect = self.image.get_rect(
            bottomleft = (random.randint(settings["screen_width"] + 10, settings["screen_width"] + 100), settings["screen_height"] - settings["ground_height"]))

    def update(self):
        self.move()

    def move(self):
        self.rect.x -= self.game["speed"]
        if self.rect.right < 0:
            self.game["speed"] += 0.05
            self.game["score"] += 1
            self.kill()
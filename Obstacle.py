import random
import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, settings, game, pygameRef):
        super().__init__()

        rock_1 = pygameRef.image.load("assets/rock-1.png").convert_alpha()
        rock_1 = pygameRef.transform.scale(rock_1, (55, 100))
        rock_2 = pygameRef.image.load("assets/rock-2.png").convert_alpha()
        rock_2 = pygameRef.transform.scale(rock_2, (60, 60))
        rock_3 = pygameRef.image.load("assets/rock-3.png").convert_alpha()
        rock_3 = pygameRef.transform.scale(rock_3, (60, 140))
        vine = pygameRef.image.load("assets/vine.png").convert_alpha()
        vine_height = settings["screen_height"] - settings["player_height"] - settings["ground_height"] - 10
        vine = pygameRef.transform.scale(vine, (30, vine_height))

        self.game = game

        # Generate top obstacles
        if random.randint(1, 5) == 1:
            self.image = vine
            self.rect = self.image.get_rect(
                topleft = (random.randint(settings["screen_width"] + 10, settings["screen_width"] + 100), 0))
            return

        random_obstacle = random.choice([rock_1, rock_2, rock_3])
        self.image = random_obstacle

        self.rect = self.image.get_rect(
            bottomleft = (random.randint(settings["screen_width"] + 10, settings["screen_width"] + 100), settings["screen_height"] - settings["ground_height"]))

    def update(self):
        self.move()

    def move(self):
        self.rect.x -= 4
        if self.rect.right < 0:
            self.game["score"] += 1
            self.kill()
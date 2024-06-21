import pygame

# Ground is a transparent surface that acts as a platform
class Ground(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        self.surface = pygame.Surface((settings["screen_width"], settings["ground_height"]), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        self.rect = self.surface.get_rect(bottomleft = (0, settings["screen_height"]))
        self.image = self.surface
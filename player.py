import pygame
from pygame.locals import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, settings, game):
        super().__init__()
        self.player_sheet = settings["player_sheet"]
        self.frames = self.initialize_frames()
        self.image = self.frames["walk"][0]
        self.image = pygame.transform.scale(self.image, (35, settings["player_height"]))
        self.rect = self.image.get_rect(center = (10, 430))
        self.settings = settings
        self.game = game

        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

        self.pos = vec((30, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False

    def move(self):
        settings = self.settings
        self.acc = vec(0, settings["gravity"])

        # Acceleration is added when keys are pressed
        # Fricition is applied as a constant to movement in the x direction
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -settings["acc"]
        if pressed_keys[K_RIGHT]:
            self.acc.x = settings["acc"]

        self.acc.x += self.vel.x * settings["fric"]
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > settings["screen_width"]:
            self.pos.x = settings["screen_width"]
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos

    def check_stop_falling(self):
        # When hitting a platform, stop falling
        hits = pygame.sprite.spritecollide(self, self.game["platforms"], False)
        if hits and self.vel.y > 0 and self.pos.y < hits[0].rect.bottom:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
            self.jumping = False

    def jump(self):
        # Can only jump if on a platform
        hits = pygame.sprite.spritecollide(self, self.game["platforms"], False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping and self.vel.y < -3:
            self.vel.y = -3

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 150:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames["walk"])
            self.image = self.frames["walk"][self.current_frame]
            self.image = pygame.transform.scale(self.image, (35, self.settings["player_height"]))

    def update(self):
        self.move()
        self.check_stop_falling()
        self.animate()

    # Extract a frame from the spritesheet
    def get_frame(self, spritesheet, frame_rect):
        frame = pygame.Surface((frame_rect[2], frame_rect[3]), pygame.SRCALPHA)
        frame.blit(spritesheet, (0, 0), frame_rect)
        return frame

    def initialize_frames(self):
        walk_frames = []
        walk_frames.append(pygame.Rect(0, 18, 15, 15))
        walk_frames.append(pygame.Rect(15, 18, 15, 15))
        jump_frames = []
        jump_frames.append(pygame.Rect(0, 45, 15, 15))
        jump_frames.append(pygame.Rect(0, 60, 15, 15))
        for i in range(0, len(walk_frames)):
            walk_frames[i] = self.get_frame(self.player_sheet, walk_frames[i])
        for i in range(0, len(jump_frames)):
            jump_frames[i] = self.get_frame(self.player_sheet, jump_frames[i])

        return {
            "walk": walk_frames,
            "jump": jump_frames
        }
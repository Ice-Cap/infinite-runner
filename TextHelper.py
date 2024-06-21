class TextHelper:
    def __init__(self, pygame, screen, settings):
        self.pygame = pygame
        self.screen = screen
        self.settings = settings
        self.font = self.pygame.font.SysFont(settings["font"], settings["font_size"])
        self.color = (0, 0, 0)
        self.cords = (0, 0)
        self.offset = None
        self.background_color = None
        self.is_center = False
        self.text = ""

    def draw(self, text):
        self.text = text
        return self

    def background(self, color):
        self.background_color = color
        return self

    def center(self):
        self.is_center = True
        return self

    def set_cords(self, cords):
        self.cords = cords
        return self

    def set_offset(self, offset):
        self.offset = offset
        return self

    def render(self):
        text = self.font.render(self.text, True, self.color)
        text_rect = text.get_rect(center = self.cords)

        if self.is_center:
            screen_center = self.screen.get_rect().center
            if self.offset:
                screen_center = (screen_center[0] + self.offset[0], screen_center[1] + self.offset[1])
            text_rect.center = screen_center

        if self.background_color:
            background = self.pygame.Surface((text_rect.width + 15, text_rect.height + 15))
            background.set_alpha(100)
            background_rect = background.get_rect(center = text_rect.center)
            background.fill(self.background_color)
            self.screen.blit(background, background_rect)

        self.screen.blit(text, text_rect)
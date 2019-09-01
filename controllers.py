import pygame

class Controller:
    def __init__(self):
        pass

    def handle(self, event):
        pass

class KeyController(Controller):
    def __init__(self, mappings):
        super().__init__()
        self.key_mappings = mappings
        self.event_type = pygame.KEYDOWN

    def handle(self, event):
        if event.key in self.key_mappings:
            self.key_mappings[event.key]()
import pygame
from util import transform_x, transform_y

class GraphicsObject:
    def __init__(self):
        pass

    def update(self, display, t, dt):
        self.draw(display)

    def hitbox(self):
        return None

    def collides(self, obj):
        pass

    def draw(self, display):
        pass

class Rect(GraphicsObject):
    def __init__(self, x, y, w, h, color = (0, 0, 0)):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def hitbox(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, display):
        pygame.draw.rect(display, self.color, Rect.transform(self, display))

    @staticmethod
    def transform(rect, display):
        return [transform_x(rect.x, display), transform_y(rect.y, display), transform_x(rect.w, display), transform_y(rect.h, display)]

class MovingRect(Rect):
    def __init__(self, x, y, w, h, v_x, v_y, color=(0,0,0)):
        super().__init__(x, y, w, h, color=color)
        self.v_x = v_x
        self.v_y = v_y

    def update(self, display, t, dt):
        self.x += self.v_x * dt
        self.y += self.v_y * dt
        self.draw(display)
import pygame
from util import transform_x, transform_y
from controllers import KeyController

class GraphicsObject:
    def __init__(self):
        self.env = None

    def update(self, display, t, dt, render):
        if render:
            self.draw(display)

    def hitbox(self):
        return None

    def collides(self, obj):
        pass

    def draw(self, display):
        pass

    def put_in(self, env):
        self.env = env

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

    def update(self, display, t, dt, render):
        self.x += self.v_x * dt
        self.y += self.v_y * dt
        if render:
            self.draw(display)

class Player(MovingRect):
    def __init__(self, x, y, w, h, v, color=(0,0,0)):
        self.v = v
        super().__init__(x, y, w, h, 0, 0, color=color)
        mappings = {
            pygame.K_LEFT: lambda: self.set_v(-self.v, 0),
            pygame.K_RIGHT: lambda: self.set_v(self.v, 0),
            pygame.K_UP: lambda: self.set_v(0, -self.v),
            pygame.K_DOWN: lambda: self.set_v(0, self.v)
        }
        self.controller = KeyController(mappings)

    def set_v(self, v_x, v_y):
        self.v_x = v_x
        self.v_y = v_y

    def put_in(self, env):
        super().put_in(env)
        env.register_controller(self.controller)


class Food(Rect):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, color=(0, 255, 0))

    def collide(self, obj):
        super.env.remove(self)

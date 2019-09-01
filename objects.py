import pygame

from util import transform_x, transform_y, squeeze
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
    def __init__(self, x, y, w, h, color=(0, 0, 0)):
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


class Food(Rect):

    _func = squeeze(-50, 50)

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, color=(0, 255, 0))

    def collides(self, obj):
        if isinstance(obj, Consumer):
            obj.consume(self.get_value())
            self.env.remove(self)

    def get_value(self):
        return Food._func(self.w * self.h / 10)

class Consumer(MovingRect):
    def __init__(self, x, y, w, h, v_x, v_y, color=(0,0,0)):
        super().__init__(x, y, w, h, v_x, v_y, color=color)
        self.energy = 100

    def consume(self, num):
        self.energy += num

    def lose(self, num):
        self.energy -= num

    def total_speed(self):
        return (self.v_x ** 2 + self.v_y ** 2) ** 0.5

    def total_area(self):
        return self.w * self.h

    def update(self, display, t, dt, render):
        super().update(display, t, dt, render)
        self.lose(self.total_speed() * self.total_area() * dt / 250)
        print(self.energy)
        if self.energy <= 0:
            self.env.remove(self)
        

class Player(Consumer):
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

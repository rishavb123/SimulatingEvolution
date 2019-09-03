import pygame
import math

from util import transform_x, transform_y, squeeze, argmin
from controllers import KeyController
from shapes import Rectangle, Circle
from constants import slowdown_rate

class GraphicsObject:
    def __init__(self):
        self.env = None
        self.storage = {}

    def update(self, display, t, dt, render):
        if render:
            self.draw(display)

    def hitbox(self):
        return None

    def on_collision(self, obj):
        pass

    def draw(self, display):
        pass

    def put_in(self, env):
        self.env = env

class GraphicsRectangle(GraphicsObject):
    def __init__(self, x, y, w, h, color=(0, 0, 0)):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def hitbox(self):
        return Rectangle(self.x, self.y, self.w, self.h)

    def draw(self, display):
        pygame.draw.rect(display, self.color, GraphicsRectangle.transform(self, display))

    @staticmethod
    def transform(rect, display):
        return [transform_x(rect.x, display), transform_y(rect.y, display), transform_x(rect.w, display), transform_y(rect.h, display)]

class GraphicsCircle(GraphicsObject):
    def __init__(self, x, y, r, color=(0, 0, 0)):
        super().__init__()
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def hitbox(self):
        return Circle(self.x, self.y, self.r)
    
    def draw(self, display):
        pygame.draw.ellipse(display, self.color, GraphicsCircle.transform(self, display))

    @staticmethod
    def transform(circle, display):
        return [transform_x(circle.x - circle.r, display), transform_y(circle.y - circle.r, display), transform_x(2 * circle.r, display), transform_y(2 * circle.r, display)]

class MovingRectangle(GraphicsRectangle):
    def __init__(self, x, y, w, h, v_x, v_y, color=(0,0,0)):
        super().__init__(x, y, w, h, color=color)
        self.v_x = v_x
        self.v_y = v_y

    def update(self, display, t, dt, render):
        self.x += self.v_x * dt
        self.y += self.v_y * dt
        if render:
            self.draw(display)

class Food:

    _func = squeeze(-50, 50)

    def on_collision(self, obj):
        if isinstance(obj, Consumer):
            obj.consume(self.get_value())
            self.env.remove(self)
    
    def get_value(self):
        return Food._func(self.get_area() / 10)

    def get_area(self):
        return 0

class CircleFood(Food, GraphicsCircle):

    def __init__(self, x, y, r):
        super().__init__(x, y, r, color=(0, 255, 0))

    def get_area(self):
        return math.pi * self.r ** 2

class RectFood(Food, GraphicsRectangle):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, color=(0, 255, 0))

    def get_area(self):
        return self.w * self.h

class Consumer(MovingRectangle):
    def __init__(self, x, y, w, h, v_x, v_y, color=(0,0,0)):
        super().__init__(x, y, w, h, v_x, v_y, color=color)
        self.energy = 100

    def consume(self, num):
        self.energy += num
        if self.energy > 100:
            self.energy = 100

    def lose(self, num):
        self.energy -= num

    def total_speed(self):
        return (self.v_x ** 2 + self.v_y ** 2) ** 0.5

    def total_area(self):
        return self.w * self.h

    def update(self, display, t, dt, render):
        super().update(display, t, dt, render)
        self.lose(self.total_speed() * self.total_area() * dt / 250)
        if self.energy <= 0:
            self.env.remove(self)
        
class Agent(Consumer):

    count = 0

    def __init__(self, x, y, w, h, v, color=(0,0,0), name=None):
        super().__init__(x, y, w, h, 0, 0, color=color)
        self.v = v
        Agent.count += 1
        if not name:
            name = "Agent {}".format(Agent.count)

    def get_targets(self):
        return self.env.get_all(Food)

    def choose_target(self):
        foods = self.get_targets()
        if foods:
            center_positions = list(map(lambda f: [f.x + f.w / 2, f.y + f.h / 2] if isinstance(f, RectFood) else [f.x, f.y], foods))
            my_pos = [self.x + self.w / 2, self.y + self.h / 2]
            squared_distances = list(map(lambda pos: (pos[0] - my_pos[0]) ** 2 + (pos[1] - my_pos[1]) ** 2, center_positions))
            for f in foods:
                if not 'consumers' in f.storage:
                    f.storage['consumers'] = []
                if self in f.storage['consumers']:
                    f.storage['consumers'].remove(self)
                    if len(f.storage['consumers']) == 0:
                        f.color = (0, 255, 0)
                    else:
                        f.color = (sum([c.color[0] for c in f.storage['consumers']]) / len(f.storage['consumers']), sum([c.color[1] for c in f.storage['consumers']]) / len(f.storage['consumers']), sum([c.color[2] for c in f.storage['consumers']]) / len(f.storage['consumers']))
            target = foods[argmin(squared_distances)]
            target.storage['consumers'].append(self)
            target.color = (sum([c.color[0] for c in target.storage['consumers']]) / len(target.storage['consumers']), sum([c.color[1] for c in target.storage['consumers']]) / len(target.storage['consumers']), sum([c.color[2] for c in target.storage['consumers']]) / len(target.storage['consumers']))
            return target
        else:
            return None

    def choose_v(self):
        food = self.choose_target()
        if food:
            direction = [0, 0]
            if isinstance(food, CircleFood):
                if self.x + self.w <= food.x - food.r / 2:
                    direction[0] = 1
                elif self.x >= food.x + food.r / 2:
                    direction[0] = -1
                if self.y + self.h <= food.y - food.r / 2:
                    direction[1] = 1
                elif self.y >= food.y + food.r / 2:
                    direction[1] = -1
                if direction[0] != 0 and direction[1] != 0:
                    self.v_x = direction[0] * self.v / 2 ** 0.5
                    self.v_y = direction[1] * self.v / 2 ** 0.5
                elif direction[0] == 0 and direction[1] == 0:
                    self.v_x *= slowdown_rate
                    self.v_y *= slowdown_rate
                else:
                    self.v_x = direction[0] * self.v
                    self.v_y = direction[1] * self.v
            elif isinstance(food, RectFood):
                if self.x + self.w <= food.x:
                    direction[0] = 1
                elif self.x >= food.x + food.w:
                    direction[0] = -1
                if self.y + self.h <= food.y:
                    direction[1] = 1
                elif self.y >= food.y + food.h:
                    direction[1] = -1
                if direction[0] != 0 and direction[1] != 0:
                    self.v_x = direction[0] * self.v / 2 ** 0.5
                    self.v_y = direction[1] * self.v / 2 ** 0.5
                elif direction[0] == 0 and direction[1] == 0:
                    self.v_x *= slowdown_rate
                    self.v_y *= slowdown_rate
                else:
                    self.v_x = direction[0] * self.v
                    self.v_y = direction[1] * self.v
            else:
                self.v_x *= slowdown_rate
                self.v_y *= slowdown_rate
        else:
            self.v_x *= slowdown_rate
            self.v_y *= slowdown_rate

    def update(self, display, t, dt, render):
        self.choose_v()
        super().update(display, t, dt, render)
        

class Player(Consumer):

    count = 0

    def __init__(self, x, y, w, h, v, color=(0,0,0), name=None):
        super().__init__(x, y, w, h, 0, 0, color=color)
        self.v = v
        mappings = {
            pygame.K_LEFT: lambda: self.set_v(-self.v, 0),
            pygame.K_RIGHT: lambda: self.set_v(self.v, 0),
            pygame.K_UP: lambda: self.set_v(0, -self.v),
            pygame.K_DOWN: lambda: self.set_v(0, self.v)
        }
        self.controller = KeyController(mappings)
        Player.count += 1
        if not name:
            name = "Agent {}".format(Player.count)

    def set_v(self, v_x, v_y):
        self.v_x = v_x
        self.v_y = v_y

    def put_in(self, env):
        super().put_in(env)
        env.register_controller(self.controller)

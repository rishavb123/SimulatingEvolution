import random

from util import set_interval
from objects import RectFood, CircleFood

class Interval:

    def __init__(self, func=None, s=1):
        if func:
            self.func = func
        self.s = s

    def func(self):
        print("hello world")

    def start(self):
        set_interval(self.func, self.s)

class Spawner(Interval):

    def __init__(self, spawn_func=None, s=1, env=None):
        super().__init__(s=s)
        if spawn_func:
            self.spawn_func = spawn_func
        self.env = env

    def func(self):
        self.env.add(self.spawn_func())
        

class FoodSpawner(Spawner):
    
    def __init__(self, w_func, h_func, r_func, circ_prob, s, env):
        super().__init__(s=s, env=env)
        self.w_func = w_func
        self.h_func = h_func
        self.r_func = r_func
        self.circ_prob = circ_prob

    def spawn_func(self):
        if random.random() < self.circ_prob:
            r = self.r_func()
            return CircleFood(random.randrange(r, 100 - r), random.randrange(r, 100 - r), r)
        else:
            w = self.w_func()
            h = self.h_func()
            return RectFood(random.randrange(0, 100 - w), random.randrange(0, 100 - h), w, h)
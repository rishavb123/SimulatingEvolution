import random

from util import set_interval
from objects import Food

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
    
    def __init__(self, w_func, h_func, s, env):
        super().__init__(s=1, env=env)
        self.w_func = w_func
        self.h_func = h_func

    def spawn_func(self):
        w = self.w_func()
        h = self.h_func()
        return Food(random.randrange(0, 100 - w), random.randrange(0, 100 - h), w, h)
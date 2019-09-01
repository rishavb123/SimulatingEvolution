import threading
import pygame
import math

def set_interval(func, s):
    def func_wrapper():
        set_interval(func, s)
        func()
    
    t = threading.Timer(s, func_wrapper)
    t.start()
    return t

def transform_x(x, display):
    return x * display.get_size()[0] / 100

def transform_y(y, display):
    return y * display.get_size()[1] / 100

def sigmoid(x):
    return 1 / (1 + math.e ** (-x))

def squeeze(minimum, maximum):
    return lambda x: minimum + sigmoid(x / 3) * (maximum - minimum)

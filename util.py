import threading
import pygame

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

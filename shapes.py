from util import clamp

class Shape:
    def __init__(self):
        pass

class Rectangle(Shape):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class Circle(Shape):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

def collides(shape1, shape2):
    shapes = [shape1, shape2]
    def get(shape_type):
        return list(filter(lambda s: isinstance(s, shape_type), shapes))
    rectangles = get(Rectangle)
    circles = get(Circle)
    if len(rectangles) == 2:
        r1 = rectangles[0]
        r2 = rectangles[1]
        return r1.x + r1.w >= r2.x and r1.x <= r2.x + r2.w and r1.y + r1.h >= r2.y and r1.y <= r2.y + r2.h
    elif len(circles) == 2:
        c1 = circles[0]
        c2 = circles[1]
        return ((c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2) ** 0.5 <= c1.r + c2.r
    elif len(rectangles) == 1 and len(circles) == 1:
        r = rectangles[0]
        c = circles[0]
        closest = [clamp(c.x, r.x, r.x + r.w), clamp(c.y, r.y, r.y + r.h)]
        distances = [c.x - closest[0], c.y - closest[1]]
        return distances[0] ** 2 + distances[1] **2 < c.r **2
    else:
        return False
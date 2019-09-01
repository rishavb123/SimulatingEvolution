class Environment:

    def __init__(self):
        self.objects = []

    def add(self, item):
        if type(item) == 'list':
            for i in item:
                add(i)
        else:
            self.objects.append(item)

    def update(self, display, t, dt):
        for i in range(len(self.objects)):
            obj = self.objects[i]
            for j in range(i + 1, len(self.objects)):
                if obj.hitbox() and obj.hitbox().colliderect(self.objects[j].hitbox()):
                    obj.collides(self.objects[j])
                    self.objects[j].collides(obj)
            obj.update(display, t, dt)
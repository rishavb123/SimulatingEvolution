from shapes import collides

class Environment:

    def __init__(self):
        self.objects = []
        self.controllers = {}
        self.remove_items = []

    def add(self, item):
        if isinstance(item, list):
            for i in item:
                self.add(i)
        else:
            self.objects.append(item)
            item.put_in(self)

    def remove(self, item):
        if isinstance(item, list):
            for i in item:
                remove(i)
        else:
            self.remove_items.append(item)

    def __real_remove(self, item):
        if isinstance(item, list):
            for i in item:
                self.__real_remove(i)
        else:
            if item in self.objects:
                self.objects.remove(item)

    def get_all(self, obj_type):
        return list(filter(lambda obj: isinstance(obj, obj_type), self.objects)) + list(filter(lambda obj: isinstance(obj, obj_type), self.controllers))

    def register_controller(self, controller):
        event_type = controller.event_type
        if not event_type in self.controllers:
            self.controllers[event_type] = []
        self.controllers[event_type].append(controller)

    def update(self, display, t, dt, render):
        for i in range(len(self.objects)):
            obj = self.objects[i]
            for j in range(i + 1, len(self.objects)):
                if obj.hitbox() and self.objects[j].hitbox() and collides(obj.hitbox(), self.objects[j].hitbox()):
                    obj.on_collision(self.objects[j])
                    self.objects[j].on_collision(obj)
            obj.update(display, t, dt, render)
        self.__real_remove(self.remove_items)
        self.remove_items = []

    def handle(self, event):
        if event.type in self.controllers:
            for controller in self.controllers[event.type]:
                controller.handle(event)

class Environment:

    def __init__(self):
        self.objects = []
        self.controllers = {}
        self.remove_items = []

    def add(self, item):
        if isinstance(item, list):
            for i in item:
                add(i)
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
            self.objects.remove(item)

    def register_controller(self, controller):
        event_type = controller.event_type
        if not event_type in self.controllers:
            self.controllers[event_type] = []
        self.controllers[event_type].append(controller)

    def update(self, display, t, dt, render):
        for i in range(len(self.objects)):
            obj = self.objects[i]
            for j in range(i + 1, len(self.objects)):
                if obj.hitbox() and obj.hitbox().colliderect(self.objects[j].hitbox()):
                    obj.collides(self.objects[j])
                    self.objects[j].collides(obj)
            obj.update(display, t, dt, render)
        self.__real_remove(self.remove_items)
        self.remove_items = []

    def handle(self, event):
        if event.type in self.controllers:
            for controller in self.controllers[event.type]:
                controller.handle(event)

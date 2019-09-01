import random

class Param:
    def __init__(self, value, values, mutation_chance = 0.01):
        self.value = value
        self.values = values
        self.mutation_chance = mutation_chance
        
    def copy(self):
        return Param(self.value, self.values, self.mutation_chance)

    def mutate(self):
        self.value = self.values.choice()

    def mutation_step(self):
        if random.random() < self.mutation_chance:
            self.mutate()

    @staticmethod
    def copy_all(params):
        return map(lambda p: p.copy(), params)

    @staticmethod
    def mutation_step_all(params):
        for p in params:
            p.mutation_step()

class Values:
    def __init__(self, values_type, poss_values = None, minimum = None, maximum = None):
        self.type = values_type
        if values_type == 'range':
            if not minimum or not maximum:
                raise Exception("For type range, minimum and maximum must be defined")
            self._min = minimum
            self._max = maximum
        elif values_type == 'list':
            if not poss_values:
                raise Exception("For type range, possible values must be defined")
            self._poss_values = poss_values
        else:
            raise Exception("Type must be either range or list")

    def choice(self):
        if self.type == 'range':
            return random.randrange(self._min, self._max)
        elif self.type == 'list':
            return random.choice(self._poss_values)
        else:
            raise Exception("Type must be either range or list")

    def sample(self, length):
        return [self.choice() for _ in range(length)]

    def contains(self, x):
        if self.type == 'range':
            return self._min <= x <= self._max
        elif self.type == 'list':
            return x in self._poss_values
        else:
            raise Exception("Type must be either range or list")

    def __str__(self):
        if self.type == 'range':
            return "[{}, {}]".format(self._min, self._max)
        elif self.type == 'list':
            return str(self._poss_values)
        else:
            raise Exception("Type must be either range or list")
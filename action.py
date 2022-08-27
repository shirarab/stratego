from constants import Direction, Degree
from soldier import Soldier


class Action(object):
    def __init__(self, soldier: Soldier, direction: Direction, num_steps: int, assumed_degree: Degree = None):
        self._soldier = soldier
        self._direction = direction
        self._num_steps = num_steps
        self._assumed_degree = assumed_degree

    @property
    def soldier(self):
        return self._soldier

    @property
    def direction(self):
        return self._direction

    @property
    def num_steps(self):
        return self._num_steps
    
    @property
    def assumed_degree(self):
        return self._assumed_degree

    def __eq__(self, other):
        if self.soldier != other.soldier \
                or self.direction != other.direction \
                or self.num_steps != other.num_steps:
            return False
        return True

    def __hash__(self):
        return hash((self.soldier, self.direction, self.num_steps))

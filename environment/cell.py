
from enum import Enum


class CellType(Enum):
    EMPTY = 0
    WALL = 1
    FIRE = 2
    EXIT = 3
    PERSON = 4


class Cell:
    def __init__(self, x, y, cell_type=CellType.EMPTY):
        self.x = x
        self.y = y
        self.type = cell_type
        self.danger_level = 0

    def is_passable(self):
        return self.type not in (CellType.WALL, CellType.FIRE)

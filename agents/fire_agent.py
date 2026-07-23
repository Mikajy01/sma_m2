
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

from environment.cell import CellType


class FireAgent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.positions = [(x, y)]

    def spread(self, building):
        new_positions = []
        for (x, y) in self.positions:
            cell = building.get_cell(x, y)
            if cell:
                cell.type = CellType.FIRE
                directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    ncell = building.get_cell(nx, ny)
                    if ncell and ncell.type == CellType.EMPTY and random.random() < 0.2:
                        if (nx, ny) not in self.positions and (nx, ny) not in new_positions:
                            new_positions.append((nx, ny))
        self.positions.extend(new_positions)

    def reset(self, x, y):
        self.positions = [(x, y)]

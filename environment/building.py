
from environment.cell import Cell, CellType
from utils.constants import GRID_WIDTH, GRID_HEIGHT
import random


class Building:
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.cells = self._init_grid()

    def _init_grid(self):
        grid = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
        
        # Ajouter des murs sur les bords
        for x in range(self.width):
            grid[0][x].type = CellType.WALL
            grid[self.height - 1][x].type = CellType.WALL
        for y in range(self.height):
            grid[y][0].type = CellType.WALL
            grid[y][self.width - 1].type = CellType.WALL
            
        # Ajouter des murs intérieurs
        for y in range(1, self.height - 1):
            grid[y][self.width // 2].type = CellType.WALL
            
        # Ajouter des ouvertures dans les murs
        grid[3][self.width // 2].type = CellType.EMPTY
        grid[8][self.width // 2].type = CellType.EMPTY
        
        # Ajouter des sorties
        grid[2][self.width - 2].type = CellType.EXIT
        grid[9][self.width - 2].type = CellType.EXIT
        
        # Ajouter du feu initial
        grid[5][5].type = CellType.FIRE
        
        return grid

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None

    def get_neighbors(self, x, y):
        neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            cell = self.get_cell(x + dx, y + dy)
            if cell:
                neighbors.append(cell)
        return neighbors

    def find_all_exits(self):
        exits = []
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[y][x].type == CellType.EXIT:
                    exits.append((x, y))
        return exits

    def reset(self):
        self.cells = self._init_grid()
        
    def get_random_passable_cell(self):
            while True:
                x = random.randint(1, self.width - 2)
                y = random.randint(1, self.height - 2)
                cell = self.cells[y][x]
                if cell.type == CellType.EMPTY:
                    return x, y
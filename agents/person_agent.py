
import sys
import os
from enum import Enum

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from environment.cell import CellType
from ai.q_learning import QLearning
from utils.constants import ACTIONS


class PersonState(Enum):
    ALIVE = 0
    EVACUATED = 1
    DEAD = 2


class PersonAgent:
    def __init__(self, x, y, q_learning=None, use_q_learning=False):
        self.x = x
        self.y = y
        self.state = PersonState.ALIVE
        self.q_learning = q_learning or QLearning()
        self.use_q_learning = use_q_learning
        self.move_count = 0
        self.initial_x = x
        self.initial_y = y

    def _calculate_min_distance_to_exit(self, x, y, exits):
        min_dist = float('inf')
        for (ex, ey) in exits:
            dist = abs(x - ex) + abs(y - ey)
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def _calculate_danger_level(self, x, y, building):
        danger = 0
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                cell = building.get_cell(x + dx, y + dy)
                if cell and cell.type == CellType.FIRE:
                    distance = abs(dx) + abs(dy)
                    danger += max(0, 5 - distance)
        return danger

    def choose_action_basic(self, building, exits):
        best_action = 4  # attendre
        min_dist = self._calculate_min_distance_to_exit(self.x, self.y, exits)
        
        for i, (dx, dy) in enumerate(ACTIONS):
            nx, ny = self.x + dx, self.y + dy
            cell = building.get_cell(nx, ny)
            if cell and cell.is_passable():
                dist = self._calculate_min_distance_to_exit(nx, ny, exits)
                if dist < min_dist:
                    min_dist = dist
                    best_action = i
        return best_action

    def choose_action(self, building, exits, training=True):
        if not self.use_q_learning:
            return self.choose_action_basic(building, exits)
        else:
            danger_level = self._calculate_danger_level(self.x, self.y, building)
            min_distance = self._calculate_min_distance_to_exit(self.x, self.y, exits)
            return self.q_learning.choose_action(self.x, self.y, danger_level, min_distance, training=training)

    def move(self, action, building, exits):
        dx, dy = ACTIONS[action]
        nx, ny = self.x + dx, self.y + dy
        cell = building.get_cell(nx, ny)
        if cell and cell.is_passable():
            self.x, self.y = nx, ny
            self.move_count += 1

    def check_state(self, building):
        cell = building.get_cell(self.x, self.y)
        if cell and cell.type == CellType.EXIT:
            self.state = PersonState.EVACUATED
        elif cell and cell.type == CellType.FIRE:
            self.state = PersonState.DEAD

    def get_reward(self, old_x, old_y, building, exits):
        cell = building.get_cell(self.x, self.y)
        if cell and cell.type == CellType.EXIT:
            return 100
        elif cell and cell.type == CellType.FIRE:
            return -100
        else:
            old_dist = self._calculate_min_distance_to_exit(old_x, old_y, exits)
            new_dist = self._calculate_min_distance_to_exit(self.x, self.y, exits)
            reward = -1
            if new_dist < old_dist:
                reward += 10
            elif new_dist > old_dist:
                reward -= 5
            return reward

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.state = PersonState.ALIVE
        self.move_count = 0

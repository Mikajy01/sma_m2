

import sys

# Block numpy/matplotlib imports
sys.modules['numpy'] = None
sys.modules['matplotlib'] = None
import pygame
from simulation.simulator import Simulator
from environment.cell import CellType
from agents.person_agent import PersonState
from utils.constants import (
    COLOR_WALL, COLOR_EMPTY, COLOR_FIRE, COLOR_EXIT,
    COLOR_PERSON, COLOR_PERSON_EVACUATED, COLOR_PERSON_DEAD,
    COLOR_UI_BACKGROUND, COLOR_TEXT,
    CELL_SIZE, GRID_WIDTH, GRID_HEIGHT,
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS
)


class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.color = (100, 150, 200)
        self.hover_color = (120, 170, 220)

    def draw(self, screen, font):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        text_surface = font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("SMA Evacuation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    use_q_learning = False
    simulator = Simulator(use_q_learning=False)
    running = True
    simulating = False

    def start_simulation():
        nonlocal simulating
        simulating = True

    def reset_simulation():
        nonlocal simulating
        simulating = False
        simulator.reset()

    def toggle_mode():
        nonlocal use_q_learning, simulator
        use_q_learning = not use_q_learning
        simulator = Simulator(use_q_learning=use_q_learning)
        if use_q_learning:
            simulator.q_learning.load_policy()
        reset_simulation()

    def train_agents():
        nonlocal simulator
        simulator.train()
        toggle_mode()

    buttons = [
        Button(GRID_WIDTH * CELL_SIZE + 20, 20, 260, 40, "Démarrer simulation", start_simulation),
        Button(GRID_WIDTH * CELL_SIZE + 20, 70, 260, 40, "Réinitialiser", reset_simulation),
        Button(GRID_WIDTH * CELL_SIZE + 20, 120, 260, 40, "Lancer entraînement", train_agents),
        Button(GRID_WIDTH * CELL_SIZE + 20, 170, 260, 40, "Changer mode", toggle_mode)
    ]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for btn in buttons:
                btn.handle_event(event)

        if simulating:
            all_done = simulator.step(training=False)
            if all_done:
                simulating = False

        # Draw grid
        screen.fill(COLOR_EMPTY)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell = simulator.building.cells[y][x]
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if cell.type == CellType.WALL:
                    pygame.draw.rect(screen, COLOR_WALL, rect)
                elif cell.type == CellType.FIRE:
                    pygame.draw.rect(screen, COLOR_FIRE, rect)
                elif cell.type == CellType.EXIT:
                    pygame.draw.rect(screen, COLOR_EXIT, rect)
                else:
                    pygame.draw.rect(screen, COLOR_EMPTY, rect)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)

        # Draw persons
        for person in simulator.persons:
            x, y = person.x, person.y
            rect = pygame.Rect(x * CELL_SIZE + 5, y * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10)
            if person.state == PersonState.ALIVE:
                pygame.draw.ellipse(screen, COLOR_PERSON, rect)
            elif person.state == PersonState.EVACUATED:
                pygame.draw.ellipse(screen, COLOR_PERSON_EVACUATED, rect)
            elif person.state == PersonState.DEAD:
                pygame.draw.ellipse(screen, COLOR_PERSON_DEAD, rect)

        # Draw UI panel
        ui_rect = pygame.Rect(GRID_WIDTH * CELL_SIZE, 0, 300, WINDOW_HEIGHT)
        pygame.draw.rect(screen, COLOR_UI_BACKGROUND, ui_rect)

        stats = simulator.get_statistics()
        mode_text = "Q-Learning" if use_q_learning else "Basique"
        info_lines = [
            f"Temps : {stats['time']}",
            f"Personnes évacuées : {stats['evacuated']} / {stats['total']}",
            f"Personnes mortes : {stats['dead']}",
            f"Episode : {simulator.episode}",
            f"Mode : {mode_text}"
        ]

        for i, line in enumerate(info_lines):
            text_surface = font.render(line, True, COLOR_TEXT)
            screen.blit(text_surface, (GRID_WIDTH * CELL_SIZE + 20, 230 + i * 30))

        for btn in buttons:
            btn.draw(screen, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

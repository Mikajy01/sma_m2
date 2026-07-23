
# Configuration des couleurs
COLOR_WALL = (50, 50, 50)
COLOR_EMPTY = (240, 240, 240)
COLOR_FIRE = (255, 100, 0)
COLOR_EXIT = (0, 200, 0)
COLOR_PERSON = (0, 100, 255)
COLOR_PERSON_EVACUATED = (0, 150, 100)
COLOR_PERSON_DEAD = (200, 0, 0)
COLOR_UI_BACKGROUND = (200, 200, 200)
COLOR_TEXT = (0, 0, 0)

# Configuration de la grille
CELL_SIZE = 40
GRID_WIDTH = 20
GRID_HEIGHT = 12

# Configuration de la fenêtre
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + 300
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 10

# Configuration de l'apprentissage
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPSILON = 0.1
EPISODES = 500

# Directions de déplacement
ACTIONS = [
    (0, -1),  # haut
    (0, 1),   # bas
    (-1, 0),  # gauche
    (1, 0),   # droite
    (0, 0)    # attendre
]

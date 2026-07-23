import random
import pickle

from utils.constants import ACTIONS, LEARNING_RATE, DISCOUNT_FACTOR, EPSILON_START, EPSILON_MIN, EPSILON_DECAY


class QLearning:
    def __init__(self):
        self.q_table = {}
        self.alpha = LEARNING_RATE
        self.gamma = DISCOUNT_FACTOR
        self.epsilon = EPSILON_START
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = EPSILON_DECAY
        self.actions = ACTIONS

    def _get_state(self, x, y, danger_level, min_distance):
        return (x, y, min(danger_level, 10), min(min_distance, 20))

    def _ensure_state_exists(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0.0] * len(self.actions)

    def choose_action(self, x, y, danger_level, min_distance, training=True):
        state = self._get_state(x, y, danger_level, min_distance)
        self._ensure_state_exists(state)
        if training and random.random() < self.epsilon:
            return random.randint(0, len(self.actions) - 1)
        else:
            q_values = self.q_table[state]
            max_q = max(q_values)
            # tie-break aléatoire entre actions à égalité (évite un biais vers l'action 0)
            best_actions = [i for i, q in enumerate(q_values) if q == max_q]
            return random.choice(best_actions)

    def update_q_value(self, x, y, danger_level, min_distance, action, reward,
                       next_x, next_y, next_danger_level, next_min_distance):
        state = self._get_state(x, y, danger_level, min_distance)
        next_state = self._get_state(next_x, next_y, next_danger_level, next_min_distance)
        self._ensure_state_exists(state)
        self._ensure_state_exists(next_state)
        old_q = self.q_table[state][action]
        next_max_q = max(self.q_table[next_state])
        new_q = old_q + self.alpha * (reward + self.gamma * next_max_q - old_q)
        self.q_table[state][action] = new_q

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save_policy(self, filename="q_table.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.q_table, f)

    def load_policy(self, filename="q_table.pkl"):
        try:
            with open(filename, "rb") as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            pass
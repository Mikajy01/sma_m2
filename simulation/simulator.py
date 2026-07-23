from environment.building import Building
from agents.person_agent import PersonAgent, PersonState
from agents.fire_agent import FireAgent
from ai.q_learning import QLearning
from utils.constants import EPISODES, MAX_STEPS_PER_EPISODE


class Simulator:
    def __init__(self, use_q_learning=False):
        self.building = Building()
        self.fire = FireAgent(5, 5)
        self.persons = []
        self.q_learning = QLearning()
        self.use_q_learning = use_q_learning
        self.time = 0
        self.episode = 0
        self._init_persons()

    def _init_persons(self):
        self.persons = [
            PersonAgent(2, 2, q_learning=self.q_learning, use_q_learning=self.use_q_learning),
            PersonAgent(2, 5, q_learning=self.q_learning, use_q_learning=self.use_q_learning),
            PersonAgent(2, 9, q_learning=self.q_learning, use_q_learning=self.use_q_learning),
            PersonAgent(10, 2, q_learning=self.q_learning, use_q_learning=self.use_q_learning),
            PersonAgent(10, 9, q_learning=self.q_learning, use_q_learning=self.use_q_learning)
        ]

    def reset(self, randomize=False):
        self.building.reset()
        self.fire.reset(5, 5)
        for p in self.persons:
            if randomize:
                x, y = self.building.get_random_passable_cell()
                p.reset(x, y)
            else:
                p.reset()
        self.time = 0

    def step(self, training=True):
        exits = self.building.find_all_exits()

        for person in self.persons:
            if person.state == PersonState.ALIVE:
                old_x, old_y = person.x, person.y
                action = person.choose_action(self.building, exits, training=training)

                if self.use_q_learning and training:
                    old_danger = person._calculate_danger_level(old_x, old_y, self.building)
                    old_dist = person._calculate_min_distance_to_exit(old_x, old_y, exits)

                person.move(action, self.building, exits)
                person.check_state(self.building)

                if self.use_q_learning and training:
                    new_danger = person._calculate_danger_level(person.x, person.y, self.building)
                    new_dist = person._calculate_min_distance_to_exit(person.x, person.y, exits)
                    reward = person.get_reward(old_x, old_y, self.building, exits, action=action)
                    self.q_learning.update_q_value(old_x, old_y, old_danger, old_dist, action, reward,
                                                   person.x, person.y, new_danger, new_dist)

        self.fire.spread(self.building)
        self.time += 1

        for person in self.persons:
            if person.state == PersonState.ALIVE:
                person.check_state(self.building)

        all_done = all(p.state != PersonState.ALIVE for p in self.persons)
        return all_done

    def train(self):
        self.use_q_learning = True
        for episode in range(EPISODES):
            self.episode = episode
            self.reset(randomize=True)  # positions de départ variées à chaque épisode
            done = False
            steps = 0
            while not done and steps < MAX_STEPS_PER_EPISODE:
                done = self.step(training=True)
                steps += 1

            self.q_learning.decay_epsilon()

            if episode % 100 == 0 or episode == EPISODES - 1:
                stats = self.get_statistics()
                print(f"Épisode {episode}/{EPISODES} - "
                      f"Évacués: {stats['evacuated']}/{stats['total']} - "
                      f"Morts: {stats['dead']} - "
                      f"Epsilon: {self.q_learning.epsilon:.3f}")

            if episode % 500 == 0 and episode > 0:
                self.q_learning.save_policy()

        self.q_learning.save_policy()

    def get_statistics(self):
        total = len(self.persons)
        evacuated = sum(1 for p in self.persons if p.state == PersonState.EVACUATED)
        dead = sum(1 for p in self.persons if p.state == PersonState.DEAD)
        total_moves = sum(p.move_count for p in self.persons)
        return {
            "time": self.time,
            "total": total,
            "evacuated": evacuated,
            "dead": dead,
            "total_moves": total_moves
        }
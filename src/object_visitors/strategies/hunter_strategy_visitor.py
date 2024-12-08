import random
from time import time
from math import sqrt, exp

# Here a strategy for interacting with each object type can be implemented
# It will be triggered if it's the highest priority visible object

class HunterStrategyVisitor:
    def __init__(self, hunter):
        self.hunter = hunter

    def visit_player(self, player):
        # Shoot a bullet if the previous shot was long enough ago
        if time() - self.hunter.prev_shot_time > self.hunter.fire_rate:
            self.hunter.bullet_strategy = self.choose_strategy()
            if self.hunter.bullet_strategy == 1:
                self.predict_bullet_direction(player)
                self.hunter.shots[1] += 1
            else:
                self.hunter.bullet_direction = (player.pos - self.hunter.pos).normalize()
                self.hunter.shots[0] += 1
            self.hunter.bullet_ready = True
        else:
            self.hunter.look_at(player.pos)

    def visit_basic_npc(self, basic_npc):
       self.hunter.look_at(basic_npc.pos)
       if time() - self.hunter.prev_shot_time > self.hunter.fire_rate:
           self.hunter.bullet_ready = True

    def visit_bullet(self, bullet):
        pass
        # self.hunter.look_at(bullet.pos)
        # self.hunter.dir = self.hunter.dir.rotate(90)

    def visit_obstacle(self, obstacle):
        pass # TODO ? Not sure

    def visit_coin(self, coin):
        self.hunter.look_at(coin.pos)

    def visit_medkit(self, medkit):
        self.hunter.look_at(medkit.pos)

    def predict_bullet_direction(self, player):
        if player.speed_vector.length() == 0:
            self.hunter.look_at(player.pos)
            return

        # I will match the names in my calculations on paper
        d = self.hunter.pos.distance_to(player.pos)
        b = self.hunter.bullet_speed
        p = player.speed
        pv = player.speed_vector
        P = player.pos
        N = self.hunter.pos
        M = N + b ** 2 / (b ** 2 - p ** 2) * (P - N)
        R = d * p * b / (b ** 2 - p ** 2)
        a2 = pv.x ** 2 + pv.y ** 2
        a1 = 2 * (pv.x * (P.x - M.x) + pv.y * (P.y - M.y))
        a0 = M.x ** 2 + M.y ** 2 + P.x ** 2 + P.y ** 2 - R ** 2 - 2 * M.x * P.x - 2 * M.y * P.y
        D = a1 ** 2 - 4 * a2 * a0

        # failsafe in case bullet is slower than the player
        if D < 0:
            D = 0
        t = (-a1 + sqrt(D)) / (2 * a2)
        predicted_direction = P + t * pv - N
        predicted_direction = 1 / predicted_direction.length() * predicted_direction
        self.hunter.bullet_direction = predicted_direction

    def choose_strategy(self):
        if self.hunter.shots[0] == 0:
            return 0
        if self.hunter.shots[1] == 0:
            return 1
        hit_rates = [hits / shots for hits, shots in zip(self.hunter.hits, self.hunter.shots)]
        if random.random() < exp(hit_rates[0]) / (exp(hit_rates[0]) + exp(hit_rates[1])):
            return 0
        return 1

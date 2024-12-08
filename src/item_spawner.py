import random
import time
from src.objects.coin import Coin


class ItemSpawner:
    def __init__(self):
        self.last_spawned_at = time.time()

    def spawn_coin(self, screen_w, screen_h, id):
        w = random.randrange(screen_w)
        h = random.randrange(screen_h)
        value = random.randint(2, 5)
        if time.time() - self.last_spawned_at > 3:
            self.last_spawned_at = time.time()
            return Coin(w, h, id, value)
        return None


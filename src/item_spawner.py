import random
import time
from src.objects.coin import Coin
from src.objects.med_kit import MedKit


class ItemSpawner:
    def __init__(self):
        self.last_spawned_coin_at = time.time()
        self.last_spawned_medkit_at = time.time()

    def spawn_item(self, screen_w, screen_h, id):
        items = []
        value = random.randint(2, 5)
        # TODO should refactor probably
        if time.time() - self.last_spawned_coin_at > 3:
            w = random.randrange(screen_w)
            h = random.randrange(screen_h)
            self.last_spawned_coin_at = time.time()
            items.append(Coin(w, h, id, value))
        if time.time() - self.last_spawned_medkit_at > 5:
            w = random.randrange(screen_w)
            h = random.randrange(screen_h)
            self.last_spawned_medkit_at = time.time()
            items.append(MedKit(w, h, id))
        return items


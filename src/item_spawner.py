import random
import time
from src.objects.coin import Coin
from src.objects.med_kit import MedKit
from src.objects.hunter_npc import HunterNPC


class ItemSpawner:
    def __init__(self):
        self.last_spawned_coin_at = time.time()
        self.last_spawned_medkit_at = time.time()
        self.last_spawned_npc_at = time.time()

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
    
    def spawn_npc(self, id, screen_w, screen_h, vision_sensor, border_sensor, collision_sensor, game_stats):
        npc_created = False
        while not npc_created:
            x = random.randrange(screen_w)
            y = random.randrange(screen_h)
            new_npc = HunterNPC(
                id = id,
                x = x,
                y = y,
                speed = 50,
                vision_sensor = vision_sensor,
                border_sensor = border_sensor,
                character_collision_sensor = collision_sensor,
                game_stats = game_stats
            )

            if not len(collision_sensor.get_reading(new_npc)):
                npc_created = True
                return [new_npc]
        return []


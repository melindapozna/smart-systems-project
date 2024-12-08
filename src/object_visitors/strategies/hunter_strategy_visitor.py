from time import time

# Here a strategy for interacting with each object type can be implemented
# It will be triggered if it's the highest priority visible object

class HunterStrategyVisitor:
    def __init__(self, hunter):
        self.hunter = hunter

    def visit_player(self, player):
        # TODO bullet prediction
        self.hunter.look_at(player.pos)
        # Shoot a bullet if the previous shot was long enough ago
        if time() - self.hunter.prev_shot_time > self.hunter.fire_rate:
            self.hunter.bullet_ready = True

    def visit_basic_npc(self, basic_npc):
       self.hunter.look_at(basic_npc.pos)
       if time() - self.hunter.prev_shot_time > self.hunter.fire_rate:
           self.hunter.bullet_ready = True

    def visit_bullet(self, bullet):
        # TODO: dodge/block
        pass

    def visit_obstacle(self, obstacle):
        pass # TODO ? Not sure

    def visit_coin(self, coin):
        self.hunter.look_at(coin.pos)
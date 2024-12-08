from time import time

class HunterNPCCollisionVisitor:
    def __init__(self, hunter):
        self.hunter = hunter

    def visit_player(self, player):
        self.add_movement_constraints(player, 1)

    def visit_basic_npc(self, basic_npc):
        self.add_movement_constraints(basic_npc, 1)

    def visit_hunter(self, hunter):
        self.add_movement_constraints(hunter, 0)
        # TODO share information here

    def visit_bullet(self, bullet):
        # Note: taking damage can be moved here
        # self.basic_npc.take_damage(bullet.damage)
        pass

    def visit_obstacle(self, obstacle):
        self.add_movement_constraints(obstacle, 0)

    def visit_coin(self, coin):
        self.hunter.pick_up(coin)
        coin.alive = False

    def visit_medkit(self, medkit):
        self.hunter.heal(medkit)
        medkit.alive = False

    # call this in visit_basic_npc and visit_player
    def add_movement_constraints(self, object, damage):
        if time() - self.hunter.prev_collision_time > 0.5:
            self.hunter.prev_collision_time = time()
            self.hunter.take_damage(damage)

        vector_to_obstacle = object.pos - self.hunter.pos
        dist_to_obstacle = vector_to_obstacle.length()
        if dist_to_obstacle == 0:
            return  # What even is this case
        self.hunter.add_constraint(1 / dist_to_obstacle * vector_to_obstacle)
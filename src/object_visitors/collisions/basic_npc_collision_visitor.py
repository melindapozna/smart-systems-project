import time

class BasicNPCCollisionVisitor:
    def __init__(self, basic_npc):
        self.basic_npc = basic_npc

    def visit_player(self, player):
        self.add_movement_constraints(player, 1)

    def visit_basic_npc(self, basic_npc):
       self.add_movement_constraints(basic_npc, 1)
       self.communicate_with_npc(basic_npc)

    def visit_hunter(self, hunter):
        self.add_movement_constraints(hunter, 1)

    def visit_bullet(self, bullet):
        # Note: taking damage can be moved here
        # self.basic_npc.take_damage(bullet.damage)
        pass

    def visit_obstacle(self, obstacle):
        self.add_movement_constraints(obstacle, 0)

    def visit_coin(self, coin):
        self.basic_npc.pick_up(coin)
        coin.alive = False

    def visit_medkit(self, medkit):
        self.basic_npc.heal(medkit)
        medkit.alive = False

    # call this in visit_basic_npc and visit_player
    def add_movement_constraints(self, object, damage):
        if time.time() - self.basic_npc.prev_collision_time > 0.5:
            self.basic_npc.prev_collision_time = time.time()
            self.basic_npc.take_damage(damage)

        vector_to_obstacle = object.pos - self.basic_npc.pos
        dist_to_obstacle = vector_to_obstacle.length()
        if dist_to_obstacle == 0:
            return  # What even is this case
        self.basic_npc.add_constraint(1 / dist_to_obstacle * vector_to_obstacle)

    # communication between two NPC (didn't know what info they can share, so now they can heal each other for example)   
    def communicate_with_npc(self, other_npc):
        if time.time() - self.basic_npc.prev_communication_time > 0.5:
            self.basic_npc.prev_communication_time = time.time()
            self.basic_npc.hp = 50
            other_npc.hp = 50

            print(f"{self.basic_npc.id} and {other_npc.id} have been healed to 50 HP.")
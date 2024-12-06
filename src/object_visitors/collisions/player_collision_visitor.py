class PlayerCollisionVisitor:
    def __init__(self, player):
        self.player = player

    def visit_player(self, player):
        pass

    def visit_basic_npc(self, basic_npc):
        vector_to_obstacle = basic_npc.pos - self.player.pos
        dist_to_obstacle = vector_to_obstacle.length()
        if dist_to_obstacle == 0:
            return  # What even is this case
        self.player.add_constraint(1 / dist_to_obstacle * vector_to_obstacle)

    def visit_bullet(self, bullet):
        self.player.take_damage(bullet.damage)
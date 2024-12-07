class PlayerCollisionVisitor:
    def __init__(self, player):
        self.player = player

    def visit_player(self, player):
        pass

    def visit_basic_npc(self, basic_npc):
        self.thing(basic_npc)

    def visit_bullet(self, bullet):
        # Note: taking damage can be moved here
        # self.player.take_damage(bullet.damage)
        pass

    def visit_obstacle(self, obstacle):
       self.thing(obstacle)

    def thing(self, object):
        vector_to_obstacle = object.pos - self.player.pos
        dist_to_obstacle = vector_to_obstacle.length()
        if dist_to_obstacle == 0:
            return
        self.player.add_constraint(1 / dist_to_obstacle * vector_to_obstacle)
class BulletCollisionVisitor:
    def __init__(self, bullet):
        self.bullet = bullet

    def visit_player(self, player):
        player.take_damage(self.bullet.damage)
        self.bullet.alive = False

    def visit_basic_npc(self, basic_npc):
        basic_npc.take_damage(self.bullet.damage)
        self.bullet.alive = False

    def visit_hunter(self, hunter):
        hunter.take_damage(self.bullet.damage)
        self.bullet.alive = False

    def visit_bullet(self, bullet):
        self.bullet.alive = False

    def visit_obstacle(self, obstacle):
        self.bullet.alive = False

    def visit_coin(self):
        pass
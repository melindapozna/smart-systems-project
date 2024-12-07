class ShootingVisitor:
    def __init__(self, collision_sensor, id_provider):
        self.collision_sensor = collision_sensor
        self.id_provider = id_provider

    def visit_player(self, player):
        return None # TODO change to actual shooting probably

    def visit_basic_npc(self, basic_npc):
        if basic_npc.bullet_ready:
            return basic_npc.shoot_bullet(
                collision_sensor=self.collision_sensor,
                bullet_id=self.id_provider.provide_id()
            )
        return None

    def visit_bullet(self, bullet):
        return None # TODO maybe the bullets split or something idk

    def visit_obstacle(self, obstacle):
        # obstacles don't shoot
        return None

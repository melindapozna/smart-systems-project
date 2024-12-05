class ShootingVisitor:
    def __init__(self, collision_sensor):
        self.collision_sensor = collision_sensor
        # TODO move this out of here
        self.radius = {
            "player": 10,
            "basic_npc": 10,
            "bullet": 2
        }

    def visit_player(self, player):
        return None # TODO change to actual shooting probably

    def visit_basic_npc(self, basic_npc):
        if basic_npc.bullet_ready:
            return basic_npc.shoot_bullet(
                offset=self.radius["basic_npc"] + 2 * self.radius["bullet"],
                collision_sensor=self.collision_sensor
            )
        return None

    def visit_bullet(self, bullet):
        return None # TODO maybe the bullets split or something idk

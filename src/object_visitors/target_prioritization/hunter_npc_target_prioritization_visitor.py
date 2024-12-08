class HunterNpcTargetPrioritizationVisitor:
    def __init__(self, hunter_npc):
        self.hunter = hunter_npc

    def visit_player(self, player):
        if self.hunter.hp <= 25 and player.hp > 50:
            return 2
        return 10

    def visit_basic_npc(self, basic_npc):
       return 4

    def visit_bullet(self, bullet):
        if self.hunter.hp < 15:
            return 10
        return 1

    def visit_obstacle(self, obstacle):
        return 0

    def visit_coin(self, coin):
        return 5

    def visit_medkit(self, medkit):
        if self.hunter.hp <= 25:
            return 10
        return 3

    def visit_hunter(self, hunter):
        if self.hunter.ready_to_update and hunter.ready_to_update:
            return 8
        return 0

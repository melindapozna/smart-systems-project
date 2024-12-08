# TODO Actual target prioritization based on the NPC parameters can be done here
# E.g. if player hp is low, prioritize the player
class HunterNpcTargetPrioritizationVisitor:
    def __init__(self, hunter_npc):
        self.hunter = hunter_npc

    def visit_player(self, player):
        return 10

    def visit_basic_npc(self, basic_npc):
       return 4

    def visit_bullet(self, bullet):
        return 1

    def visit_obstacle(self, obstacle):
        return 0

    def visit_coin(self, coin):
        return 5

    def visit_medkit(self, medkit):
        return 3

    def visit_hunter(self, hunter):
        return 2

class CharacterCollisionSensor:
    def __init__(self, player, npcs):
        # TODO move the radius outside of this class
        self.radius = {
            "player": 10,
            "basic_npc": 10,
            "bullet": 2
        }
        self.player = player
        self.npcs = npcs

    def get_reading(self, position):
        if position.distance_to(self.player.pos) < self.radius["player"]:
            return self.player
        for npc in self.npcs:
            if position.distance_to(npc.pos) < self.radius["basic_npc"]:
                return npc
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

    def get_reading(self, object):
        if object.pos.distance_to(self.player.pos) < self.radius["player"]:
            return self.player
        for npc in self.npcs:
            try:

                if object.pos.distance_to(npc.pos) < self.radius["basic_npc"] and npc.id != object.id:
                    return npc

            # To avoid error on collision with bullets, as they have no IDs implemented
            # TODO
            except AttributeError:
                return None
        return None
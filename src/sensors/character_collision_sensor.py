class CharacterCollisionSensor:
    def __init__(self, player, npcs):
        self.player = player
        self.npcs = npcs

    def get_reading(self, object):
        if object.pos.distance_to(self.player.pos) < self.player.radius:
            return self.player
        for npc in self.npcs:
            try:

                if object.pos.distance_to(npc.pos) < npc.radius and npc.id != object.id:
                    return npc

            # To avoid error on collision with bullets, as they have no IDs implemented
            # TODO
            except AttributeError:
                return None
        return None
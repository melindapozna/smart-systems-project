class CharacterCollisionSensor:
    def __init__(self, player, npcs):
        self.player = player
        self.npcs = npcs

    def get_reading(self, object):
        collided_objects = []
        try:
            if self.player.id != object.id and object.pos.distance_to(self.player.pos) < self.player.radius + object.radius:
                collided_objects.append(self.player)
        except AttributeError:
            return None
        for npc in self.npcs:
            try:
                if npc.id != object.id and object.pos.distance_to(npc.pos) <= npc.radius + object.radius:
                    collided_objects.append(npc)
            # To avoid error on collision with bullets, as they have no IDs implemented
            # TODO
            except AttributeError:
                return None
        return collided_objects
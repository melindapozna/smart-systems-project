class CharacterCollisionSensor:
    def __init__(self, player, npcs, bullets, obstacles, items):
        self.player = player
        self.npcs = npcs
        self.bullets = bullets
        self.obstacles = obstacles
        self.items = items

    def get_all_objects(self):
        return [self.player] + self.npcs + self.bullets + self.obstacles + self.items

    def get_reading(self, object):
        collided_objects = [x for x in self.get_all_objects()
                            if x.id != object.id
                            and object.pos.distance_to(x.pos) <= x.radius + object.radius]
        return collided_objects

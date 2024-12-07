class CharacterCollisionSensor:
    def __init__(self, player, npcs, bullets, obstacles):
        self.player = player
        self.npcs = npcs
        self.bullets = bullets
        self.obstacles = obstacles

    def get_reading(self, object):
        collided_objects = []
        if self.player.id != object.id and object.pos.distance_to(self.player.pos) < self.player.radius + object.radius:
            collided_objects.append(self.player)
        for npc in self.npcs:
            if npc.id != object.id and object.pos.distance_to(npc.pos) <= npc.radius + object.radius:
                collided_objects.append(npc)
        for obstacle in self.obstacles:
            if obstacle.id !=  object.id and object.pos.distance_to(obstacle.pos) <= obstacle.radius + object.radius:
                collided_objects.append(obstacle)
        return collided_objects

class Obstacle:
    def __init__(self, id, radius, pos):
        self.id = id
        self.radius = radius
        self.pos = pos

    def accept(self, visitor):
        return visitor.visit_obstacle(self)

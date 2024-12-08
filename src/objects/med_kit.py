from pygame import Vector2

class MedKit:
    def __init__(self, w, h, id):
        self.pos = Vector2(w, h)
        self.value = 5
        self.id = id
        self.alive = True
        self.radius = 5

    def accept(self, visitor):
        return visitor.visit_medkit(self)
from pygame import Vector2

class Coin:
    def __init__(self, w, h, id, value=1):
        self.pos = Vector2(w, h)
        self.value = value
        self.id = id
        self.alive = True
        self.radius = 3

    def accept(self, visitor):
        return visitor.visit_coin(self)
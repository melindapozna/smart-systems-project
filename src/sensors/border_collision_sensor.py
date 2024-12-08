from pygame import Vector2

class BorderCollisionSensor:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def get_reading(self, character):
        result = []
        if character.pos.x <= character.radius:
            result.append(Vector2(-1, 0))
        if character.pos.y <= character.radius:
            result.append(Vector2(0, -1))
        if character.pos.x >= self.w - character.radius:
            result.append(Vector2(1, 0))
        if character.pos.y >= self.h - character.radius:
            result.append(Vector2(0, 1))

        return result
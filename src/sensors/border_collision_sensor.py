class BorderCollisionSensor:
    def __init__(self, w, h):
        # screen width and height
        self.w = w
        self.h = h

    def get_reading(self, position):
        return not ((0 < position.x < self.w) and
                    (0 < position.y < self.h))
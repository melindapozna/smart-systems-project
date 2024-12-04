from pygame import Vector2


class BasicNPC:
    def __init__(self, x, y, speed, sensor):
        self.pos = Vector2(x, y)
        self.speed = speed
        self.dir = Vector2(0, 1)
        self.sensor = sensor
        self.hp = 50
        self.alive = True

    def move(self, dt):
        self.look_at(self.sensor.get_reading())
        self.pos += self.speed * dt * self.dir

    def look_at(self, position):
        dist = self.pos.distance_to(position)
        if dist == 0:
            return
        self.dir = (position - self.pos) / dist

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False



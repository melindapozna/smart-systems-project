class PlayerPositionSensor:
    def __init__(self, player):
        self.player = player

    def get_reading(self):
        return self.player.pos

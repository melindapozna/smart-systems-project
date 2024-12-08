import pygame

class DrawVisitor:
    def __init__(self, screen):
        self.screen = screen

    def visit_player(self, player):
        pygame.draw.circle(self.screen, "green", player.pos, player.radius)

    def visit_basic_npc(self, basic_npc):
        pygame.draw.circle(self.screen, "red", basic_npc.pos, basic_npc.radius)

    def visit_bullet(self, bullet):
        pygame.draw.circle(self.screen, "orange", bullet.pos, bullet.radius)

    def visit_obstacle(self, obstacle):
        pygame.draw.circle(self.screen, "darkgreen", obstacle.pos, obstacle.radius)

    def visit_coin(self, coin):
        pygame.draw.circle(self.screen, "gold", coin.pos, coin.radius)

    def visit_medkit(self, medkit):
        pygame.draw.circle(self.screen, "cyan", medkit.pos, medkit.radius)

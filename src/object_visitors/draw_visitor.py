import pygame
from math import pi


class DrawVisitor:
    def __init__(self, screen):
        self.screen = screen

    def visit_player(self, player):
        pygame.draw.circle(self.screen, "green", player.pos, player.radius)

    def visit_basic_npc(self, basic_npc):
        pygame.draw.line(self.screen, "black", basic_npc.pos,
                         basic_npc.pos + basic_npc.vision_radius * basic_npc.dir.rotate(20))
        pygame.draw.line(self.screen, "black", basic_npc.pos,
                         basic_npc.pos + basic_npc.vision_radius * basic_npc.dir.rotate(-20))
        pygame.draw.line(self.screen, "black", basic_npc.pos + basic_npc.vision_radius * basic_npc.dir.rotate(20),
                         basic_npc.pos + basic_npc.vision_radius * basic_npc.dir.rotate(-20))
        pygame.draw.circle(self.screen, "red", basic_npc.pos, basic_npc.radius)

    def visit_hunter(self, hunter):
        pos = hunter.pos
        dir_left = hunter.dir.rotate(hunter.vision_angle / 2)
        dir_right = hunter.dir.rotate(-hunter.vision_angle / 2)
        vradius = hunter.vision_radius
        pygame.draw.line(self.screen, "white", pos + hunter.radius * dir_right, pos + vradius * dir_right)
        pygame.draw.line(self.screen, "white", pos + hunter.radius * dir_left, pos + vradius * dir_left)
        pygame.draw.arc(self.screen,
                        "white",
                        pygame.Rect(pos.x - vradius, pos.y - vradius, 2 * vradius, 2 * vradius),
                        dir_left.angle_to(pygame.Vector2(1, 0)) / 180 * pi,
                        dir_right.angle_to(pygame.Vector2(1, 0)) / 180 * pi)
        pygame.draw.circle(self.screen, "purple", hunter.pos, hunter.radius)

    def visit_bullet(self, bullet):
        pygame.draw.circle(self.screen, "orange", bullet.pos, bullet.radius)

    def visit_obstacle(self, obstacle):
        pygame.draw.circle(self.screen, "darkgreen", obstacle.pos, obstacle.radius)

    def visit_coin(self, coin):
        pygame.draw.circle(self.screen, "yellow", coin.pos, coin.radius)

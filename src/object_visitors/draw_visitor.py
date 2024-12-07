import pygame
from pygame import Vector2

class DrawVisitor:
    def __init__(self, screen):
        self.radius = {
            "player": 10,
            "basic_npc": 10,
            "bullet": 2,
            "npc_vision": 400
        }
        self.screen = screen

    def visit_player(self, player):
        pygame.draw.circle(self.screen, "green", player.pos, self.radius["player"])

    def visit_basic_npc(self, basic_npc):
        pygame.draw.line(self.screen, "black", basic_npc.pos, basic_npc.pos + self.radius["npc_vision"]*basic_npc.dir.rotate(20))
        pygame.draw.line(self.screen, "black", basic_npc.pos, basic_npc.pos + self.radius["npc_vision"]*basic_npc.dir.rotate(-20))
        pygame.draw.line(self.screen, "black", basic_npc.pos + self.radius["npc_vision"]*basic_npc.dir.rotate(20), basic_npc.pos + self.radius["npc_vision"]*basic_npc.dir.rotate(-20))
        pygame.draw.circle(self.screen, "red", basic_npc.pos, self.radius["basic_npc"])


    def visit_bullet(self, bullet):
        pygame.draw.circle(self.screen, "yellow", bullet.pos, self.radius["bullet"])
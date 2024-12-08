import pygame

class MovementVisitor:
    def __init__(self):
        self.dt = 0

    def visit_player(self, player):
        keys = pygame.key.get_pressed()
        player_direction = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            player_direction += pygame.Vector2(0, -1)
        if keys[pygame.K_s]:
            player_direction += pygame.Vector2(0, 1)
        if keys[pygame.K_a]:
            player_direction += pygame.Vector2(-1, 0)
        if keys[pygame.K_d]:
            player_direction += pygame.Vector2(1, 0)
        if player_direction.length() > 1:
            player_direction /= player_direction.length()
        player.move(player_direction, self.dt)

    def visit_basic_npc(self, basic_npc):
        pass
        basic_npc.action(self.dt)
        #basic_npc.move(self.dt)
        # TODO maybe move it elsewhere?
        # if npc.bullet_ready:
        #     bullets.append(npc.shoot_bullet(
        #         offset=radius["basic_npc"] + 2 * radius["bullet"],
        #         collision_sensor=PlayerCollisionSensor())
        #     )

    def visit_bullet(self, bullet):
        bullet.move(self.dt)

    def visit_obstacle(self, obstacle):
        # obstacles don't move
        pass

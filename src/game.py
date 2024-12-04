import pygame
from time import sleep

from src.player import Player
from src.npc_basic import BasicNPC


class BorderCollisionSensor:
    def get_reading(self, position):
        return not ((0 < position.x < screen.get_width()) and
                (0 < position.y < screen.get_height()))


class PlayerPositionSensor:
    def get_reading(self):
        return player.pos

class PlayerCollisionSensor:
    def get_reading(self, position):
        if position.distance_to(player.pos) < 35:
            return player
        # for npc in npcs:
            # if position.distance_to(npc.pos) < 35:
                # return npc

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player = Player(screen.get_width() / 2, screen.get_height() / 2, BorderCollisionSensor())

npcs = []
npcs.append(BasicNPC(screen.get_width() / 4,
                     screen.get_height() / 4,
                     220,
                     PlayerPositionSensor(),
                     BorderCollisionSensor()))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "green", player.pos, 30)

    for npc in npcs:
        if npc.type == "Basic":
            pygame.draw.circle(screen, "red", npc.pos, 30)
            if npc.bullet_ready:
                npcs.append(npc.shoot_bullet(PlayerCollisionSensor()))
        if npc.type == "Bullet":
            pygame.draw.circle(screen, "yellow", npc.pos, 5)
        npc.move(dt)

    if not player.alive:
        screen.fill("red")
        text = pygame.font.Font("freesansbold.ttf", 32).render("Game Over", True, "black")
        screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, screen.get_height() / 2))
        pygame.display.flip()
        sleep(1)
        running = False
    npcs = list(filter(lambda x: x.alive, npcs))

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
    player.move(player_direction, dt)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()

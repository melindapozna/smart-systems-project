import pygame

from src.player import Player
from src.npc_basic import BasicNPC


class PlayerSensor:
    @staticmethod
    def get_reading():
        return player.pos

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

sensor = PlayerSensor()
player = Player(screen.get_width() / 2, screen.get_height() / 2)

npc = BasicNPC(screen.get_width() / 4, screen.get_height() / 4, 220, sensor)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "green", player.pos, 40)
    pygame.draw.circle(screen, "red", npc.pos, 40)

    npc.move(dt)

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

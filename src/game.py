import pygame
from time import sleep

from objects import *
from object_visitors import *
from sensors import *
from src.id_provider import IdProvider


class Game:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0     # delta time: seconds elapsed since the last frame
        self.id_provider = IdProvider()
        self.border_sensor = BorderCollisionSensor(self.screen.get_width(), self.screen.get_height())


        self.player = Player(self.next_id(), self.screen.get_width() / 2, self.screen.get_height() / 2, self.border_sensor)
        self.npcs = []
        self.bullets = []
        self.font = pygame.font.SysFont("freesansbold.ttf", 25)

        self.player_position_sensor = PlayerPositionSensor(self.player)
        self.collision_sensor = CharacterCollisionSensor(self.player, self.npcs, self.bullets)
        # TODO CHANGE!!!
        self.player.collision_sensor = self.collision_sensor

        # initialize an NPC
        self.npcs.append(BasicNPC(self.next_id(),
                                  self.screen.get_width() / 2,
                                  self.screen.get_height() / 4,
                                  90,
                                  self.player_position_sensor,
                                  self.border_sensor,
                                  self.collision_sensor))
        self.npcs.append(BasicNPC(self.next_id(),
                                  self.screen.get_width() / 3,
                                  self.screen.get_height() / 3,
                                  90,
                                  self.player_position_sensor,
                                  self.border_sensor,
                                  self.collision_sensor))

        self.draw_visitor = DrawVisitor(self.screen)
        self.movement_visitor = MovementVisitor()
        self.shooting_visitor = ShootingVisitor(self.collision_sensor, self.id_provider)

    def next_id(self):
        return self.id_provider.provide_id()

    def run(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("purple")
            keys = pygame.key.get_pressed()

            self.movement_visitor.dt = self.dt
            self.player.accept(self.draw_visitor)
            self.player.accept(self.movement_visitor)

            new_bullet = self.player.accept(self.shooting_visitor)
            if new_bullet:
                self.bullets.append(new_bullet)

            for npc in self.npcs:
                npc.accept(self.draw_visitor)
                npc.accept(self.movement_visitor)
                new_bullet = npc.accept(self.shooting_visitor)
                if new_bullet:
                    self.bullets.append(new_bullet)
                    
                npc.update_conversation(self.player.pos, keys)
                self.draw_visitor.render_conversation(npc, self.screen)
                        

            for bullet in self.bullets:
                bullet.accept(self.draw_visitor)
                bullet.accept(self.movement_visitor)

            if not self.player.alive:
                self.screen.fill("red")
                text = pygame.font.Font("freesansbold.ttf", 32).render("Game Over", True, "black")
                self.screen.blit(text,
                                 (self.screen.get_width() / 2 - text.get_width() / 2, self.screen.get_height() / 2))
                pygame.display.flip()
                sleep(1)
                self.running = False

            # Slice assignment so that the external references to the lists remain valid
            self.npcs[:] = list(filter(lambda x: x.alive, self.npcs))
            self.bullets[:] = list(filter(lambda x: x.alive, self.bullets))

            # Render lives to the screne 
            self.draw_visitor.render_lives(self.player)

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

import random
import pygame
from time import sleep

from objects import *
from object_visitors import *
from sensors import *
from src.id_provider import IdProvider
from src.game_stats import GameStats

from src.objects.hunter_npc import HunterNPC
from src.item_spawner import ItemSpawner


class Game:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.w = 1280
        self.h = 720
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0     # delta time: seconds elapsed since the last frame
        self.id_provider = IdProvider()
        self.border_sensor = BorderCollisionSensor(self.w, self.h)
        self.game_stats = GameStats()
        self.player = Player(self.next_id(), self.w / 2, self.h / 2, self.border_sensor, self.game_stats)
        self.npcs = []
        self.bullets = []
        self.obstacles = []
        self.items = []

        self.player_position_sensor = PlayerPositionSensor(self.player)
        self.collision_sensor = CharacterCollisionSensor(self.player, self.npcs, self.bullets, self.obstacles, self.items)
        # TODO CHANGE!!!
        self.player.collision_sensor = self.collision_sensor
        self.vision_sensor = VisionSensor(self.player, self.npcs, self.bullets, self.obstacles, self.items)

        # initialize an NPC
        self.npcs.append(HunterNPC(self.next_id(),
                                  3 * self.w / 4,
                                  3 * self.h / 4,
                                  50,
                                  self.vision_sensor,
                                  self.border_sensor,
                                  self.collision_sensor,
                                  self.game_stats))

        self.npcs.append(HunterNPC(self.next_id(),
                                   3 * self.w / 5,
                                   3 * self.h / 5,
                                   50,
                                   self.vision_sensor,
                                   self.border_sensor,
                                   self.collision_sensor,
                                   self.game_stats))

        # generate 10 objects in random size and position if they don't already collide with something
        for i in range(10):
            radius = random.randint(10, 40)
            object_appendable = False
            while not object_appendable:
                position = pygame.Vector2(random.randrange(self.w),
                                          random.randrange(self.h))
                curr_obstacle = Obstacle(self.next_id(),
                                               radius,
                                               position)
                if not len(self.collision_sensor.get_reading(curr_obstacle)):
                    self.obstacles.append(curr_obstacle)
                    object_appendable = True


        self.draw_visitor = DrawVisitor(self.screen)
        self.movement_visitor = MovementVisitor()
        self.shooting_visitor = ShootingVisitor(self.collision_sensor, self.id_provider)
        self.difficulty_manager = DifficultyManager()

        self.item_spawner = ItemSpawner()

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

            self.screen.fill("sienna4")

            self.movement_visitor.dt = self.dt

            #handle difficulty changes during the run
            npc_accuracy = self.game_stats.get_basic_npc_accuracy()
            if npc_accuracy < 0.1:
                self.basic_npc_difficulty_level = min(self.difficulty_manager.basic_npc_difficulty_level + 1, self.difficulty_manager.basic_npc_max_difficulty)
                for npc in self.npcs:
                    self.difficulty_manager.visit_basic_npc(npc)
            player_hit_treshold = self.game_stats.player_hit_treshold()
            if player_hit_treshold:
                self.player_difficulty_level = min(self.difficulty_manager.player_difficulty_level + 1, self.difficulty_manager.player_max_difficulty)
                self.basic_npc_difficulty_level = min(self.difficulty_manager.basic_npc_difficulty_level - 1, 1 )
                self.difficulty_manager.visit_player(self.player)
                for npc in self.npcs:
                    self.difficulty_manager.visit_basic_npc(npc)

            new_bullet = self.player.accept(self.shooting_visitor)
            if new_bullet:
                self.bullets.append(new_bullet)

            for npc in self.npcs:
                npc.accept(self.draw_visitor)
                npc.accept(self.movement_visitor)
                new_bullet = npc.accept(self.shooting_visitor)
                if new_bullet:
                    self.bullets.append(new_bullet)

            self.player.accept(self.draw_visitor)
            self.player.accept(self.movement_visitor)

            for bullet in self.bullets:
                bullet.accept(self.draw_visitor)
                bullet.accept(self.movement_visitor)

            for obstacle in self.obstacles:
                obstacle.accept(self.draw_visitor)

            new_items = [item for item in self.item_spawner.spawn_item(self.screen.get_width(), self.screen.get_height(), self.next_id())
                         if not len(self.collision_sensor.get_reading(item))]
            # only append it if it doesn't collide with something
            if len(new_items):
                for item in new_items:
                    self.items.append(item)

            for item in self.items:
                item.accept(self.draw_visitor)

            if not self.player.alive:
                self.screen.fill("red")
                text = pygame.font.Font("freesansbold.ttf", 32).render("Game Over", True, "black")
                self.screen.blit(text,
                                 (self.w / 2 - text.get_width() / 2, self.h / 2))
                pygame.display.flip()
                sleep(1)
                self.running = False

            # Slice assignment so that the external references to the lists remain valid
            self.npcs[:] = list(filter(lambda x: x.alive, self.npcs))
            self.bullets[:] = list(filter(lambda x: x.alive, self.bullets))
            self.items[:] = list(filter(lambda x: x.alive, self.items))

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

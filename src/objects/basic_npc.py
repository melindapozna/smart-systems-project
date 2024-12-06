import pygame
from pygame import Vector2
from src.objects.bullet import Bullet
from src.object_visitors.collisions.basic_npc_collision_visitor import BasicNPCCollisionVisitor
import time


class BasicNPC:
    def __init__(self, id, x, y, speed, player_sensor, border_sensor, character_collision_sensor):
        self.id = id
        self.radius = 10
        self.pos = Vector2(x, y)
        self.speed = speed
        self.dir = Vector2(0, 1)
        self.player_sensor = player_sensor
        self.border_sensor = border_sensor
        self.character_collision_sensor = character_collision_sensor
        self.hp = 50
        self.alive = True
        self.damage = 10
        self.bullet_radius = 2
        self.bullet_ready = False
        self.prev_shot_time = time.time()
        self.collided = False
        self.prev_collision_time = time.time()
        # Directions in which the NPC can't move
        self.constraints = []
        self.collision_visitor = BasicNPCCollisionVisitor(self)

        # Added communication
        self.dialogue = [
            "Hello, player!",
            "Let's start our fight.",
            "Good luck!"
        ]
        self.is_in_conversation = False
        self.conversation_index = 0
        self.last_key_press_time = 0
        self.key_debounce_delay = 0.2
        self.conversation_finished = False

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def process_constraints(self, speed_vector):
        for constraint in self.constraints:
            normal_component = speed_vector.dot(constraint)
            if normal_component > 0:
                speed_vector -= normal_component * constraint
        self.constraints = []
        return speed_vector

    def move(self, dt):
        if not self.is_in_conversation:
            colliding_objects = self.character_collision_sensor.get_reading(self)
            if colliding_objects:
                for colliding_object in colliding_objects:
                    colliding_object.accept(self.collision_visitor)
            self.look_at(self.player_sensor.get_reading())
            speed_vector = self.speed * self.dir
            speed_vector = self.process_constraints(speed_vector)

            self.pos += dt * speed_vector

            # Shoot a bullet if the previous shot was at least 1 second ago
            if time.time() - self.prev_shot_time > 1:
                self.bullet_ready = True

            # Kill the NPC if it reaches the border
            if self.border_sensor.get_reading(self.pos):
                self.alive = False

    # make the npc face a target position
    def look_at(self, position):
        dist = self.pos.distance_to(position)
        if dist == 0:
            return
        self.dir = (position - self.pos) / dist

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def shoot_bullet(self, collision_sensor, bullet_id):
        if not self.is_in_conversation:
            self.bullet_ready = False
            self.prev_shot_time = time.time()
            # offset: radius of the shooter to avoid bullet collision with the shooter itself
            offset = self.radius + self.bullet_radius
            bullet_pos = self.pos + offset * self.dir
            return Bullet(bullet_pos, self.dir, self.damage, self.bullet_radius, collision_sensor, bullet_id)

    def collide(self, obstacle_pos):
        # Take damage on all collisons
        # TODO move into a visitor
        pass

    def accept(self, visitor):
        return visitor.visit_basic_npc(self)
    
    def update_conversation(self, player_pos, keys):
        if not self.conversation_finished and not self.is_in_conversation:
            distance = self.pos.distance_to(player_pos)
            if distance < 100:  # Trigger conversation if player is close enough
                self.start_conversation()

        if self.is_in_conversation:
            current_time = time.time()
            if keys[pygame.K_SPACE] and current_time - self.last_key_press_time > self.key_debounce_delay:
                self.advance_dialogue()
                self.last_key_press_time = current_time

    def start_conversation(self):
        self.is_in_conversation = True
        self.conversation_index = 0

    def advance_dialogue(self):
        self.conversation_index += 1
        if self.conversation_index >= len(self.dialogue):
            print("hereeeeeee")
            self.end_conversation()

    def end_conversation(self):
        # Reset NPC behavior after conversation ends
        self.is_in_conversation = False
        self.conversation_finished = True

    # maybe it is not supposed to be in this file 
    def draw_text(self, screen, text, x, y, font_size):
        font = pygame.font.SysFont('Arial', font_size)
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))

    def render_conversation(self, screen):
        if self.is_in_conversation and self.conversation_index < len(self.dialogue):
            box_width = screen.get_width() - 150
            box_height = 100
            box_x = 50
            box_y = screen.get_height() - box_height - 30
            pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  
            pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)
            self.draw_text(screen, self.dialogue[self.conversation_index], box_x + 20, box_y + 30, 30)
            prompt_text = "* Press SPACE to continue *"
            prompt_y = box_y - 30  # Position slightly above the dialogue box
            self.draw_text(screen, prompt_text, box_x + 20, prompt_y, 18)


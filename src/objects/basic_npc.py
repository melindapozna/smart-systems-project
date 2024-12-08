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
        self.prev_communication_time = time.time()
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
        self.text_displayed_at = None
        self.conversation_duration = 2
        self.conversation_finished = False
        self.dialogue_transition_start_time = None 
        self.dialogue_transition_duration = 0.5  
        self.transitioning = False

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

    def start_conversation(self):
        self.is_in_conversation = True
        self.conversation_index = 0
        self.text_displayed_at = time.time() 

    def advance_dialogue(self):
        self.conversation_index += 1
        if self.conversation_index >= len(self.dialogue):
            self.start_dialogue_transition()
            self.end_conversation()
        else:
            self.text_displayed_at = time.time() 

    def end_conversation(self):
        # Reset NPC behavior after conversation ends
        self.is_in_conversation = False
        self.conversation_finished = True
        self.text_displayed_at = None
        
    
    # dialogue transition
    def start_dialogue_transition(self):
        self.transitioning = True
        self.dialogue_transition_start_time = time.time()

    def is_in_transition(self):
        if not self.transitioning:
            return False
        elapsed_time = time.time() - self.dialogue_transition_start_time
        if elapsed_time > self.dialogue_transition_duration:
            self.transitioning = False
            return False
        return True

from pygame import Vector2

from src.object_visitors.collisions.basic_npc_collision_visitor import BasicNPCCollisionVisitor
from src.object_visitors.collisions.hunter_npc_collision_visitor import HunterNPCCollisionVisitor
from src.object_visitors.strategies.hunter_strategy_visitor import HunterStrategyVisitor
from src.object_visitors.target_prioritization.hunter_npc_target_prioritization_visitor import \
    HunterNpcTargetPrioritizationVisitor
from src.objects.bullet import Bullet
import time


class HunterNPC:
    def __init__(self, id, x, y, speed, vision_sensor, border_sensor, character_collision_sensor, game_stats):
        self.id = id
        self.radius = 10
        self.pos = Vector2(x, y)
        self.speed = speed
        self.dir = Vector2(0, 1)
        self.vision_sensor = vision_sensor
        self.border_sensor = border_sensor
        self.character_collision_sensor = character_collision_sensor
        self.hp = 50
        self.alive = True
        self.damage = 10
        self.bullet_radius = 2
        self.bullet_direction = Vector2(0, 1)
        # TODO change
        self.bullet_speed = 400
        self.bullet_ready = False
        self.prev_shot_time = time.time()
        self.vision_angle = 30
        self.vision_radius = 300
        self.prev_collision_time = time.time()
        # Directions in which the NPC can't move
        self.constraints = []
        self.items = []
        self.collision_visitor = HunterNPCCollisionVisitor(self)
        self.prioritization_visitor = HunterNpcTargetPrioritizationVisitor(self)
        self.strategy_visitor = HunterStrategyVisitor(self)
        self.fire_rate = 1
        self.game_stats = game_stats
        
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

        # for choosing strategy
        self.hits = [0, 0]
        self.shots = [0, 0]
        self.bullet_strategy = 0

        self.has_updates = False
        self.updates_buffer = []
        self.ready_to_update = False
        self.last_update_time = time.time()

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
        if self.has_updates:
            for hits, shots in self.updates_buffer:
                self.hits[0] = (self.hits[0] + hits[0]) / 2
                self.hits[1] = (self.hits[1] + hits[1]) / 2
                self.shots[0] = (self.shots[0] + shots[0]) / 2
                self.shots[1] = (self.shots[1] + shots[1]) / 2
            self.has_updates = False
            self.ready_to_update = False
            self.updates_buffer = []
            self.last_update_time = time.time()
        if time.time() - self.last_update_time > 5:
            self.ready_to_update = True


        colliding_objects = self.character_collision_sensor.get_reading(self)
        for colliding_object in colliding_objects:
            colliding_object.accept(self.collision_visitor)

        visible_objects = self.vision_sensor.get_reading(self)

        highest_priority = 0
        target = None
        if visible_objects:
            for obj in visible_objects:
                priority = obj.accept(self.prioritization_visitor)
                if priority > highest_priority:
                    target = obj
                    highest_priority = priority

        if highest_priority == 0:
            self.dir = self.dir.rotate(1)
            return
        else:
            target.accept(self.strategy_visitor)

        # Add border constraints
        for direction in self.border_sensor.get_reading(self):
            self.add_constraint(direction)

        speed_vector = self.speed * self.dir
        speed_vector = self.process_constraints(speed_vector)

        self.pos += dt * speed_vector

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

    def heal(self, medkit):
        self.hp += medkit.value

    def shoot_bullet(self, collision_sensor, bullet_id):
        self.bullet_ready = False
        self.prev_shot_time = time.time()
        # offset: radius of the shooter to avoid bullet collision with the shooter itself
        offset = self.radius + 2 * self.bullet_radius
        bullet_pos = self.pos + offset * self.dir
        self.game_stats.track_bullet_fired()
        return Bullet(bullet_pos,
                      self.bullet_direction,
                      self.damage,
                      self.bullet_radius,
                      collision_sensor,
                      bullet_id,
                      self,
                      self.bullet_strategy)

    def register_hit(self, strategy):
        self.hits[strategy] += 1

    def pick_up(self, item):
        self.items.append(item)

    def accept(self, visitor):
        return visitor.visit_hunter(self)
    
    def start_conversation(self):
        self.is_in_conversation = True
        self.conversation_index = 0
        self.text_displayed_at = time.time() 

    def advance_dialogue(self):
        self.conversation_index += 1
        if self.conversation_index >= len(self.dialogue):
            # self.start_dialogue_transition()
            self.end_conversation()
        else:
            self.text_displayed_at = time.time() 

    def end_conversation(self):
        # Reset NPC behavior after conversation ends
        self.is_in_conversation = False
        self.conversation_finished = True
        self.text_displayed_at = None
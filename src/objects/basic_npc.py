from pygame import Vector2
from objects.bullet import Bullet
import time
import math
import random

class BasicNPC:
    def __init__(self, x, y, speed, player_sensor, border_sensor):
        self.pos = Vector2(x, y)
        self.speed = speed
        self.dir = Vector2(0, 1)
        self.player_sensor = player_sensor
        self.border_sensor = border_sensor
        self.hp = 50
        self.alive = True
        self.damage = 20
        self.bullet_ready = False
        self.prev_shot_time = time.time()
        self.vision_radius= 400
        self.lastKnownLocation = None
        self.lastCheck = time.time()
        self.newSightDir = None
        self.rotateCounter = 0
    def action(self, dt):
        b_Point = self.pos + self.vision_radius*self.dir.rotate(20)
        c_Point = self.pos + self.vision_radius*self.dir.rotate(-20)
        character_position = self.player_sensor.get_reading()
        side_1 = self.pos.distance_to(b_Point)
        side_2 = self.pos.distance_to(c_Point)
        side_3 = c_Point.distance_to(b_Point)
        side_4 = self.pos.distance_to(character_position)
        side_5 = b_Point.distance_to(character_position)
        side_6 = c_Point.distance_to(character_position)
        p1 = (side_1 + side_2 + side_3) / 2
        p2 = (side_1 + side_4 + side_5) / 2
        p3 = (side_3 + side_5 + side_6) / 2
        p4 = (side_2 + side_4 + side_6) / 2
        area1 = math.sqrt(p1*(p1 - side_1)*(p1 - side_2) * (p1 - side_3))
        area2 = math.sqrt(p2*(p2 - side_1)*(p2 - side_4) * (p2 - side_5))
        area3 = math.sqrt(p3*(p3 - side_3)*(p3 - side_5) * (p3 - side_6))
        area4 = math.sqrt(p4*(p4 - side_2)*(p4 - side_4) * (p4 - side_6))
        if(area1 <= area2 + area3 + area4 + 10 and area1 >= area2 + area3 + area4 - 10):
            self.move(dt)
            self.lastKnownLocation = character_position.copy()
        else:
            self.searching(dt)
    
    def searching(self, dt):
        if(self.lastKnownLocation != None):
            self.look_at(self.lastKnownLocation)
            self.pos += self.speed * dt * self.dir
            if(self.pos.x > self.lastKnownLocation.x - 1 and self.pos.x < self.lastKnownLocation.x + 1 and
               self.pos.y > self.lastKnownLocation.y -1 and self.pos.y < self.lastKnownLocation.y + 1):
                self.lastKnownLocation = None
        else:
            if(time.time() - self.lastCheck > 3 and self.newSightDir == None):
                self.newSightDir = random.randint(0, 180)
                self.lastCheck = time.time()
            elif(self.newSightDir != None and time.time() - self.lastCheck):
                if(time.time() - self.lastCheck > 0.01):
                    self.dir = self.dir.rotate(1)
                    self.rotateCounter += 1
                    self.lastCheck = time.time()
                    if(self.rotateCounter >= self.newSightDir):
                        self.newSightDir = None
                        self.rotateCounter = 0
                

    def move(self, dt):
        self.look_at(self.player_sensor.get_reading())
        if(self.pos.distance_to(self.player_sensor.get_reading())>60):
            self.pos += self.speed * dt * self.dir
        elif(self.pos.distance_to(self.player_sensor.get_reading())<40):
            self.pos -= self.speed * dt * self.dir

        # Shoot a bullet if a second has passed since the last one
        if not self.bullet_ready and time.time() - self.prev_shot_time > 1:
            self.bullet_ready = True

        # Kill the NPC if it reaches the border
        if self.border_sensor.get_reading(self.pos):
            self.alive = False

    def look_at(self, position):
        dist = self.pos.distance_to(position)
        if dist == 0:
            return
        self.dir = (position - self.pos) / dist

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def shoot_bullet(self, offset, collision_sensor):
        self.bullet_ready = False
        self.prev_shot_time = time.time()

        return Bullet(self.pos + offset * self.dir, self.dir, self.damage, collision_sensor)

    def accept(self, visitor):
        return visitor.visit_basic_npc(self)

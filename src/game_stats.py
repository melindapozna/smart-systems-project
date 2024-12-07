import time

class GameStats:
    def __init__(self):
        self.basic_npc_shots_fired = 0
        self.basic_npc_shots_hit = 0
        self.last_hit_time = []
        self.hit_treshold_time = 10

    def track_bullet_fired(self):
        self.basic_npc_shots_fired += 1
    
    def get_basic_npc_accuracy(self):
        if self.basic_npc_shots_fired == 0:
            return 0
        return self.basic_npc_shots_hit / self.basic_npc_shots_fired
    
    def player_hit_treshold(self):
        curr_time = time.time()
        self.last_hit_time = [t for t in self.last_hit_time if curr_time - t <= self.hit_treshold_time] 
        return len(self.last_hit_time) >= 2
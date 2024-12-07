from src import objects
from src import game_stats
class DifficultyManager:
    def __init__(self, basic_npc_initial_difficulty=1, basic_npc_max_difficulty=10, player_initial_difficulty=1, player_max_difficulty=5):
        self.basic_npc_difficulty_level = basic_npc_initial_difficulty
        #We could also get rid of max difficulty
        self.npc_max_difficulty = basic_npc_max_difficulty
        self.player_difficulty_level = player_initial_difficulty
        self.player_max_difficulty = player_max_difficulty

    def visit_basic_npc(self, npc):
        npc.speed += self.basic_npc_difficulty_level * 6
        npc.fire_rate += self.basic_npc_difficulty_level * 0.1

    def visit_player(self, player):
        player.speed += self.player_difficulty_level * 10

    def adjust_basic_npc_difficulty(self, game_stats):
        npc_accuracy = game_stats.get_basic_npc_accuracy()
        if npc_accuracy < 0.1:
            self.basic_npc_difficulty_level = min(self.basic_npc_difficulty_level + 1, self.npc_max_difficulty) 

    def adjust_player_difficulty(self, game_stats):
        if game_stats.player_hit_treshold():
            self.player_difficulty_level = max(self.player_difficulty_level - 1, self.player_max_difficulty)

        

        
    
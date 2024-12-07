from src import objects
from src.game_stats import GameStats
class DifficultyManager:
    def __init__(self, basic_npc_initial_difficulty=1, basic_npc_max_difficulty=10, player_initial_difficulty=1, player_max_difficulty=5):
        self.basic_npc_difficulty_level = basic_npc_initial_difficulty
        #We could also get rid of max difficulty
        self.basic_npc_max_difficulty = basic_npc_max_difficulty
        self.player_difficulty_level = player_initial_difficulty
        self.player_max_difficulty = player_max_difficulty
    
    def visit_basic_npc(self, npc):
        npc.speed += self.basic_npc_difficulty_level * 0.1

    def visit_player(self, player):
        player.speed += self.player_difficulty_level * 0.15

        

        
    
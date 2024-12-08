from src import objects
from src.game_stats import GameStats
class DifficultyManager:
    def __init__(self, npc_initial_difficulty=1, npc_max_difficulty=10, player_initial_difficulty=1, player_max_difficulty=5):
        self.npc_difficulty_level = npc_initial_difficulty
        #We could also get rid of max difficulty
        self.npc_max_difficulty = npc_max_difficulty
        self.player_difficulty_level = player_initial_difficulty
        self.player_max_difficulty = player_max_difficulty
    
    def visit_npc(self, npc):
        npc.speed += self.npc_difficulty_level * 0.12

    def visit_decrease_npc_diff(self, npc):
        npc.speed -= self.npc_difficulty_level * 0.18

    def visit_bigger_decrease_npc_diff(self, npc):
        npc.speed -= self.npc_difficulty_level * 0.25

    def visit_player(self, player):
        player.speed += self.player_difficulty_level * 0.05


        

        
    
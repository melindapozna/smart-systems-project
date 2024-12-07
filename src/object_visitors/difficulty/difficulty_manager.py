from src import objects

class difficultyManager:
    def __init__(self, npc_initial_difficulty=1, npc_max_difficulty=10, player_initial_difficulty=1, player_max_difficulty=5):
        self.npc_difficulty_level = npc_initial_difficulty
        #We could also get rid of max difficulty
        self.npc_max_difficulty = npc_max_difficulty
        self.player_difficulty_level = player_initial_difficulty
        self_player_max_difficulty = player_max_difficulty

    def visit_basic_npc(self, npc):
        npc.speed += self.npc_difficulty_level * 6
        npc.fire_rate += self.npc_difficulty_level * 0.1

    def visit_player(self, player):
        player.speed += self.player_difficulty_level * 10

    def adjust_npc_difficulty(self, game_stats):
        #TODO implement game_stats to track stats
        if game_stats['npc_accuracy'] < 0.1:
            self.npc_difficulty_level = min(self.npc_difficulty_level + 1, self.npc_max_difficulty) 

    def adjust_player_difficulty(self, game_stats):
        if game_stats['player_hit_treshold'] is True:
            self.player_difficulty_level = max(self.player_difficulty_level + 1, self.player_max_difficulty)

        

        
    
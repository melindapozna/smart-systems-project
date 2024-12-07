import pygame
import time

class DrawVisitor:
    def __init__(self, screen, player_pos):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)  # Font for rendering text
        self.smaller_font = pygame.font.SysFont("Arial", 14)  # Font for rendering text
        self.player_pos = player_pos
        
    def visit_player(self, player):
        pygame.draw.circle(self.screen, "green", player.pos, player.radius)
        self.render_lives(player)

    def visit_basic_npc(self, basic_npc):
        pygame.draw.circle(self.screen, "red", basic_npc.pos, basic_npc.radius)
        self.update_conversation(basic_npc)
        self.render_conversation(basic_npc)
        self.render_npc_stats(basic_npc)

    def visit_bullet(self, bullet):
        pygame.draw.circle(self.screen, "yellow", bullet.pos, bullet.radius)
    
    
    def render_lives(self, player):
        # Render the player's remaining lives in the corner.
        lives_text = self.font.render(f"Lives: {player.hp}", True, "white")
        self.screen.blit(lives_text, (20, 20))
        
    # useless, but  wanted to see how it heals
    def render_npc_stats(self, npc):
        stats_text = f"HP: {npc.hp} | DMG: {npc.damage}"
        text_surface = self.smaller_font.render(stats_text, True, "white")
        text_position = npc.pos + pygame.Vector2(0, -npc.radius - 20)
        self.screen.blit(text_surface, (text_position.x, text_position.y))

    def render_conversation(self, npc):
        if npc.is_in_conversation and npc.conversation_index < len(npc.dialogue):
            box_width = self.screen.get_width() - 150
            box_height = 100
            box_x = 50
            box_y = self.screen.get_height() - box_height - 30
            pygame.draw.rect(self.screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  
            pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)
            self.draw_text(self.screen, npc.dialogue[npc.conversation_index], box_x + 20, box_y + 30, 30)
            prompt_text = "* Press SPACE to continue *"
            prompt_y = box_y - 30
            self.draw_text(self.screen, prompt_text, box_x + 20, prompt_y, 18)
   
    def update_conversation(self, npc):
        if not npc.conversation_finished and not npc.is_in_conversation:
            distance = npc.pos.distance_to(self.player_pos)
            if distance < 100:  # Trigger conversation if player is close enough
                npc.start_conversation()

        if npc.is_in_conversation:
            current_time = time.time()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and current_time - npc.last_key_press_time > npc.key_debounce_delay:
                npc.advance_dialogue()
                npc.last_key_press_time = current_time
                
    def draw_text(self, screen, text, x, y, font_size):
        font = pygame.font.SysFont('Arial', font_size)
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))
        
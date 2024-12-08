import pygame
import time
from math import pi


class DrawVisitor:
    def __init__(self, screen, player_pos):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24) 
        self.smaller_font = pygame.font.SysFont("Arial", 14)
        self.player_pos = player_pos
        
    def visit_player(self, player):
        pygame.draw.circle(self.screen, "green", player.pos, player.radius)
        self.render_player_stats(player)

    def visit_basic_npc(self, basic_npc):
        pygame.draw.line(self.screen, "black", basic_npc.pos,
                         basic_npc.pos + basic_npc.vision_radius * basic_npc.dir.rotate(20))
        pygame.draw.line(self.screen, "black", basic_npc.pos,
                         basic_npc.pos + basic_npc.vision_radius * basic_npc.dir.rotate(-20))
        pygame.draw.line(self.screen, "black", basic_npc.pos + basic_npc.vision_radius * basic_npc.dir.rotate(20),
                         basic_npc.pos + basic_npc.vision_radius * basic_npc.dir.rotate(-20))
        pygame.draw.circle(self.screen, "red", basic_npc.pos, basic_npc.radius)
        self.update_conversation(basic_npc)
        self.render_conversation(basic_npc)
        self.render_npc_stats(basic_npc)

    def visit_hunter(self, hunter):
        pos = hunter.pos
        dir_left = hunter.dir.rotate(hunter.vision_angle / 2)
        dir_right = hunter.dir.rotate(-hunter.vision_angle / 2)
        vradius = hunter.vision_radius
        pygame.draw.line(self.screen, "white", pos + hunter.radius * dir_right, pos + vradius * dir_right)
        pygame.draw.line(self.screen, "white", pos + hunter.radius * dir_left, pos + vradius * dir_left)
        pygame.draw.arc(self.screen,
                        "white",
                        pygame.Rect(pos.x - vradius, pos.y - vradius, 2 * vradius, 2 * vradius),
                        dir_left.angle_to(pygame.Vector2(1, 0)) / 180 * pi,
                        dir_right.angle_to(pygame.Vector2(1, 0)) / 180 * pi)
        pygame.draw.circle(self.screen, "purple", hunter.pos, hunter.radius)

    def visit_bullet(self, bullet):
        pygame.draw.circle(self.screen, "yellow", bullet.pos, bullet.radius)
    
    # Render the player's remaining lives and items in the corner.
    def render_player_stats(self, player):
        stats_text = f"Lives: {player.hp}"
        # stats_text = f"Lives: {player.hp} Items: {len(player.items)}"
        lives_text = self.font.render(stats_text, True, "white")
        self.screen.blit(lives_text, (20, 20))
    
    # useless, but  wanted to see how it heals
    def render_npc_stats(self, npc):
        stats_text = f"HP: {npc.hp} | DMG: {npc.damage}"
        text_surface = self.smaller_font.render(stats_text, True, "white")
        text_position = npc.pos + pygame.Vector2(0, -npc.radius - 20)
        self.screen.blit(text_surface, (text_position.x, text_position.y))

    def render_conversation(self, npc):
        # Check if the dialogue is still within the display duration
        if npc.is_in_conversation and npc.text_displayed_at:
            current_time = time.time()
            elapsed_time = current_time - npc.text_displayed_at

            if elapsed_time < npc.conversation_duration:
                dialogue_text = npc.dialogue[npc.conversation_index]
                
                box_width = 200  
                box_height = 50 
                box_x = npc.pos.x - box_width / 2 
                box_y = npc.pos.y - npc.radius - box_height - 10  
            
                pygame.draw.rect(self.screen, (0, 0, 0), (box_x, box_y, box_width, box_height))
                pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)


                self.draw_text(self.screen, dialogue_text, box_x + 10, box_y + 10, 20)

    def update_conversation(self, npc):
        if not npc.conversation_finished and not npc.is_in_conversation:
            distance = npc.pos.distance_to(self.player_pos)
            if distance < 100:  # Trigger conversation if player is close enough
                npc.start_conversation()

        if npc.is_in_conversation:
            current_time = time.time()
            keys = pygame.key.get_pressed()

            if (current_time - npc.text_displayed_at > npc.conversation_duration) or (keys[pygame.K_SPACE] and current_time - npc.last_key_press_time > npc.key_debounce_delay):
                npc.advance_dialogue()
                npc.last_key_press_time = current_time
                
    def draw_text(self, screen, text, x, y, font_size):
        font = pygame.font.SysFont('Arial', font_size)
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))

    def visit_obstacle(self, obstacle):
        pygame.draw.circle(self.screen, "darkgreen", obstacle.pos, obstacle.radius)

    def visit_coin(self, coin):
        pygame.draw.circle(self.screen, "gold", coin.pos, coin.radius)

    def visit_medkit(self, medkit):
        pygame.draw.circle(self.screen, "cyan", medkit.pos, medkit.radius)

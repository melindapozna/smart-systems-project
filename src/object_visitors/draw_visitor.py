import pygame
import os
import time
from math import pi

ASSETS_DIR = os.path.join(os.path.dirname(__file__), '../../assets/images')

class DrawVisitor:
    def __init__(self, screen, player_pos):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24) 
        self.smaller_font = pygame.font.SysFont("Arial", 14)
        self.player_pos = player_pos
        
        self.heart_image = pygame.image.load(os.path.join(ASSETS_DIR, 'heart.png'))
        self.heart_image = pygame.transform.scale(self.heart_image, (20, 20))

        self.coin_image = pygame.image.load(os.path.join(ASSETS_DIR, 'coin.png'))
        self.coin_image = pygame.transform.scale(self.coin_image, (25, 25))
        
        self.medkit_image = pygame.image.load(os.path.join(ASSETS_DIR, 'medkit.png'))
        self.medkit_image = pygame.transform.scale(self.medkit_image, (20, 20))

        self.tree_texture = pygame.image.load(os.path.join(ASSETS_DIR, 'tree2.png'))
        self.tree_texture = pygame.transform.scale(self.tree_texture, (50, 50))
        
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
        self.update_conversation(hunter)
        self.render_conversation(hunter)
        self.render_npc_stats(hunter)

    def visit_bullet(self, bullet):
        pygame.draw.circle(self.screen, "yellow", bullet.pos, bullet.radius)
    
    # Render the player's remaining lives and items in the corner.
    def render_player_stats(self, player):
        heart_x, heart_y = 20, 20  
        coin_x, coin_y = 20, 60
        
        self.screen.blit(self.heart_image, (heart_x, heart_y )) 
        lives_text = self.font.render(f"Lives: {player.hp}", True, "white")  
        self.screen.blit(lives_text, (heart_x + 30, heart_y - 2))

        self.screen.blit(self.coin_image, (coin_x, coin_y))  
        coins_text = self.font.render(f"Coins:  {len(player.items)}", True, "white")  
        self.screen.blit(coins_text, (coin_x + 33, coin_y - 5))
    
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
                box_y = npc.pos.y - npc.radius - box_height - 20
            
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
        # pygame.draw.circle(self.screen, "darkgreen", obstacle.pos, obstacle.radius)
        scaled_texture = pygame.transform.scale(self.tree_texture, (obstacle.radius * 3, obstacle.radius * 3))
        rect = scaled_texture.get_rect(center=obstacle.pos)
        self.screen.blit(scaled_texture, rect)

    def visit_coin(self, coin):
        # pygame.draw.circle(self.screen, "gold", coin.pos, coin.radius)
        coin_image = pygame.image.load(os.path.join(ASSETS_DIR, 'coin.png'))
        coin_image = pygame.transform.scale(coin_image, (20, 20))
        
        coin_pos = (coin.pos.x - 10, coin.pos.y - 10)
        self.screen.blit(coin_image, coin_pos)

    def visit_medkit(self, medkit):
        # pygame.draw.circle(self.screen, "cyan", medkit.pos, medkit.radius)
        medkit_pos = (medkit.pos.x - 10, medkit.pos.y - 10)
        self.screen.blit(self.medkit_image, medkit_pos)

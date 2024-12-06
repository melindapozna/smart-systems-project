import pygame

class DrawVisitor:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)  # Font for rendering text


    def visit_player(self, player):
        pygame.draw.circle(self.screen, "green", player.pos, player.radius)
        
    def render_lives(self, player):
        # Render the player's remaining lives in the corner.
        lives_text = self.font.render(f"Lives: {player.hp}", True, "white")
        self.screen.blit(lives_text, (20, 20))

    def visit_basic_npc(self, basic_npc):
        pygame.draw.circle(self.screen, "red", basic_npc.pos, basic_npc.radius)

    def draw_text(self, screen, text, x, y, font_size):
        font = pygame.font.SysFont('Arial', font_size)
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))

    def render_conversation(self, npc, screen):
        if npc.is_in_conversation and npc.conversation_index < len(npc.dialogue):
            box_width = screen.get_width() - 150
            box_height = 100
            box_x = 50
            box_y = screen.get_height() - box_height - 30
            pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  
            pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)
            self.draw_text(screen, npc.dialogue[npc.conversation_index], box_x + 20, box_y + 30, 30)
            prompt_text = "* Press SPACE to continue *"
            prompt_y = box_y - 30
            self.draw_text(screen, prompt_text, box_x + 20, prompt_y, 18)


    def visit_bullet(self, bullet):
        pygame.draw.circle(self.screen, "yellow", bullet.pos, bullet.radius)
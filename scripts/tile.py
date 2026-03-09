import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))
        self.image.fill('#4c566a')
        self.rect = self.image.get_rect(topleft=pos)
        
        # --- Mapping & Reward Logic ---
        self.mapped = False          # Hidden by Fog of War
        self.revealed_value = 10     # Base Materials yield

    def render(self, surface, player_pos, vision_radius, render_pos):
        # 1. HARD GATE: If it hasn't been discovered, don't draw anything!
        if not self.mapped:
            return 

        # 2. If it HAS been discovered, decide how bright to draw it
        dist = pygame.math.Vector2(self.rect.center).distance_to(player_pos)
        
        if dist < vision_radius:
            # Active Vision (The "Hole" in the fog)
            self.image.set_alpha(255) 
        else:
            # The "Memory" (Where you've been, but aren't currently looking)
            self.image.set_alpha(60) 
        
        # 3. Draw to the screen
        surface.blit(self.image, render_pos)
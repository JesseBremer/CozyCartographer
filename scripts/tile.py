import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))
        self.image.fill('#4c566a')
        self.rect = self.image.get_rect(topleft=pos)
        self.mapped = False

    def render(self, surface, player_pos, vision_radius):
        if self.mapped:
            dist = pygame.math.Vector2(self.rect.center).distance_to(player_pos)
            
            # Hybrid Vision: Bright near player, dimmed elsewhere
            if dist < vision_radius:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(80) # The "Blueprint" memory trace
            
            surface.blit(self.image, self.rect)
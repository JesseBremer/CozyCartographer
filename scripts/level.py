import pygame
from scripts.tile import Tile
from scripts.player import Player

class Level:
    def __init__(self, map_data, data_manager):
        self.display_surface = pygame.display.get_surface()
        self.data = data_manager
        
        # Sprite Groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()
        
        # Permanent Fog Mask
        self.fog_mask = pygame.Surface(self.display_surface.get_size())
        self.fog_mask.fill((20, 24, 30))
        self.fog_mask.set_colorkey((255, 0, 255))

        self.setup_level(map_data)

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x, y = col_index * 64, row_index * 64
                if col == 'W':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.tile_sprites])
                if col == 'P':
                    self.player = Player((x, y), [self.visible_sprites], 
                                         self.obstacle_sprites, self.tile_sprites)

    def update(self):
        # Carve path into fog mask permanently
        pygame.draw.circle(self.fog_mask, (255, 0, 255), self.player.rect.center, self.player.vision_radius)
        self.visible_sprites.update()

    def render(self):
        # Draw mapped tiles
        for sprite in self.visible_sprites:
            if isinstance(sprite, Tile):
                sprite.render(self.display_surface, self.player.rect.center, self.player.vision_radius)
            else:
                self.display_surface.blit(sprite.image, sprite.rect)
        
        # Draw the darkness curtain
        self.display_surface.blit(self.fog_mask, (0, 0))
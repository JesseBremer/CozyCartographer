import pygame
import json # New import for reading files
from scripts.tile import Tile
from scripts.player import Player
from scripts.objects import SpecialistObject

class Level:
    def __init__(self, dungeon_name, data_manager):
        self.display_surface = pygame.display.get_surface()
        self.data = data_manager
        
        # 1. Load Dungeon Data from JSON
        # Assuming your files are in a folder named 'data'
        with open(f'data/{dungeon_name}.json', 'r') as f:
            dungeon_data = json.load(f)

        self.is_town = dungeon_data.get('is_town', False)
        self.map_layout = dungeon_data['map']
        self.fog_color = dungeon_data.get('fog_color', (20, 24, 30))
        
        # 2. Setup Groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()
        
        # 3. Setup Fog Mask using JSON color
        self.fog_mask = pygame.Surface(self.display_surface.get_size())
        self.fog_mask.fill(self.fog_color)
        self.fog_mask.set_colorkey((255, 0, 255))

        # 4. Build the World
        self.setup_level(self.map_layout)

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x, y = col_index * 64, row_index * 64
                
                if col == 'W':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.tile_sprites])
                elif col == 'P':
                    self.player = Player((x, y), [self.visible_sprites], 
                                         self.obstacle_sprites, self.tile_sprites)
                elif col == 'C':
                    SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Cipher', 50)
                elif col == 'E':
                    SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Extractor', 100)
                elif col == 'A':
                    SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Architect', 150)
                elif col == 'G':
                    # Surveyor's Guild NPC
                    SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Guild', 0)
                elif col == 'S':
                    # Drafting Shack NPC
                    SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Shack', 0)

    def check_interactions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            for sprite in self.interactable_sprites:
                dist = pygame.math.Vector2(self.player.rect.center).distance_to(sprite.rect.center)
                if dist < 80:
                    sprite.interact(self.data.current_kit)

    def update(self):
        if not self.is_town:
            pygame.draw.circle(self.fog_mask, (255, 0, 255), self.player.rect.center, self.player.vision_radius)
        
        self.visible_sprites.update()
        self.check_interactions()

    def render(self):
        player_pos = self.player.rect.center
        vision_radius = self.player.vision_radius

        for sprite in self.visible_sprites:
            if isinstance(sprite, Tile):
                if self.is_town:
                    sprite.image.set_alpha(255)
                    self.display_surface.blit(sprite.image, sprite.rect)
                else:
                    sprite.render(self.display_surface, player_pos, vision_radius)
            else:
                self.display_surface.blit(sprite.image, sprite.rect)
        
        if not self.is_town:
            self.display_surface.blit(self.fog_mask, (0, 0))
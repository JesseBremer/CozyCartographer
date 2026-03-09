import pygame
import json
import random
from scripts.tile import Tile
from scripts.player import Player
from scripts.objects import SpecialistObject, TransportTile
from scripts.generator import DungeonGenerator 

class Level:
    def __init__(self, dungeon_name, data_manager):
        self.display_surface = pygame.display.get_surface()
        self.data = data_manager
        self.dungeon_name = dungeon_name
        
        # 1. Branching Logic
        if dungeon_name == 'town':
            self.is_town = True
            with open(f'data/town.json', 'r') as f:
                d_data = json.load(f)
            self.map_layout = d_data['map']
            self.fog_color = d_data.get('fog_color', (20, 24, 30))
        else:
            self.is_town = False
            # Randomly generate a 30x30 ruin
            gen = DungeonGenerator(width=30, height=30, max_tiles=150)
            self.map_layout = gen.generate()
            self.fog_color = (20, 24, 30)

        # 2. Setup Groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()
        self.transport_sprites = pygame.sprite.Group() 
        
        # 3. Setup Fog Mask
        self.fog_mask = pygame.Surface(self.display_surface.get_size())
        self.fog_mask.fill(self.fog_color)
        self.fog_mask.set_colorkey((255, 0, 255))
        # Set alpha to 160 so discovered areas aren't pitch black
        self.fog_mask.set_alpha(160) 

        # 4. Build the World
        self.setup_level(self.map_layout)

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x, y = col_index * 64, row_index * 64
                if col == 'W':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.tile_sprites])
                elif col == 'P':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.tile_sprites, self.data, self)
                elif col == 'H': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Shack', 0)
                elif col == 'F': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Foundry', 0)
                elif col == 'G': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Guild', 0)
                elif col == 'V': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Archive', 0)
                elif col == 'L': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Greenhouse', 0)
                elif col == 'C': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Cipher', 50)
                elif col == 'E': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Extractor', 100)
                elif col == 'A': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Architect', 150)
                elif col == 'X':
                    dest = "SELECT_DUNGEON" if self.is_town else "town"
                    TransportTile((x,y), [self.visible_sprites, self.transport_sprites], dest)

    def update(self):
        if not hasattr(self, 'player'):
            return None

        if not self.is_town:
            # RESET and redraw vision circle on the mask
            self.fog_mask.fill(self.fog_color)
            screen_center = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2)
            pygame.draw.circle(self.fog_mask, (255, 0, 255), screen_center, self.player.vision_radius)
        
        self.visible_sprites.update()
        self.check_interactions()

        # Logic for discovering tiles (requires Ink)
        if self.data.ink_current > 0:
            for tile in self.tile_sprites:
                dist = pygame.math.Vector2(self.player.rect.center).distance_to(tile.rect.center)
                if dist < self.player.vision_radius and not tile.mapped:
                    tile.mapped = True
                    self.data.gold += (tile.revealed_value * self.data.essentials['pen'])

        return self.check_transport()

    def render(self, display_surface, camera_offset):
        player_pos = self.player.rect.center
        vision_radius = self.player.vision_radius

        for sprite in self.visible_sprites:
            offset_pos = sprite.rect.topleft - camera_offset
            
            # 1. Handle Tiles
            if isinstance(sprite, Tile):
                if self.is_town:
                    # In town, everything is fully visible and bright
                    sprite.image.set_alpha(255)
                    display_surface.blit(sprite.image, offset_pos)
                else:
                    # In dungeons, the Tile's internal render handles 
                    # the "mapped" check and the "memory" alpha
                    sprite.render(display_surface, player_pos, vision_radius, offset_pos)
            
            # 2. Handle Everything Else (Player, NPCs, Specialist Objects)
            else:
                if not self.is_town:
                    dist = pygame.math.Vector2(sprite.rect.center).distance_to(player_pos)
                    if dist < vision_radius:
                        display_surface.blit(sprite.image, offset_pos)
                else:
                    # Always draw objects in town
                    display_surface.blit(sprite.image, offset_pos)
        
        # 3. Apply the Fog Overlay (the "dimmer")
        if not self.is_town:
            display_surface.blit(self.fog_mask, (0, 0))

    def check_interactions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            for sprite in self.interactable_sprites:
                dist = pygame.math.Vector2(self.player.rect.center).distance_to(sprite.rect.center)
                if dist < 80:
                    sprite.interact(self.data.current_kit)

    def check_transport(self):
        for sprite in self.transport_sprites:
            if sprite.rect.colliderect(self.player.rect):
                return sprite.destination
        return None
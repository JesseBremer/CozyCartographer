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
        
        # 1. Branching Logic: Static Town vs. Procedural Dungeon
        if dungeon_name == 'town':
            self.is_town = True
            with open(f'data/town.json', 'r') as f:
                d_data = json.load(f)
            self.map_layout = d_data['map']
            self.fog_color = d_data.get('fog_color', (20, 24, 30))
        else:
            self.is_town = False
            
            # --- DYNAMIC SCALING LOGIC ---
            # Calculate Tier based on ink_max (100=T1, 200=T2, etc.)
            ink_tier = self.data.essentials.get('ink_max', 100) // 100
            
            # Base size is 20x20. Every Tier adds 5 tiles to dimensions.
            map_w = 20 + (ink_tier * 5)
            map_h = 20 + (ink_tier * 5)
            
            # Max tiles scales to keep the "Random Walk" dense
            total_tiles = 100 + (ink_tier * 40)
            
            gen = DungeonGenerator(width=map_w, height=map_h, max_tiles=total_tiles)
            self.map_layout = gen.generate()
            self.fog_color = (20, 24, 30)

        # 2. Setup Sprite Groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()
        self.transport_sprites = pygame.sprite.Group() 
        
        # 3. Setup Fog Mask (Matches screen size dynamically)
        self.fog_mask = pygame.Surface(self.display_surface.get_size())
        self.fog_mask.fill(self.fog_color)
        self.fog_mask.set_colorkey((255, 0, 255))
        # Set alpha so discovered but distant areas look like "Blueprint Memories"
        self.fog_mask.set_alpha(160) 

        # 4. Build the World
        self.setup_level(self.map_layout)

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x, y = col_index * 64, row_index * 64
                
                # --- WALLS ---
                if col == 'W':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.tile_sprites])
                
                # --- EXITS & DUNGEON ENTRANCE ---
                elif col == 'X':
                    dest = "SELECT_DUNGEON" if self.is_town else "town"
                    TransportTile((x,y), [self.visible_sprites, self.transport_sprites], dest)
                    
                    if not self.is_town:
                        # Create player exactly on the X tile
                        self.player = Player(
                            (x, y), [self.visible_sprites], 
                            self.obstacle_sprites, self.tile_sprites,
                            self.data, self
                        )
                        
                        # IMPORTANT: Move them 1 full tile North so they are 
                        # standing in the "Entry Hallway" we forced in the generator.
                        self.player.rect.y -= 64

                # --- TOWN PLAYER SPAWN (For town.json) ---
                elif col == 'P':
                    self.player = Player(
                        (x, y), [self.visible_sprites], 
                        self.obstacle_sprites, self.tile_sprites,
                        self.data, self
                    )
                
                # --- VILLAGE BUILDINGS ---
                elif col == 'H': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Shack', 0)
                elif col == 'F': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Foundry', 0)
                elif col == 'G': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Guild', 0)
                elif col == 'V': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Archive', 0)
                elif col == 'L': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Greenhouse', 0)
                
                # --- DUNGEON SPECIALISTS (Loot) ---
                elif col == 'C': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Cipher', 50)
                elif col == 'E': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Extractor', 100)
                elif col == 'A': SpecialistObject((x,y), [self.visible_sprites, self.interactable_sprites], 'Architect', 150)
    
    def check_interactions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            for sprite in self.interactable_sprites:
                dist = pygame.math.Vector2(self.player.rect.center).distance_to(sprite.rect.center)
                if dist < 80:
                    # Passing full data object for Foundry/Shack logic
                    sprite.interact(self.data)

    def check_transport(self):
        for sprite in self.transport_sprites:
            if sprite.rect.colliderect(self.player.rect):
                return sprite.destination
        return None

    def update(self):
        if not hasattr(self, 'player'): return None

        # 1. Update Fog Mask for Procedural Ruins
        if not self.is_town:
            self.fog_mask.fill(self.fog_color)
            # Center the vision "hole" on the screen
            screen_center = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2)
            pygame.draw.circle(self.fog_mask, (255, 0, 255), screen_center, self.player.vision_radius)
        
        self.visible_sprites.update()
        self.check_interactions()

        # 2. Mapping Logic (Discovery consumes Ink and yields Gold)
        if self.data.ink_current > 0:
            for tile in self.tile_sprites:
                dist = pygame.math.Vector2(self.player.rect.center).distance_to(tile.rect.center)
                if dist < self.player.vision_radius and not tile.mapped:
                    tile.mapped = True
                    # Reward based on Pen Multiplier
                    self.data.gold += (tile.revealed_value * self.data.essentials['pen'])

        return self.check_transport()

    def render(self, display_surface, camera_offset):
        player_pos = self.player.rect.center
        vision_radius = self.player.vision_radius

        for sprite in self.visible_sprites:
            offset_pos = sprite.rect.topleft - camera_offset
            
            # --- 1. Tile Rendering (with discovery/memory logic) ---
            if isinstance(sprite, Tile):
                if self.is_town:
                    sprite.image.set_alpha(255)
                    display_surface.blit(sprite.image, offset_pos)
                else:
                    sprite.render(display_surface, player_pos, vision_radius, offset_pos)
            
            # --- 2. Entity/Object Rendering ---
            else:
                if not self.is_town:
                    # Hide loot/objects in the deep fog until approached
                    dist = pygame.math.Vector2(sprite.rect.center).distance_to(player_pos)
                    if dist < vision_radius:
                        display_surface.blit(sprite.image, offset_pos)
                else:
                    # Always show objects in town
                    display_surface.blit(sprite.image, offset_pos)
        
        # --- 3. Final Fog Overlay ---
        if not self.is_town:
            display_surface.blit(self.fog_mask, (0, 0))
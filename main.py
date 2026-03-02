import pygame
import sys
from scripts.player import Player
from scripts.tile import Tile

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Cozy Cart')
        self.clock = pygame.time.Clock()
        self.running = True

        # 1. Setup Groups FIRST
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # 2. Define Map
        self.world_map = [
            'WWWWWWWWWWWWWWWWWWWW',
            'W                  W',
            'W        WWWW      W',
            'W                  W',
            'W    P             W',
            'W          WW      W',
            'W          WW      W',
            'W                  W',
            'WWWWWWWWWWWWWWWWWWWW',
        ]

        # 3. Create Map (This creates the player too!)
        self.tile_sprites = pygame.sprite.Group()
        self.create_map()

        #Darkness Effects
        self.fog_surf = pygame.Surface((1280, 720))
        self.fog_surf.set_colorkey((255, 0, 255))

    def create_map(self):
            for row_index, row in enumerate(self.world_map):
                for col_index, col in enumerate(row):
                    x, y = col_index * 64, row_index * 64
                    if col == 'W':
                        # Add to tile_sprites so player can find them
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.tile_sprites])
                    if col == 'P':
                        self.player = Player((x, y), [self.visible_sprites], 
                                            self.obstacle_sprites, self.tile_sprites)

    def draw_fog(self):
        self.fog_surf.fill((20, 24, 30)) # Darkness color
        
        # Create a "Light Hole" at player position
        pygame.draw.circle(self.fog_surf, (255, 0, 255), self.player.rect.center, self.player.vision_radius)
        self.screen.blit(self.fog_surf, (0, 0), special_flags=pygame.BLEND_MULT)

    def run(self):
        while self.running:
            # 1. Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # 2. Update Logic
            # This calls the update() method of the player and all tiles
            self.visible_sprites.update()

            # 3. Rendering Logic
            self.screen.fill('#2e3440') # Background color (Nord theme night)

            # Manual Draw Loop: Only draw tiles if they have been discovered
            for sprite in self.visible_sprites:
                # If it's a tile, check if it has been mapped by the player
                if hasattr(sprite, 'mapped'):
                    if sprite.mapped:
                        self.screen.blit(sprite.image, sprite.rect)
                else:
                    # If it's the player or an active tool, always draw it
                    self.screen.blit(sprite.image, sprite.rect)

            # 4. Fog of War / Vignette
            # This applies the dark overlay with the light circle around the player
            self.draw_fog()
            
            # 5. Refresh
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
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
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(self.world_map):
            for col_index, col in enumerate(row):
                x = col_index * 64
                y = row_index * 64
                if col == 'W':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'P':
                    # We pass the groups and the obstacle group for collisions
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update everything in one group
            self.visible_sprites.update()

            # Draw everything once
            self.screen.fill('#2e3440')
            self.visible_sprites.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
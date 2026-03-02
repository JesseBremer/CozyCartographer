import pygame
import sys

from scripts.player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Cozy Cart')
        self.clock = pygame.clock.Clock()
        self.running = True

        # Create a sprite group for the player
        self.player_group = pygame.sprite.Group()
        self.player = Player((640, 360), self.player_group)

    def run(self):
        while self.running:
            # 1. Input/Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # 2. Update logic (Empty for now)
            self.player_group.update()
            # 3. Draw/Render
            self.screen.fill('#2e3440') # A cozy dark blue/grey
            self.player_group.draw(self.screen)
            pygame.display.update()
            
            # Maintain 60 Frames Per Second
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
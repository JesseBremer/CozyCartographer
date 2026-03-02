import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Cozy Cart')
        self.clock = pygame.clock.Clock()
        self.running = True

    def run(self):
        while self.running:
            # 1. Input/Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # 2. Update logic (Empty for now)

            # 3. Draw/Render
            self.screen.fill('#2e3440') # A cozy dark blue/grey
            pygame.display.update()
            
            # Maintain 60 Frames Per Second
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
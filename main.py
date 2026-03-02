import pygame, sys
from scripts.data_manager import DataManager
from scripts.level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        
        self.data = DataManager()
        self.world_map = [
            'WWWWWWWWWWWWWWWWWWWW',
            'W                  W',
            'W    P             W',
            'WWWWWWWWWWWWWWWWWWWW',
        ]
        
        self.level = Level(self.world_map, self.data)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.level.update()
            self.screen.fill('#1a1c23')
            self.level.render()
            
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    Game().run()
import pygame, sys
from scripts.data_manager import DataManager
from scripts.level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Cozy Cartographer')
        self.clock = pygame.time.Clock()
        
        # 1. Persistent Data (Ink, Gold, Kits)
        self.data = DataManager()
        
        # 2. State Management
        # We start in the town. 
        # This string must match your filename: data/town.json
        self.current_location = 'town' 
        self.load_level(self.current_location)

    def load_level(self, location_name):
        """Swaps the current level for a new one based on a JSON file."""
        # We re-instantiate self.level. 
        # The Level class now handles its own Sprite Groups internally.
        self.level = Level(location_name, self.data)

    def check_transport(self):
        """
        Placeholder for logic to switch between town and dungeon.
        Example: Press 'T' to go to town, 'D' to go to dungeon.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_t] and self.current_location != 'town':
            self.current_location = 'town'
            self.load_level('town')
        elif keys[pygame.K_d] and self.current_location != 'clockwork_conservatory':
            self.current_location = 'clockwork_conservatory'
            self.load_level('clockwork_conservatory')

    def run(self):
        while True:
            # 1. Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # 2. Update Logic
            self.check_transport() # Check if we need to switch maps
            self.level.update()    # Handles player, fog, and interactions

            # 3. Rendering Logic
            self.screen.fill('#1a1c23')
            self.level.render()    # Handles tiles, players, and fog mask
            
            # 4. Refresh
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    Game().run()
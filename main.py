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

                # 2. Update Logic (Only call update ONCE)
                # The level returns a string (like 'town' or 'SELECT_DUNGEON') if the player hits an exit
                new_destination = self.level.update()
                
                if new_destination:
                    if new_destination == "SELECT_DUNGEON":
                        self.open_dungeon_menu()
                    else:
                        self.current_location = new_destination
                        self.load_level(self.current_location)

                # 3. Rendering Logic
                self.screen.fill('#1a1c23')
                self.level.render()
                
                pygame.display.update()
                self.clock.tick(60)

    def open_dungeon_menu(self):
        selecting = True
        while selecting:
            self.screen.fill('#2e3440')
            # For now, we'll use a simple print, but you can draw text here later
            # This is the "Drafting Shack" phase of your Design Doc
            print("--- CHOOSE DESTINATION ---")
            print("1. Clockwork Conservatory")
            print("2. Sunken Scriptorium (Locked)")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.current_location = 'clockwork_conservatory'
                        self.load_level(self.current_location)
                        selecting = False
                    if event.key == pygame.K_ESCAPE: # Back out
                        # Move player away from exit so they don't re-trigger it
                        self.level.player.pos.y += 10 
                        selecting = False
            
            pygame.display.update()
            self.clock.tick(60)   

if __name__ == '__main__':
    Game().run()
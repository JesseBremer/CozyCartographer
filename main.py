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
                    elif new_destination == "town":
                        # Instead of loading immediately, ask first
                        if self.confirm_exit_menu():
                            self.current_location = "town"
                            self.load_level(self.current_location)
                        else:
                            # Move player away from the exit so it doesn't loop
                            self.level.player.rect.y += 64

                # 3. Rendering Logic
                self.screen.fill('#1a1c23')
                self.level.render()
                
                pygame.display.update()
                self.clock.tick(60)

    def open_dungeon_menu(self):
            """A dedicated state to select an expedition destination."""
            selecting = True
            
            # We use a black overlay to dim the town while picking
            overlay = pygame.Surface((1280, 720))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))

            while selecting:
                # 1. Draw the current town in the background, then the overlay
                self.level.render()
                self.screen.blit(overlay, (0, 0))

                # 2. Draw Menu Text
                font = pygame.font.SysFont('Arial', 40, bold=True)
                title = font.render("--- SELECT EXPEDITION ---", True, 'white')
                opt1 = font.render("[ 1 ] Clockwork Conservatory", True, '#ebcb8b')
                opt2 = font.render("[ 2 ] Sunken Scriptorium (Locked)", True, '#4c566a')
                exit_hint = font.render("Press ESC to return to Town", True, '#bf616a')

                self.screen.blit(title, (400, 200))
                self.screen.blit(opt1, (400, 300))
                self.screen.blit(opt2, (400, 380))
                self.screen.blit(exit_hint, (400, 550))

                # 3. Wait for Input (This stops the console spam)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.current_location = 'clockwork_conservatory'
                            self.load_level(self.current_location)
                            selecting = False # Exit the menu and return to run()
                        
                        if event.key == pygame.K_ESCAPE:
                            # Move player away from the exit so they don't re-trigger it immediately
                            self.level.player.rect.y += 64 
                            selecting = False

                pygame.display.update()
                self.clock.tick(60)

    def confirm_exit_menu(self):
        """Pauses the game to confirm if the player wants to leave the dungeon."""
        waiting = True
        
        # Dim the background
        overlay = pygame.Surface((1280, 720))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        while waiting:
            # 1. Render the dungeon in the background
            self.level.render()
            self.screen.blit(overlay, (0, 0))

            # 2. Draw Menu Text (Vertical List Style)
            font = pygame.font.SysFont('Arial', 40, bold=True)
            
            title = font.render("--- RETURN TO TOWN? ---", True, 'white')
            opt_yes = font.render("[ 1 ] Yes, Secure Map Data", True, '#ebcb8b')
            opt_no = font.render("[ 2 ] No, Keep Exploring", True, '#ebcb8b')
            exit_hint = font.render("Press ESC to cancel", True, '#bf616a')

            # Using the same coordinates as your Selection Menu for consistency
            self.screen.blit(title, (400, 200))
            self.screen.blit(opt_yes, (400, 300))
            self.screen.blit(opt_no, (400, 380))
            self.screen.blit(exit_hint, (400, 550))

            # 3. Input Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return True  # Proceed to town
                    if event.key == pygame.K_2 or event.key == pygame.K_ESCAPE:
                        return False # Stay in dungeon

            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    Game().run()
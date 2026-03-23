import pygame, sys
from scripts.data_manager import DataManager
from scripts.level import Level
from scripts.ui import UI

class Game:
    def __init__(self):
        pygame.init()
        self.show_inventory = False
        
        # Get the actual user monitor resolution for a perfect fit
        info = pygame.display.Info()
        self.window_width = info.current_w
        self.window_height = info.current_h
        
        # Set to Fullscreen
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN)
        
        pygame.display.set_caption('Cozy Cartographer')
        self.clock = pygame.time.Clock()
        self.ui = UI()
        
        self.data = DataManager()
        self.camera_offset = pygame.math.Vector2() 
        
        self.current_location = 'town' 
        self.load_level(self.current_location)

    def load_level(self, location_name):
        """Swaps the current level and resets camera."""
        self.level = Level(location_name, self.data)

    def run(self):
        while True:
            # --- 1. CONSOLIDATED EVENT HANDLING ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    if event.key in [pygame.K_TAB, pygame.K_i]:
                        self.show_inventory = not self.show_inventory

            # --- 2. UPDATE LOGIC (Pause if inventory is open) ---
            if not self.show_inventory:
                new_destination = self.level.update()

                if hasattr(self.level, 'player'):
                    self.camera_offset.x = self.level.player.rect.centerx - (self.screen.get_width() / 2)
                    self.camera_offset.y = self.level.player.rect.centery - (self.screen.get_height() / 2)

                # --- NEW SIGNAL HANDLING ---
                if new_destination:
                    # A. Handle Universal Shops (Foundry, Guild, Archive, etc.)
                    if isinstance(new_destination, str) and new_destination.startswith("OPEN_SHOP_"):
                        shop_type = new_destination.replace("OPEN_SHOP_", "")
                        self.open_shop_menu(shop_type) # The generic menu function
                        self.level.player.rect.y += 64 
                        
                    # B. Handle Dungeon Selection
                    elif new_destination == "SELECT_DUNGEON":
                        self.open_dungeon_menu()
                        self.level.player.rect.y += 64 
                        
                    # C. Handle Town Return
                    elif new_destination == "town":
                        if self.confirm_exit_menu():
                            self.current_location = "town"
                            self.load_level(self.current_location)
                        else:
                            self.level.player.rect.y += 100
                            
                    # D. Handle Simple Interactions (Like the Shack)
                    elif new_destination == True: 
                        self.level.player.rect.y += 64

            # --- 3. RENDERING LOGIC ---
            self.screen.fill('#1a1c23')
            self.level.render(self.screen, self.camera_offset)
            self.ui.render(self.data)

            if self.show_inventory:
                self.ui.draw_inventory_menu(self.screen, self.data)
            
            pygame.display.update()
            self.clock.tick(60)


    def open_dungeon_menu(self):
        selecting = True
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        
        sw, sh = self.screen.get_width(), self.screen.get_height()
        center_x = sw // 2

        while selecting:
            self.level.render(self.screen, self.camera_offset)
            self.screen.blit(overlay, (0, 0))

            font = pygame.font.SysFont('Arial', 50, bold=True)
            hint_font = pygame.font.SysFont('Arial', 30)
            
            def draw_center(text, y, color='white', custom_font=font):
                surf = custom_font.render(text, True, color)
                self.screen.blit(surf, (center_x - surf.get_width() // 2, y))

            draw_center("--- THE EXPEDITION GATE ---", sh * 0.2, '#eceff4')
            draw_center("The ruins shift and change beyond this point.", sh * 0.35, '#d8dee9', hint_font)
            draw_center("[ 1 ] I am ready to explore", sh * 0.5, '#ebcb8b')
            draw_center("[ 2 ] I still need to prepare", sh * 0.6, '#bf616a')
            draw_center("Tip: Ensure your Ink is full at the Foundry first!", sh * 0.8, '#81a1c1', hint_font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.current_location = 'clockwork_conservatory'
                        self.load_level(self.current_location)
                        selecting = False
                    if event.key == pygame.K_2 or event.key == pygame.K_ESCAPE:
                        self.level.player.rect.y += 100
                        selecting = False

            pygame.display.update()
            self.clock.tick(60)

    def confirm_exit_menu(self):
        """Dynamic Fullscreen confirmation menu to avoid crashes."""
        waiting = True
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))

        sw, sh = self.screen.get_width(), self.screen.get_height()
        center_x = sw // 2

        while waiting:
            # FIX: Pass camera_offset to avoid TypeError crash
            self.level.render(self.screen, self.camera_offset)
            self.screen.blit(overlay, (0, 0))

            font = pygame.font.SysFont('Arial', 50, bold=True)
            
            def draw_center(text, y, color='white'):
                surf = font.render(text, True, color)
                self.screen.blit(surf, (center_x - surf.get_width() // 2, y))

            draw_center("--- RETURN TO TOWN? ---", sh * 0.3, '#eceff4')
            draw_center("[ 1 ] Yes, Secure Map Data", sh * 0.45, '#ebcb8b')
            draw_center("[ 2 ] No, Keep Exploring", sh * 0.55, '#a3be8c')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return True 
                    if event.key == pygame.K_2 or event.key == pygame.K_ESCAPE:
                        return False

            pygame.display.update()
            self.clock.tick(60)

    def open_shop_menu(self, shop_type):
        shopping = True
        
        # Define Shop Inventories
        # Format: "Display Name": (Cost, ItemName, Uses/Value)
        shops = {
            'FOUNDRY': {
                'title': 'THE INK FOUNDRY',
                'items': {"Refill Ink": (25, "REFILL", 100), "Ink Vial": (40, "Ink Vial", 1)}
            },
            'GUILD': {
                'title': 'EXPLORERS GUILD',
                'items': {"Cipher Kit": (50, "Cipher", 3), "Extractor": (75, "Extractor", 5), "Architect Set": (100, "Architect", 2)}
            },
            'ARCHIVE': {
                'title': 'THE ARCHIVE',
                'items': {"Old Map": (30, "Map Fragment", 1), "Research Notes": (60, "Focus Buff", 1)}
            },
            'GREENHOUSE': {
                'title': 'THE GREENHOUSE',
                'items': {"Small Satchel": (150, "UPGRADE_SATCHEL", 1), "Herbal Tea": (20, "Speed Buff", 1)}
            }
        }

        current_shop = shops.get(shop_type, shops['FOUNDRY'])

        while shopping:
            self.level.render(self.screen, self.camera_offset)
            # Use a dark overlay
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((20, 30, 40, 220))
            self.screen.blit(overlay, (0,0))

            # UI Rendering
            font = pygame.font.SysFont('Arial', 40, bold=True)
            item_font = pygame.font.SysFont('Arial', 30)
            cx, cy = self.screen.get_width() // 2, self.screen.get_height() // 2

            # Draw Title
            title_surf = font.render(current_shop['title'], True, '#81a1c1')
            self.screen.blit(title_surf, (cx - title_surf.get_width()//2, cy - 200))

            # Draw Items
            for i, (name, details) in enumerate(current_shop['items'].items()):
                cost, item_id, val = details
                text = f"[ {i+1} ] {name} - {cost}g"
                color = '#ebcb8b' if self.data.gold >= cost else '#bf616a'
                item_surf = item_font.render(text, True, color)
                self.screen.blit(item_surf, (cx - item_surf.get_width()//2, cy - 50 + (i * 60)))

            # Handle Input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: shopping = False
                    
                    # Check keys 1, 2, 3...
                    for i, (name, details) in enumerate(current_shop['items'].items()):
                        if event.key == getattr(pygame, f"K_{i+1}"):
                            cost, item_id, val = details
                            if self.data.gold >= cost:
                                # SPECIAL CASES (Refills/Upgrades)
                                if item_id == "REFILL":
                                    self.data.gold -= cost
                                    self.data.ink_current = self.data.essentials['ink_max']
                                elif item_id == "UPGRADE_SATCHEL":
                                    self.data.gold -= cost
                                    self.data.essentials['satchel'] += 1
                                # STANDARD ITEMS
                                elif self.data.add_to_inventory(item_id, val):
                                    self.data.gold -= cost
                                    print(f"Bought {item_id}")
            
            pygame.display.update()
            self.clock.tick(60)
    

if __name__ == '__main__':
    Game().run()
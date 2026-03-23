import pygame

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont('Arial', 26, bold=True)

        # UI Bar settings
        self.bar_width = 200
        self.bar_height = 20
        self.padding = 20

    def draw_ink_bar(self, current, max_ink):
        # Draw Background
        bg_rect = pygame.Rect(self.padding, self.padding, self.bar_width, self.bar_height)
        pygame.draw.rect(self.display_surface, '#4c566a', bg_rect)

        # Calculate Fill
        ratio = current / max_ink
        current_width = self.bar_width * ratio
        fill_rect = pygame.Rect(self.padding, self.padding, current_width, self.bar_height)

        # Draw Fill (Blue for Ink)
        color = '#81a1c1' if ratio > 0.2 else '#bf616a' # Turns red when low
        pygame.draw.rect(self.display_surface, color, fill_rect)

    def draw_text(self, value, x, y, icon=""):
            # Check if the value is a number (int or float) before converting
            if isinstance(value, (int, float)):
                display_string = f"{icon} {int(value)}"
            else:
                # If it's a string (like 'Pathfinder'), just display it
                display_string = f"{icon} {value}"

            text_surf = self.font.render(display_string, True, 'white')
            self.display_surface.blit(text_surf, (x, y))

    def draw_inventory_menu(self, screen, data):
        # 1. Create a semi-transparent overlay
        overlay = pygame.Surface((300, 400))
        overlay.set_alpha(200)
        overlay.fill((46, 52, 64)) # A nice Nordic dark blue
        screen.blit(overlay, (50, 50))
        
        font = pygame.font.SysFont('Arial', 22, bold=True)
        small_font = pygame.font.SysFont('Arial', 18)

        # 2. Draw Header
        title = font.render("SATCHEL CONTENTS", True, '#eceff4')
        screen.blit(title, (70, 70))
        
        # 3. Draw Slots Info
        slots_text = small_font.render(f"Slots: {len(data.inventory)}/{data.essentials['satchel']}", True, '#81a1c1')
        screen.blit(slots_text, (70, 100))

        # 4. List Items & Durability
        for i, item in enumerate(data.inventory):
            y_pos = 140 + (i * 40)
            
            # Item Name
            name_text = small_font.render(item['name'], True, '#ebcb8b')
            screen.blit(name_text, (80, y_pos))
            
            # Durability "Pips" (e.g., [ |||  ])
            uses = item['uses']
            pips = "|" * uses
            durability_text = small_font.render(f"[{pips}]", True, '#a3be8c')
            screen.blit(durability_text, (200, y_pos))

        # 5. Draw Gold/Ink at the bottom
        gold_text = small_font.render(f"Gold: {data.gold}g", True, '#ebcb8b')
        screen.blit(gold_text, (70, 400))
    

    def render(self, data):
        # Draw the essential stats from DataManager
        self.draw_ink_bar(data.ink_current, data.essentials['ink_max'])
        self.draw_text(data.gold, self.padding, self.padding + 30, "Materials:")
        self.draw_text(data.current_kit, self.padding, self.padding + 60, "Kit:")
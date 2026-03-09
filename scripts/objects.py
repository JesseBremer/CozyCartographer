import pygame

class SpecialistObject(pygame.sprite.Sprite):
    def __init__(self, pos, groups, lock_type, reward_val):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))
        # Visual distinction: Dungeon rewards are gold, Village buildings are blue-ish
        color = '#ebcb8b' if lock_type in ['Cipher', 'Extractor', 'Architect'] else '#81a1c1'
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        
        self.lock_type = lock_type 
        self.reward_value = reward_val # Fixed: was reward in __init__ but reward_value in interact
        self.interacted = False

    def interact(self, data):
        """Now takes the full data object to modify ink, gold, etc."""
        
        # --- 1. VILLAGE BUILDINGS ---
        if self.lock_type == 'Foundry':
            refill_cost = 25
            if data.gold >= refill_cost:
                if data.ink_current < data.essentials['ink_max']:
                    data.gold -= refill_cost
                    data.ink_current = data.essentials['ink_max']
                    print(f"Ink Refilled! Gold remaining: {data.gold}")
                    return True
                else:
                    print("Ink is already full!")
            else:
                print("Not enough gold for ink.")
            return False

        elif self.lock_type == 'Shack':
            # Drafting Shack logic: "Sell" your mapped progress
            # For now, let's just say it gives a bonus and resets the level
            print("Mapping data secured. Village growth increased.")
            return True

        # --- 2. DUNGEON SPECIALISTS ---
        elif data.current_kit == self.lock_type:
            # Match: 'Cipher' kit unlocks 'Cipher' object
            print(f"Unlocked! Gained {self.reward_value} gold.")
            data.gold += self.reward_value
            self.interacted = True
            self.kill() 
            return True
            
        else:
            # Failed interaction
            print(f"Access Denied. Need {self.lock_type} kit.")
            return False

class TransportTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, destination):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))
        self.image.fill('#bf616a') 
        self.rect = self.image.get_rect(topleft=pos)
        self.destination = destination
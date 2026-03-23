import pygame

class SpecialistObject(pygame.sprite.Sprite):
    def __init__(self, pos, groups, lock_type, reward_val):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))
        # Village buildings (Foundry, Shack, etc.) get a blue-ish color
        # Dungeon rewards (Cipher, Extractor, Architect) get a gold color
        village_types = ['Shack', 'Foundry', 'Guild', 'Archive', 'Greenhouse']
        color = '#81a1c1' if lock_type in village_types else '#ebcb8b'
        
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        
        self.lock_type = lock_type 
        self.reward_value = reward_val 
        self.interacted = False

    def interact(self, data):
        """Modified to handle the Foundry refill and Consumable tools."""
        
        # --- 1. VILLAGE BUILDINGS ---
        if self.lock_type == 'Foundry':
            return "OPEN_FOUNDRY_SHOP"

        elif self.lock_type == 'Shack':
            print("Mapping data secured. Village growth increased.")
            return True
        
        elif self.lock_type == 'Guild':
            # Simple Shop Logic: Buy a 'Cipher' kit for 50g
            ITEM_NAME = 'Cipher'
            COST = 50
            USES = 3

            if data.gold >= COST:
                if data.add_to_inventory(ITEM_NAME, USES):
                    data.gold -= COST
                    print(f"Purchased {ITEM_NAME}! {len(data.inventory)}/{data.essentials['satchel']} Slots used.")
                    return True
                else:
                    print("Satchel is full! Upgrade at the Greenhouse.")
            else:
                print(f"Need {COST}g to buy a {ITEM_NAME}.")
            return False

        # --- 2. DUNGEON SPECIALISTS (Consumable Logic) ---
        # Look for a matching tool in the inventory list
        # data.inventory looks like: [{'name': 'Extractor', 'uses': 5}, ...]
        tool = next((item for item in data.inventory if item['name'] == self.lock_type), None)
        
        if tool and tool['uses'] > 0:
            # Found a working tool!
            tool['uses'] -= 1
            print(f"Used {tool['name']}! {tool['uses']} charges remaining.")
            
            # Add the reward
            data.gold += self.reward_value
            print(f"Gained {self.reward_value} gold.")
            
            # If tool is broken, remove it from inventory
            if tool['uses'] <= 0:
                data.inventory.remove(tool)
                print(f"Your {self.lock_type} tool has shattered!")
            
            self.interacted = True
            self.kill() # Remove the reward object from the map
            return True
            
        else:
            # Failed interaction
            print(f"Access Denied. You need a working {self.lock_type} tool.")
            return False

class TransportTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, destination):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))
        self.image.fill('#bf616a') 
        self.rect = self.image.get_rect(topleft=pos)
        self.destination = destination
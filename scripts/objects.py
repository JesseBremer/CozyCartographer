import pygame

class SpecialistObject(pygame.sprite.Sprite):
    def __init__(self, pos, groups, lock_type, reward_val):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))
        self.image.fill('#bf616a') # exits
        self.image.fill('#ebcb8b') # interactables
        self.rect = self.image.get_rect(topleft=pos)
        
        self.lock_type = lock_type # 'Cipher', 'Extractor', or 'Architect'
        self.reward = reward_val
        self.interacted = False

    def interact(self, current_kit):
            # 1. Define which objects are PERMANENT (Village Buildings)
            village_buildings = ['Shack', 'Foundry', 'Guild', 'Archive', 'Greenhouse']
            
            # 2. Check if it's a village building OR if the player has the right kit
            if self.lock_type in village_buildings:
                print(f"Opening {self.lock_type} Menu...")
                # We return True but DO NOT call self.kill()
                return True 
                
            elif current_kit == self.lock_type:
                # This is a Dungeon Reward (Cipher, Extractor, Architect)
                print(f"Unlocked! Gained {self.reward_value} materials.")
                self.interacted = True
                self.kill() # Only dungeon rewards disappear
                return True
                
            else:
                # Failed interaction
                print(f"Access Denied. Current Kit: {current_kit}. Required: {self.lock_type}.")
                return False

class TransportTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, destination):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))
        self.image.fill('#bf616a') # Red/Pink for Exits
        self.rect = self.image.get_rect(topleft=pos)
        self.destination = destination
import pygame

class SpecialistObject(pygame.sprite.Sprite):
    def __init__(self, pos, groups, lock_type, reward_val):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))
        self.image.fill('#ebcb8b') # Gold/Yellow for interactables
        self.rect = self.image.get_rect(topleft=pos)
        
        self.lock_type = lock_type # 'Cipher', 'Extractor', or 'Architect'
        self.reward = reward_val
        self.interacted = False

    def interact(self, current_kit):
        if current_kit == self.lock_type:
            print(f"Unlocked! Gained {self.reward} materials.")
            self.interacted = True
            self.kill() # Remove from world once claimed
            return True
        else:
            print(f"I need the {self.lock_type} kit for this.")
            return False
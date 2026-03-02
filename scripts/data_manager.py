class DataManager:
    def __init__(self):
        # Vertical Essentials (Upgradable)
        self.essentials = {
            'pen': 1,      # Gold/XP mult
            'ink_max': 100, 
            'paper': 0.25, # Data retention
            'satchel': 1   # Tool slots
        }
        self.gold = 0
        self.current_kit = 'Pathfinder' # Horizontal Key
        self.ink_current = 100
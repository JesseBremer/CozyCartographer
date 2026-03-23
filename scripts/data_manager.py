# scripts/data_manager.py

class DataManager:
    def __init__(self):
        # Vertical Essentials (Upgradable)
        self.essentials = {
            'pen': 1,      # Gold/XP mult
            'ink_max': 100, 
            'paper': 0.25, # Data retention
            'satchel': 3   # Max slots in inventory
        }
        
        self.gold = 150
        self.ink_current = 100
        self.current_kit = 'Pathfinder' # You can keep or remove this
        
        # A list of dictionaries to store consumable tools
        self.inventory = [
            {'name': 'Cipher', 'uses': 3},    # Starter tool for testing
            {'name': 'Extractor', 'uses': 5}
        ]

    def add_to_inventory(self, item_name, uses):
        """Checks if there is room in the satchel before adding."""
        if len(self.inventory) < self.essentials['satchel']:
            self.inventory.append({'name': item_name, 'uses': uses})
            return True
        return False
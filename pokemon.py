import pygame
import os

# Creation of the Pokemon class
class Pokemon:
    def __init__(self, pokemon_id, all_data):
        """Initializes a Pokémon from JSON data"""
        file = all_data[str(pokemon_id)]
        self.id = pokemon_id
        self.xp = 0
        self.load_attributes(file)

    def get_type(self):
        """Getter for the Pokémon type"""
        return self.__type
    
    def get_attack(self):
        """Getter for attack"""
        return self.__attack
    
    def set_attack(self, value):
        """Setter for attack (cannot be negative)"""
        self.__attack = max(0, value)

    def load_attributes(self, file):
        """Loads all attributes from JSON data"""
        self.name = file["name"]
        self.__type = file["type"]
        self.level = file["level"]
        self.hp = file["hp"]
        self.hp_max = file["hp"]
        self.__attack = file["attack"]
        self.defense = file["defense"]
        self.evolution_id = file["evolution_id"]
        self.evolution_level = file["evolution_level"]
        
        # Load sprite only if it exists
        sprite_path = file["sprite"]
        if os.path.exists(sprite_path):
            try:
                self.sprite = pygame.image.load(sprite_path)
            except Exception as e:
                print(f"Warning: Could not load sprite {sprite_path}: {e}")
                self.sprite = None
        else:
         self.__attack=value

    def load_attributes(self,file): #Method to avoid repetition and have all pokemon data imported
        self.name=file["name"]
        self.__type=file["type"]
        self.level=file["level"]
        self.hp=file["hp"]
        self.hp_max=file["hp"]
        self.__attack=file["attack"]
        self.defense=file["defense"]
        self.evolution_id=file["evolution_id"]
        self.evolution_level=file["evolution_level"]
        self.sprite=pygame.image.load(file["sprite"])

    def __str__(self): #Method to debug in case of issues
        display=f"--Pokémon Data--\n"
        display+=f"Name: {self.name}(lv.{self.level}\n)"
        display+=f"Type: {"/".join(self.get_type())}\n"
        display+=f"Health: {self.hp}/{self.hp_max}\n"
        display+=f"Stats: ATK:{self.get_attack()}/DEF: {self.defense}\n"
        if self.evolution_id:
            display += f"Evolves at level {self.evolution_level}\n"
        else:
            display += f"Final evolution stage\n"
        
        return display

    def is_alive(self):
        """Checks whether the Pokémon is alive"""
        return self.hp > 0
    
    def evolve(self, new_data):
        """Evolves the Pokémon if it reaches the required level"""
        if self.evolution_id and self.level >= self.evolution_level:
            self.id = self.evolution_id
            new_file = new_data[str(self.evolution_id)]
            self.load_attributes(new_file)
            return True
        return False
    
    def raise_xp_level(self, new_data):
        """Increases XP and level after a won battle"""
        self.xp += 10
        
        if self.xp >= 100:
            self.level += 1
            self.xp = 0
            self.hp += 5
            self.hp_max += 5
            self.set_attack(self.get_attack() + 3)
            self.defense += 3
            
            # Attempt to evolve
            evolved = self.evolve(new_data)
            if evolved:
                print(f"{self.name} evolved!")
    
    def take_damage(self, damage):
        """Inflicts damage to the Pokémon (taking defense into account)"""
        total_damage = max(0, damage - self.defense)
        # HP cannot drop below 0
        self.hp = max(0, self.hp - total_damage)
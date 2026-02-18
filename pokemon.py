import pygame

#Creation of pokemon class
class Pokemon:
    def __init__(self,pokemon_id,all_data): #Take pokemon id and data from pokemon.json
        file=all_data[str(pokemon_id)]#Load all data from pokemon.json
        self.id=pokemon_id
        self.xp=0
        self.load_attributes(file)

    def get_type(self): #getters for type and attack
        return self.__type
    def get_attack(self):
        return self.__attack
    def set_attack(self, value):
        if value<0:
         self.__attack=0
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
            display+=f"Evolve at level: {self.evolution_level} in {self.evolution_id}\n"
        else:
            display+=f"This Pokemon is at his final stage of evolution\n"
        return display

    def is_alive(self): #Method that check if pokemon is alive or not
        return self.hp>0
    
    def evolve(self,new_data): #Method that evolve the pokemon by taking the evolution_id from pokemon.json
        if self.level>=self.evolution_level and self.evolution_id!=None:
            self.id=self.evolution_id
            new_file=new_data[str(self.evolution_id)] #Change past pokemon data with new data from the evolved pokemon
            self.load_attributes(new_file)
            return True
        return False
    
    
    def raise_xp_level(self,new_data): #Raise xp and level after each fight won 
        self.xp+=10
        if self.xp>=100:
           self.level+=1
           self.xp=0
           self.hp+=5
           self.hp_max+=5
           self.set_attack(self.get_attack()+3)
           self.defense+=3
           self.evolve(new_data) #Call evolve method 
    
    def take_damage(self,damage): #Method that lower hp using the total damage 
        total_damage=max(0,damage-self.defense)
        self.hp-=total_damage
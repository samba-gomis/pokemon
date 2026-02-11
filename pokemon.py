import pygame


class Pokemon:
    def __init__(self,pokemon_id,all_data):
        file=all_data[str(pokemon_id)]
        self.id=pokemon_id
        self.xp=0
        self.load_attributes(file)

    def load_attributes(self,file):
        self.name=file["name"]
        self.type=file["type"]
        self.level=file["level"]
        self.hp=file["hp"]
        self.hp_max=file["hp"]
        self.attack=file["attack"]
        self.defense=file["defense"]
        self.evolution_id=file["evolution_id"]
        self.evolution_level=file["evolution_level"]
        self.sprite=pygame.image.load(file["sprite"])

    def __str__(self):
        display=f"--Pokémon Data--\n"
        display+=f"Name: {self.name}(lv.{self.level}\n)"
        display+=f"Type: {"/".join(self.type)}\n"
        display+=f"Health: {self.hp}/{self.hp_max}\n"
        display+=f"Stats: ATK:{self.attack}/DEF: {self.defense}\n"
        if self.evolution_id:
            display+=f"Evolve at level: {self.evolution_level} in {self.evolution_id}\n"
        else:
            display+=f"This Pokemon is at his final stage of evolution\n"

    def is_alive(self):
        if self.hp>0:
            return True
        return False
    
    def evolve(self,new_data):
        if self.level>=self.evolution_level and self.evolution_id!=None:
            self.id=self.evolution_id
            new_file=new_data[str(self.evolution_id)]
            self.load_attributes(new_file)
            return True
        return False
    

    def raise_xp_level(self,new_data):
        self.xp+=10
        if self.xp>=100:
           self.level+=1
           self.xp=0
           self.hp+=5
           self.hp_max+=5
           self.attack+=3
           self.defense+=3
           self.evolve(new_data)
    
    def take_damage(self,damage):
        total_damage=max(0,damage-self.defense)
        self.hp-=total_damage

    
    
    
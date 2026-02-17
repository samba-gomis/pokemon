import random
from pokemon import * #import pokemon class and attributes
from type import damage_mutliplying #import the function to calculate the multiplier
from pokedex import * #import save method 

class Fight:
    def __init__(self,pokemon, all_data):
        self.pokemon=pokemon #player pokemon
        random_id=random.choice(list(all_data.keys())) #get random_id for random opponent
        self.opponent=pokemon(random_id,all_data) #create opponant 
    
    def check_victory(self): 
        if not self.opponent.is_alive():
           print(f"{self.pokemon.name} won! {self.opponent.name} lost!")
           return True
           
        elif not self.pokemon.is_alive():
         print(f"{self.opponent.name} managed to win! You lost!")
         return False       
        return None
    
    def catch_pokemon(self): #manage chances of catching a pokemon after a victory using 50/50
       catching_chances=random.randint(1,100)
       if catching_chances<=50:
          print("Oh no! This pokemon escaped!")
          return False
       else:
          print("Good Job! You caught this pokemon!")
          return True


    def attack_power(self,attacker,target): #use random with the possibly of missing an attack if attack<1
         attack=random.randint(1,10)
         if attack>1:
            multiplicator = damage_mutliplying(attacker.get_type()[0], target.get_type()) #calculate the multiplicator using the type of the attacker and the type of the target
            total_damage = attacker.get_attack() * multiplicator
            target.take_damage(total_damage)
         else:
            print("Oups! Attack missed")

    def fight(self, all_data):
       
      while self.pokemon.is_alive() and self.opponent.is_alive(): #check if both are alive
           self.attack_power(self.pokemon,self.opponent)
        
           if self.opponent.is_alive():
               self.attack_power(self.opponent,self.pokemon)
            
      if self.check_victory(): #if victory, raise xp, use catch chances and save the opponent
            self.pokemon.raise_xp_level(all_data)
            is_captured = self.catch_pokemon()
            self.save_to_pokedex(self.opponent,is_captured)
    
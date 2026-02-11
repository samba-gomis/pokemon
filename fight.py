import random
from pokemon import * #import pokemon class and attributes
from type import * #import type dic and multiplier method
from pokedex import * #import save method 

class Fight:
    def __init__(self,pokemon, all_data):
        self.pokemon=pokemon #player pokemon
        random_id=random.choice(list(all_data.keys())) #charge random_id for random opponent
        self.opponent=Pokemon(random_id,all_data) #create opponant 
    
    def check_victory(self): 
        if not self.opponent.is_alive():
           print(f"{self.pokemon.name} won! {self.opponent.name} lost!")
           return True
        else:
         print(f"{self.opponent.name} managed to win! You lost!")
         return False
    
    def catch_pokemon(self): #manage chances of catching a pokemon after a victory using 50/50
       catching_chances=random.randint(1,100)
       if self.check_victory:
          if catching_chances<=50:
             print("Oh no! This pokemon escaped!")
             return False
          elif catching_chances>=50:
             print("Good Job! You caught this pokemon!")
             return True


    def attack_power(self,attacker,target): #use random with the possibly of missing an attack if attack<1
       attack=random.randint(1,10)
       if attack>1:  
        multiplicator=get_type_multiplier(attacker.get_type,target.get_type) #call of type.py method and take type of both pokemon
        total_damage=attacker.attack*multiplicator #take pokemon attack from pokemon.py 
        target.take_damage(total_damage) #take pokemon.py method take_damage
       else:
        print("Oups! Attack missed")

    def fight(self, all_data):
       
       while self.pokemon.is_alive() and self.opponent.is_alive(): #check if both is alive
           self.attack_power(self.pokemon,self.opponent)
        
           if self.opponent.is_alive():
               self.attack_power(self.opponent,self.pokemon)
            
       if self.check_victory(): #if victory, raise xp, use catch chances and save the opponent
          self.pokemon.raise_xp_level(all_data)
          is_captured = self.catch_pokemon()
          self.save_to_pokedex(self.opponent,is_captured)
       else: #if lost leave the boucle
          return
          

               
           
           
import random
from src.pokemon import *
from src.type import damage_multiplying
from src.pokedex import Pokedex 

class Fight:
    def __init__(self,player_pokemon, opponent_pokemon, all_data):
        self.pokemon=player_pokemon #player pokemon
        self.opponent=opponent_pokemon #create opponant 
        self.pokedex=Pokedex()

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
          return False
       else:
          return True

    def attack_power(self,attacker,target): #use random with the possibly of missing an attack if attack<1
         attack=random.randint(1,10)
         if attack>1:
            multiplicator = damage_multiplying(attacker.get_type()[0], target.get_type()) #calculate the multiplicator using the type of the attacker and the type of the target
            total_damage = attacker.get_attack() * multiplicator
            target.take_damage(total_damage)
             
            if multiplicator >= 2:
             eff_msg = "It's super effective!"
            elif multiplicator > 1:
             eff_msg = "It's effective!"
            elif multiplicator == 1:
             eff_msg = ""
            elif multiplicator > 0:
             eff_msg = "It's not very effective..."
            else:
             eff_msg = "It has no effect!"
        
            msg = f"{attacker.name} attacks {target.name}!"
            if eff_msg:
              msg += f" {eff_msg}"
            return msg
         else:
          return f"{attacker.name} missed!"
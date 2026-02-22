import json
import random
import os
from src.pokemon import Pokemon
from src.pokedex import Pokedex
from src.fight import Fight

class Game:
    def __init__(self):
        # GAME DATA
        self.all_data = self.load_pokemon_data()
        self.pokemons = self.create_pokemons()
        self.filtered_pokemons=[]
        self.fight = None
        
        # RENAMED to match graphical_interface.py
        self.player_pokemon = None
        self.opponent_pokemon = None
        self.combat_log = []

        # POKEDEX - Single shared instance
        self.pokedex_manager = Pokedex()

        # Flag to track if the game is running
        self.running = True 

        
    # LOADING DATA
    def load_pokemon_data(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_path, "pokemon.json")
        with open(json_path, "r") as f:
            return json.load(f)

    def create_pokemons(self):
        return [Pokemon(pid, self.all_data) for pid in self.all_data]

    # POKEMON SELECTION, FILTER BY POKEMON NO EVOLVED
    def get_pokemon_list(self):     
     evolution_ids = set()
     for pid, data in self.all_data.items():
        evo_id = data.get("evolution_id")
        if evo_id:
            evolution_ids.add(str(evo_id))
     self.filtered_pokemons = [p for p in self.pokemons if str(p.base_id) not in evolution_ids]
     return self.filtered_pokemons

    def choose_player_pokemon(self, index):
        self.player_pokemon = self.filtered_pokemons[index]

    #CHOOSE OPPONENT REGARDING PLAYER POKEMON LEVEL
    def choose_random_opponent_pokemon(self):
        player_level = self.player_pokemon.level
        player_atk = self.player_pokemon.get_attack()
    
        close_pokemons = [
         p for p in self.filtered_pokemons
         if abs(p.level - player_level) <= 3
         and abs(p.get_attack() - player_atk) <= 20
         and p != self.player_pokemon
        ]
    
        if close_pokemons:
         self.opponent_pokemon = random.choice(close_pokemons)
        else:
         fallback = [p for p in self.filtered_pokemons
                    if abs(p.level - player_level) <= 5 and p != self.player_pokemon]
         self.opponent_pokemon = random.choice(fallback) if fallback else random.choice(self.filtered_pokemons)
    # POKEMON BATTLE
    def start_battle(self):
        self.combat_log = []
        if not self.player_pokemon or not self.opponent_pokemon:
         return False
        self.player_pokemon.hp = self.player_pokemon.hp_max
        self.opponent_pokemon.hp = self.opponent_pokemon.hp_max
        self.fight = Fight(self.player_pokemon, self.opponent_pokemon, self.all_data)
        return True
    
    #MANAGE TURNS AND DISPLAY MESSAGES
    def battle_turn(self):
        if not self.fight:
         return False, []
        message=[]
        msg=self.fight.attack_power(self.player_pokemon, self.opponent_pokemon)
        if msg:
            message.append(msg)

        if self.opponent_pokemon.is_alive():
         msg=self.fight.attack_power(self.opponent_pokemon, self.player_pokemon)
         if msg:
             message.append(msg)
        return self.fight.check_victory(),message

    # SPECIAL ACTIONS
    def use_potion(self):
        """Uses a potion to heal the player's Pokemon"""
        if self.player_pokemon and self.player_pokemon.hp > 0:
            heal = 20
            old_hp = self.player_pokemon.hp
            self.player_pokemon.hp = min(
                self.player_pokemon.hp + heal, 
                self.player_pokemon.hp_max
            )
            actual_heal = self.player_pokemon.hp - old_hp
            self.combat_log.append(
                f" {self.player_pokemon.name} uses a potion (+{actual_heal} HP)"
            )

    def try_to_escape(self):
        """Attempts to flee the battle (50% chance)"""
        if not self.player_pokemon or not self.opponent_pokemon:
            self.combat_log.append(" Cannot escape, Pokemon not selected!")
            return False

        chance = random.random()
        if chance > 0.5:
            self.combat_log.append(" The player managed to escape!")
            return True
        else:
            self.combat_log.append(" Escape failed!")
            # The opponent attacks during the escape attempt
            self.fight.attack_power(self.opponent_pokemon, self.player_pokemon)
            return False

    # ADD A CUSTOM POKEMON
    def add_custom_pokemon(self, name, types, hp, level, attack, defense):
        """Adds a custom Pokemon to the list"""
        # Generate a new ID
        existing_ids = [int(k) for k in self.all_data.keys()]
        new_id = str(max(existing_ids) + 1) if existing_ids else "1"
        
        new_pokemon_data = {
            "name": name,
            "type": types,
            "level": level,
            "hp": hp,
            "attack": attack,
            "defense": defense,
            "evolution_id": None,
            "evolution_level": None,
            "sprite": "assets/images/default.png"
        }
        
        # Add to data
        self.all_data[new_id] = new_pokemon_data
        
        # Create the Pokemon instance
        try:
            new_pokemon = Pokemon(new_id, self.all_data)
            self.pokemons.append(new_pokemon)
            return new_pokemon
        except Exception as e:
            print(f"Error creating custom Pokemon: {e}")
            return None

    # POKEDEX MANAGEMENT
    def add_to_pokedex(self, pokemon, captured=False):
        """Adds a Pokemon to the Pokedex"""
        self.pokedex_manager.save_to_pokedex(pokemon, captured)

    def get_pokedex(self):
        """Returns the Pokedex manager"""
        return self.pokedex_manager

    # CLEAN EXIT
    def quit_game(self):
        """Clean up and exit"""
        self.pokedex_manager.clear_pokedex()
        self.running = False
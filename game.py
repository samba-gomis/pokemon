import json
import random
import os
from pokemon import Pokemon
from pokedex import Pokedex
from type import damage_multiplying, TYPE_DAMAGE

class Game:
    def __init__(self):
        # GAME DATA
        self.all_data = self.load_pokemon_data()
        self.pokemons = self.create_pokemons()
        
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

    # POKEMON SELECTION
    def get_pokemon_list(self):
        return self.pokemons

    def choose_player_pokemon(self, index):
        self.player_pokemon = self.pokemons[index]

    def choose_random_opponent_pokemon(self):
        self.opponent_pokemon = random.choice(self.pokemons)

    # POKEMON BATTLE
    def start_battle(self):
        self.combat_log = []

        if not self.player_pokemon or not self.opponent_pokemon:
            self.combat_log.append("Error: Player or opponent Pokémon not selected!")
            return self.combat_log

        while self.player_pokemon.is_alive() and self.opponent_pokemon.is_alive():
            self.battle_turn()

        if self.player_pokemon.is_alive():
            self.combat_log.append(f" {self.player_pokemon.name} wins!")
            self.player_pokemon.raise_xp_level(self.all_data)
            self.add_to_pokedex(self.opponent_pokemon, captured=True)
        else:
            self.combat_log.append(f" {self.player_pokemon.name} loses...")
            self.add_to_pokedex(self.opponent_pokemon, captured=False)

        return self.combat_log

    def battle_turn(self):
        """One battle turn: the player attacks, then the opponent"""
        self.attack(self.player_pokemon, self.opponent_pokemon)
        if self.opponent_pokemon.is_alive():
            self.attack(self.opponent_pokemon, self.player_pokemon)

    def attack(self, attacker, defender):
        """Performs an attack from one Pokémon to another"""
        attack_type = attacker.get_type()[0]
        
        # Uses damage_multiplying (keeping the original typo from the file)
        multiplier = damage_multiplying(attack_type, defender.get_type())

        # Renamed to avoid shadowing the function name
        damage_dealt = int(attacker.get_attack() * multiplier)
        defender.take_damage(damage_dealt)

        # Combat message
        message = f" {attacker.name} attacks {defender.name} and deals {damage_dealt} damage"
        
        if multiplier > 1:
            message += " (Super effective!)"
        elif multiplier < 1:
            message += " (Not very effective...)"
        else:
            message += "!"

        self.combat_log.append(message)

    # SPECIAL ACTIONS
    def use_potion(self):
        """Uses a potion to heal the player's Pokémon"""
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
            self.combat_log.append(" Cannot escape, Pokémon not selected!")
            return False

        chance = random.random()
        if chance > 0.5:
            self.combat_log.append(" The player managed to escape!")
            return True
        else:
            self.combat_log.append(" Escape failed!")
            # The opponent attacks during the escape attempt
            self.attack(self.opponent_pokemon, self.player_pokemon)
            return False

    # ADD A CUSTOM POKEMON
    def add_custom_pokemon(self, name, types, hp, level, attack, defense):
        """Adds a custom Pokémon to the list"""
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
            "sprite": "assets/images/default.png"  # Default sprite
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
        """Adds a Pokémon to the Pokédex"""
        self.pokedex_manager.save_to_pokedex(pokemon, captured)

    def get_pokedex(self):
        """Returns the Pokédex manager"""
        return self.pokedex_manager

    # CLEAN EXIT
    def quit_game(self):
        """Clean up and exit"""
        self.running = False
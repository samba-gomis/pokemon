import json
import random
from pokemon import Pokemon
from pokedex import Pokedex
#from type import damage_mutliplying

class Game:
    def __init__(self):
        #  GAME DATA 
        self.all_data = self.load_pokemon_data()
        self.pokemons = self.create_pokemons()
        self.pokemon_joueur = None
        self.pokemon_adversaire = None
        self.combat_log = []

        #  POKEDEX 
        self.pokedex = []

        # New flag to track if the game is running
        self.running = True 
        
    def quit_game(self):
        """Signals the main loop to stop the game properly."""
        self.running = False    

    #  LOADING DATA 
    def load_pokemon_data(self):
        import os
        base_path = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_path, "pokemon.json")
        with open(json_path, "r") as f:
            return json.load(f)

    def create_pokemons(self):
        return [Pokemon(pid, self.all_data) for pid in self.all_data]

    #  POKEMON SELECTION 
    def get_pokemon_list(self):
        return self.pokemons

    def choose_player_pokemon(self, index):
        self.pokemon_joueur = self.pokemons[index]

    def choose_random_opponent_pokemon(self):
        self.pokemon_adversaire = random.choice(self.pokemons)

    # POKEMON BATTLE ---
    def start_battle(self):
        self.combat_log = []

        if not self.pokemon_joueur or not self.pokemon_adversaire:
            self.combat_log.append("Error: Player or opponent Pokémon not selected!")
            return self.combat_log

        while self.pokemon_joueur.is_alive() and self.pokemon_adversaire.is_alive():
            self.battle_turn()

        if self.pokemon_joueur.is_alive():
            self.combat_log.append(f"{self.pokemon_joueur.name} wins!")
            self.pokemon_joueur.raise_xp_level(self.all_data)
            self.add_to_pokedex(self.pokemon_adversaire, captured=True)
        else:
            self.combat_log.append(f"{self.pokemon_joueur.name} loses...")

        return self.combat_log

    def battle_turn(self):
        self.attack(self.pokemon_joueur, self.pokemon_adversaire)
        if self.pokemon_adversaire.is_alive():
            self.attack(self.pokemon_adversaire, self.pokemon_joueur)

    def attack(self, attacker, defender):
        attack_type = attacker.get_type()[0]
        multiplier = damage(attack_type, defender.get_type())

        damage = int(attacker.get_attack() * multiplier)
        defender.take_damage(damage)

        message = f"{attacker.name} attacks {defender.name} and deals {damage} damage "
        if multiplier > 1:
            message += "(Super effective)"
        elif multiplier < 1:
            message += "(Not very effective)"

        self.combat_log.append(message)

    # --- SPECIAL ACTIONS ---
    def use_potion(self):
        if self.pokemon_joueur and self.pokemon_joueur.hp > 0:
            heal = 20
            self.pokemon_joueur.hp = min(self.pokemon_joueur.hp + heal, self.pokemon_joueur.hp_max)
            self.combat_log.append(f"{self.pokemon_joueur.name} uses a potion (+{heal} HP)")

    def try_to_escape(self):
        if not self.pokemon_joueur or not self.pokemon_adversaire:
            self.combat_log.append("Cannot escape, Pokémon not selected!")
            return False

        chance = random.random()
        if chance > 0.5:
            self.combat_log.append("The player managed to escape!")
            return True
        else:
            self.combat_log.append("Escape failed!")
            self.attack(self.pokemon_adversaire, self.pokemon_joueur)
            return False

    # --- POKEDEX MANAGEMENT ---
    def add_to_pokedex(self, pokemon, captured=False):
        """
        Add a Pokemon to the player's Pokedex if captured or after winning a battle.
        """
        if pokemon not in self.pokedex:
            self.pokedex.append(pokemon)
        Pokedex(pokemon, captured)

    def get_pokedex(self):
        """
        Return self to allow chaining .display_pokedex() in the GUI.
        """
        return self

    def display_pokedex(self):
        """
        Return a list of strings describing each Pokemon in the Pokedex.
        """
        if not self.pokedex:
            return ["Your Pokédex is empty."]
        return [f"{p.name} - Lv.{p.level} - HP:{p.hp}/{p.hp_max}" for p in self.pokedex]

    # --- CLEAN EXIT ---
    def quit_game(self):
        """
        Optional helper method for GUI: clean up and exit.
        """
        import pygame, sys
        pygame.quit()
        sys.exit()

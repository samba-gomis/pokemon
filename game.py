import json
import random
from pokemon import Pokemon
from pokedex import save_to_pokedex
from type import damage_mutliplying

class Game:
    def __init__(self):
        self.all_data = self.load_pokemon_data()
        self.pokemons = self.create_pokemons()
        self.pokemon_joueur = None
        self.pokemon_adversaire = None
        self.combat_log = []
        self.pokedex = []

    #  LOADING DATA
    def load_pokemon_data(self):
        with open("pokemon.json", "r") as f:
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

    #  POKEMON BATTLE
    def start_battle(self):
        self.combat_log = []

        while self.pokemon_joueur.is_alive() and self.pokemon_adversaire.is_alive():
            self.battle_turn()

        if self.pokemon_joueur.is_alive():
            self.combat_log.append(" Player wins!")
            self.pokemon_joueur.raise_xp_level(self.all_data)
            save_to_pokedex(self.pokemon_adversaire, True)
        else:
            self.combat_log.append(" Player loses...")

        return self.combat_log

    def battle_turn(self):
        # Player attacks first
        self.attack(self.pokemon_joueur, self.pokemon_adversaire)

        if self.pokemon_adversaire.is_alive():
            self.attack(self.pokemon_adversaire, self.pokemon_joueur)

    def attack(self, attacker, defender):
        attack_type = attacker.get_type()[0]
        multiplier = damage_mutliplying(attack_type, defender.get_type())

        damage = int(attacker.get_attack() * multiplier)
        defender.take_damage(damage)

        message = (
            f"{attacker.name} attacks {defender.name} "
            f"and deals {damage} damage "
        )

        if multiplier > 1:
            message += "(Super effective)"
        elif multiplier < 1:
            message += "(Not very effective)"

        self.combat_log.append(message)

    # SPECIAL ACTIONS (OPTIONAL BUT FUN)
    def use_potion(self):
        if self.pokemon_joueur.hp > 0:
            heal = 20
            self.pokemon_joueur.hp = min(
                self.pokemon_joueur.hp + heal,
                self.pokemon_joueur.hp_max
            )
            self.combat_log.append(
                f"{self.pokemon_joueur.name} uses a potion (+{heal} HP)"
            )

    def try_to_escape(self):
        chance = random.random()
        if chance > 0.5:
            self.combat_log.append(" The player managed to escape!")
            return True
        else:
            self.combat_log.append(" Escape failed!")
            self.attack(self.pokemon_adversaire, self.pokemon_joueur)
            return False
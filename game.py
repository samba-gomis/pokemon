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

    # ===============================
    #  CHARGEMENT DES DONNÉES
    # ===============================
    def load_pokemon_data(self):
        with open("pokemon.json", "r") as f:
            return json.load(f)

    def create_pokemons(self):
        return [Pokemon(pid, self.all_data) for pid in self.all_data]

    # ===============================
    #  SÉLECTION DES POKÉMONS
    # ===============================
    def obtenir_liste_pokemons(self):
        return self.pokemons

    def choisir_pokemon_joueur(self, index):
        self.pokemon_joueur = self.pokemons[index]

    def choisir_pokemon_adversaire_aleatoire(self):
        self.pokemon_adversaire = random.choice(self.pokemons)

    # ===============================
    #  COMBAT POKÉMON
    # ===============================
    def demarrer_combat(self):
        self.combat_log = []

        while self.pokemon_joueur.is_alive() and self.pokemon_adversaire.is_alive():
            self.tour_de_combat()

        if self.pokemon_joueur.is_alive():
            self.combat_log.append(" Victoire du joueur !")
            self.pokemon_joueur.raise_xp_level(self.all_data)
            save_to_pokedex(self.pokemon_adversaire, True)
        else:
            self.combat_log.append(" Défaite du joueur...")

        return self.combat_log

    def tour_de_combat(self):
        # Le joueur attaque en premier
        self.attaquer(self.pokemon_joueur, self.pokemon_adversaire)

        if self.pokemon_adversaire.is_alive():
            self.attaquer(self.pokemon_adversaire, self.pokemon_joueur)

    def attaquer(self, attaquant, defenseur):
        type_attaque = attaquant.get_type()[0]
        multiplicateur = damage_mutliplying(type_attaque, defenseur.get_type())

        degats = int(attaquant.get_attack() * multiplicateur)
        defenseur.take_damage(degats)

        message = (
            f"{attaquant.name} attaque {defenseur.name} "
            f"et inflige {degats} dégâts "
        )

        if multiplicateur > 1:
            message += "(Super efficace )"
        elif multiplicateur < 1:
            message += "(Peu efficace )"

        self.combat_log.append(message)

    # ===============================
    # ACTIONS SPÉCIALES (OPTIONNEL MAIS FUN)
    # ===============================
    def utiliser_potion(self):
        if self.pokemon_joueur.hp > 0:
            soin = 20
            self.pokemon_joueur.hp = min(
                self.pokemon_joueur.hp + soin,
                self.pokemon_joueur.hp_max
            )
            self.combat_log.append(
                f"{self.pokemon_joueur.name} utilise une potion (+{soin} HP)"
            )

    def tenter_fuite(self):
        chance = random.random()
        if chance > 0.5:
            self.combat_log.append(" Le joueur a réussi à fuir !")
            return True
        else:
            self.combat_log.append(" La fuite a échoué !")
            self.attaquer(self.pokemon_adversaire, self.pokemon_joueur)
            return False
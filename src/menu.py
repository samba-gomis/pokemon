import pygame
from src.constants import *

class Menu:
    def __init__(self, screen, draw_text, draw_button):
        self.screen = screen
        self.draw_text = draw_text
        self.draw_button = draw_button

    def main_menu(self, set_state):
        self.screen.fill(BG_COLOR)
        self.draw_text("POKEMON GAME", FONT_TITLE, TEXT_COLOR, WIDTH//2, 50, center=True)
        self.draw_text("Catch them all!", FONT_NORMAL, (149, 165, 166), WIDTH//2, 100, center=True)
        self.draw_button("Start Game", WIDTH//2 - 125, 200, 250, 50, BUTTON_GREEN, lambda: set_state("pokemon_selection"))
        self.draw_button("Add Pokemon", WIDTH//2 - 125, 270, 250, 50, BUTTON_BLUE, lambda: set_state("add_pokemon"))
        self.draw_button("View Pokedex", WIDTH//2 - 125, 340, 250, 50, BUTTON_ORANGE, lambda: set_state("pokedex"))
        self.draw_button("Quit", WIDTH//2 - 125, 410, 250, 50, BUTTON_RED, lambda: pygame.quit())
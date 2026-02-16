import pygame
import pygame_textinput
from game import Game
from type import TYPE_DAMAGE
from constants import *

# Initialize Pygame
pygame.init()

class GraphicalInterface:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("🎮 Pokemon Game 🎮")
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.state = "main_menu"
        self.selected_pokemon_index = -1
        self.battle_history = []
        self.pokedex_content = []
        self.scroll_offset = 0
        self.text_input = pygame_textinput.TextInputVisualizer(font_object=FONT_NORMAL)
        self.current_input_field = None
        self.form_data = {
            "name": "",
           "type1": list(TYPE_DAMAGE.keys())[0],
            "type2": "None",
            "hp": "",
            "level": "",
            "attack": "",
            "defense": ""
        }
        self.run()

    def draw_text(self, text, font, color, x, y, center=False):
        render = font.render(text, True, color)
        if center:
            rect = render.get_rect(center=(x, y))
            self.screen.blit(render, rect)
        else:
            self.screen.blit(render, (x, y))

    def draw_button(self, text, x, y, width, height, color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect)
        self.draw_text(text, FONT_BUTTON, TEXT_COLOR, x + width//2, y + height//2, center=True)
        if rect.collidepoint(mouse) and click[0] == 1:
            if action:
                action()

    def draw_listbox(self, items, x, y, width, height, selected_index):
        pygame.draw.rect(self.screen, FRAME_COLOR, (x, y, width, height))
        item_height = 30
        visible_items = height // item_height
        start = max(0, selected_index - visible_items // 2)
        for i in range(start, min(len(items), start + visible_items)):
            color = BUTTON_BLUE if i == selected_index else FRAME_COLOR
            pygame.draw.rect(self.screen, color, (x, y + (i - start) * item_height, width, item_height))
            self.draw_text(items[i], FONT_NORMAL, TEXT_COLOR, x + 10, y + (i - start) * item_height + 5)

    def draw_scrolled_text(self, lines, x, y, width, height):
        pygame.draw.rect(self.screen, FRAME_COLOR, (x, y, width, height))
        line_height = 20
        visible_lines = height // line_height
        start = self.scroll_offset
        for i in range(start, min(len(lines), start + visible_lines)):
            self.draw_text(lines[i], FONT_COURIER, TEXT_COLOR, x + 10, y + (i - start) * line_height)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if self.current_input_field:
                self.text_input.update(events)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.form_data[self.current_input_field] = self.text_input.value
                    self.current_input_field = None
                    self.text_input = pygame_textinput.TextInputVisualizer(font_object=FONT_NORMAL)

    def main_menu(self):
        self.screen.fill(BG_COLOR)
        self.draw_text("🎮 POKEMON GAME 🎮", FONT_TITLE, TEXT_COLOR, WIDTH//2, 50, center=True)
        self.draw_text("Catch them all!", FONT_NORMAL, (149, 165, 166), WIDTH//2, 100, center=True)
        self.draw_button("⚔️ Start Game", WIDTH//2 - 125, 200, 250, 50, BUTTON_GREEN, lambda: self.set_state("pokemon_selection"))
        self.draw_button("➕ Add Pokemon", WIDTH//2 - 125, 270, 250, 50, BUTTON_BLUE, lambda: self.set_state("add_pokemon"))
        self.draw_button("📖 View Pokedex", WIDTH//2 - 125, 340, 250, 50, BUTTON_ORANGE, lambda: self.set_state("pokedex"))
        self.draw_button("🚪 Quit", WIDTH//2 - 125, 410, 250, 50, BUTTON_RED, lambda: pygame.quit())

    def pokemon_selection(self):
        self.screen.fill(BG_COLOR)
        self.draw_text("Choose Your Pokemon", FONT_TITLE, TEXT_COLOR, WIDTH//2, 50, center=True)
        pokemons = self.game.obtenir_liste_pokemons()
        items = []
        for i, pokemon in enumerate(pokemons):
            types_str = "/".join(pokemon.type)
            text = f"{i+1}. {pokemon.nom} ({types_str}) - Lv.{pokemon.niveau} - ATK:{pokemon.attaque} DEF:{pokemon.defense}"
            items.append(text)
        self.draw_listbox(items, 50, 100, 800, 400, self.selected_pokemon_index)
        self.draw_button("✅ Confirm", WIDTH//2 - 100, 550, 150, 50, BUTTON_GREEN, self.confirm_pokemon_selection)
        self.draw_button("🔙 Back", WIDTH//2 + 60, 550, 150, 50, BUTTON_GRAY, lambda: self.set_state("main_menu"))

    def confirm_pokemon_selection(self):
        if self.selected_pokemon_index >= 0:
            self.game.choisir_pokemon_joueur(self.selected_pokemon_index)
            self.game.choisir_pokemon_adversaire_aleatoire()
            self.set_state("battle")

    def battle(self):
        self.screen.fill(BG_COLOR)
        self.draw_text("⚔️ POKEMON BATTLE ⚔️", FONT_TITLE, TEXT_COLOR, WIDTH//2, 50, center=True)
        # Player Pokemon
        pygame.draw.rect(self.screen, BUTTON_GREEN, (100, 100, 300, 150))
        self.draw_text("YOUR POKEMON", FONT_BUTTON, TEXT_COLOR, 250, 110)
        self.draw_text(str(self.game.pokemon_joueur), FONT_SMALL, TEXT_COLOR, 110, 140)
        # VS
        self.draw_text("VS", FONT_TITLE, BUTTON_RED, WIDTH//2, 175, center=True)
        # Opponent Pokemon
        pygame.draw.rect(self.screen, BUTTON_RED, (500, 100, 300, 150))
        self.draw_text("OPPONENT", FONT_BUTTON, TEXT_COLOR, 650, 110)
        self.draw_text(str(self.game.pokemon_adversaire), FONT_SMALL, TEXT_COLOR, 510, 140)
        # Battle Text
        self.draw_scrolled_text(self.battle_history, 50, 300, 800, 250)
        self.draw_button("⚡ FIGHT!", WIDTH//2 - 100, 580, 200, 50, (243, 156, 18), self.start_battle)

    def start_battle(self):
        battle = self.game.demarrer_combat()
        if battle:
            self.battle_history = battle.demarrer_combat()
            message = self.game.enregistrer_pokemon_au_pokedex(self.game.pokemon_adversaire)
            self.battle_history.append(message)
        self.draw_button("🔄 New Battle", WIDTH//2 - 150, 650, 150, 50, BUTTON_BLUE, lambda: self.set_state("pokemon_selection"))
        self.draw_button("🏠 Main Menu", WIDTH//2 + 10, 650, 150, 50, BUTTON_GRAY, lambda: self.set_state("main_menu"))

    def add_pokemon(self):
        self.screen.fill(BG_COLOR)
        self.draw_text("➕ Add Pokemon", FONT_TITLE, TEXT_COLOR, WIDTH//2, 50, center=True)
        pygame.draw.rect(self.screen, FRAME_COLOR, (100, 100, 700, 500))
        fields = [
            ("Name:", "name", 120),
            ("HP:", "hp", 200),
            ("Level:", "level", 240),
            ("Attack:", "attack", 280),
            ("Defense:", "defense", 320)
        ]
        for label, key, y in fields:
            self.draw_text(label, FONT_NORMAL, TEXT_COLOR, 120, y)
            if self.current_input_field == key:
                self.screen.blit(self.text_input.surface, (300, y))
            else:
                self.draw_text(self.form_data[key], FONT_NORMAL, TEXT_COLOR, 300, y)
                if pygame.Rect(300, y, 400, 30).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    self.current_input_field = key
                    self.text_input.value = self.form_data[key]
        # Type1
        self.draw_text("Type 1:", FONT_NORMAL, TEXT_COLOR, 120, 160)
        self.draw_button(self.form_data["type1"], 300, 160, 200, 30, BUTTON_BLUE, lambda: self.cycle_type("type1"))
        # Type2
        self.draw_text("Type 2 (optional):", FONT_NORMAL, TEXT_COLOR, 120, 360)
        self.draw_button(self.form_data["type2"], 300, 360, 200, 30, BUTTON_BLUE, lambda: self.cycle_type("type2"))
        self.draw_button("✅ Add", WIDTH//2 - 100, 620, 150, 50, BUTTON_GREEN, self.confirm_add_pokemon)
        self.draw_button("🔙 Back", WIDTH//2 + 60, 620, 150, 50, BUTTON_GRAY, lambda: self.set_state("main_menu"))

    def cycle_type(self, key):
        types_list = list(TYPE_DAMAGE.keys())
        types = types_list if key == "type1" else ["None"] + types_list
        current = self.form_data[key]
        index = types.index(current) if current in types else 0
        self.form_data[key] = types[(index + 1) % len(types)]

    def confirm_add_pokemon(self):
        try:
            name = self.form_data["name"].strip()
            type1 = self.form_data["type1"]
            type2 = self.form_data["type2"]
            hp = int(self.form_data["hp"])
            level = int(self.form_data["level"])
            attack = int(self.form_data["attack"])
            defense = int(self.form_data["defense"])
            if not name:
                return  # Error handling
            types = [type1]
            if type2 != "None":
                types.append(type2)
            message = self.game.ajouter_pokemon_personnalise(name, types, hp, level, attack, defense)
            self.set_state("main_menu")
        except ValueError:
            pass  # Error handling

    def pokedex(self):
        self.screen.fill(BG_COLOR)
        self.draw_text("📖 POKEDEX 📖", FONT_TITLE, TEXT_COLOR, WIDTH//2, 50, center=True)
        self.pokedex_content = self.game.obtenir_pokedex().afficher_pokedex()
        self.draw_scrolled_text(self.pokedex_content, 50, 100, 800, 500)
        self.draw_button("🔙 Back to Menu", WIDTH//2 - 100, 620, 200, 50, BUTTON_GRAY, lambda: self.set_state("main_menu"))

    def set_state(self, new_state):
        self.state = new_state
        self.scroll_offset = 0
        if new_state == "pokedex":
            self.pokedex_content = self.game.obtenir_pokedex().afficher_pokedex()

    def run(self):
        while True:
            self.handle_events()
            if self.state == "main_menu":
                self.main_menu()
            elif self.state == "pokemon_selection":
                self.pokemon_selection()
            elif self.state == "battle":
                self.battle()
            elif self.state == "add_pokemon":
                self.add_pokemon()
            elif self.state == "pokedex":
                self.pokedex()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    GraphicalInterface()
import pygame
import pygame_textinput
from game import Game
from type import TYPE_DAMAGE
from constants import *
import os
import sys

# Initialize Pygame
pygame.init()

class GraphicalInterface:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pokemon Game")
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.state = "main_menu"
        self.selected_pokemon_index = -1
        self.battle_history = []
        self.pokedex_content = []
        self.scroll_offset = 0
        self.button_clicked = False
        self.text_input = pygame_textinput.TextInputVisualizer(font_object=FONT_NORMAL)
        self.current_input_field = None
        self.type_list = list(TYPE_DAMAGE.keys())
        self.form_data = {
            "name": "",
            "type1": self.type_list[0],
            "type2": "None",
            "hp": "",
            "level": "",
            "attack": "",
            "defense": ""
        }
        self.battle_done = False
        self.running = True  # Flag to control the main loop
        
        # Load background images
        self.backgrounds = {}
        self.load_backgrounds()
        
        self.run()

    def load_backgrounds(self):
        """Load background images if they exist"""
        background_files = {
            "main_menu": "assets/images/menu.png",
            "pokemon_selection": "assets/images/selection.png",
            "battle": "assets/images/battle.png",
            "add_pokemon": "assets/images/add.png",
            "pokedex": "assets/images/pokedex.png"
        }
        
        for state, filepath in background_files.items():
            if os.path.exists(filepath):
                try:
                    bg = pygame.image.load(filepath)
                    # Resize image to screen size
                    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
                    self.backgrounds[state] = bg
                except:
                    self.backgrounds[state] = None
            else:
                self.backgrounds[state] = None

    def draw_background(self, state):
        """Display background image if it exists, otherwise fill with color"""
        if self.backgrounds.get(state):
            self.screen.blit(self.backgrounds[state], (0, 0))
        else:
            self.screen.fill(BG_COLOR)

    def draw_text(self, text, font, color, x, y, center=False):
        render = font.render(text, True, color)
        if center:
            rect = render.get_rect(center=(x, y))
            self.screen.blit(render, rect)
        else:
            self.screen.blit(render, (x, y))

    def draw_button(self, text, x, y, width, height, color, action=None):
     mouse = pygame.mouse.get_pos()
     rect = pygame.Rect(x, y, width, height)
     pygame.draw.rect(self.screen, color, rect)
     self.draw_text(text, FONT_BUTTON, TEXT_COLOR, x + width // 2, y + height // 2, center=True)
     if rect.collidepoint(mouse) and action and self.button_clicked:
        action()

    def draw_listbox(self, items, x, y, width, height, selected_index):
        pygame.draw.rect(self.screen, FRAME_COLOR, (x, y, width, height))
        item_height = 30
        visible_items = height // item_height
        start = max(0, selected_index - visible_items // 2)
        
        # Draw items
        for i in range(start, min(len(items), start + visible_items)):
            color = BUTTON_BLUE if i == selected_index else FRAME_COLOR
            item_rect = pygame.Rect(x, y + (i - start) * item_height, width, item_height)
            pygame.draw.rect(self.screen, color, item_rect)
            self.draw_text(items[i], FONT_NORMAL, TEXT_COLOR, x + 10, y + (i - start) * item_height + 5)

    def draw_scrolled_text(self, lines, x, y, width, height):
        pygame.draw.rect(self.screen, FRAME_COLOR, (x, y, width, height))
        line_height = 20
        visible_lines = height // line_height
        start = self.scroll_offset
        for i in range(start, min(len(lines), start + visible_lines)):
            self.draw_text(lines[i], FONT_COURIER, TEXT_COLOR, x + 10, y + (i - start) * line_height)

    def quit_game(self):
        """Clean method to quit the game"""
        self.game.quit_game()
        self.running = False

    def handle_events(self):
        self.button_clicked = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()
                return
            
            # Handle text input fields
            if self.current_input_field:
                self.text_input.update(events)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.form_data[self.current_input_field] = self.text_input.value
                    self.current_input_field = None
                    self.text_input = pygame_textinput.TextInputVisualizer(font_object=FONT_NORMAL)
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
               self.button_clicked = True
            
            # Handle clicks on the Pokémon selection listbox
            if self.state == "pokemon_selection" and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                listbox_x, listbox_y = 50, 100
                listbox_width, listbox_height = 800, 400
                
                if listbox_x <= mouse_x <= listbox_x + listbox_width and \
                   listbox_y <= mouse_y <= listbox_y + listbox_height:
                    item_height = 30
                    relative_y = mouse_y - listbox_y
                    clicked_index = relative_y // item_height
                    
                    visible_items = listbox_height // item_height
                    start = max(0, self.selected_pokemon_index - visible_items // 2)
                    actual_index = start + clicked_index
                    
                    if 0 <= actual_index < len(self.game.get_pokemon_list()):
                        self.selected_pokemon_index = actual_index
            
            # Handle mouse wheel scrolling
            if event.type == pygame.MOUSEWHEEL:
                if self.state == "pokedex":
                    self.scroll_offset = max(
                        0,
                        min(self.scroll_offset - event.y, len(self.pokedex_content) - 10)
                    )
             

    def main_menu(self):
        self.draw_background("main_menu")
        self.draw_text("POKEMON GAME", FONT_TITLE, TEXT_COLOR, WIDTH // 2, 50, center=True)
        self.draw_text("Catch them all!", FONT_NORMAL, (149, 165, 166), WIDTH // 2, 100, center=True)
        self.draw_button("Start Game", WIDTH // 2 - 125, 200, 250, 50, BUTTON_GREEN,
                         lambda: self.set_state("pokemon_selection"))
        self.draw_button("Add Pokemon", WIDTH // 2 - 125, 270, 250, 50, BUTTON_BLUE,
                         lambda: self.set_state("add_pokemon"))
        self.draw_button("View Pokedex", WIDTH // 2 - 125, 340, 250, 50, BUTTON_ORANGE,
                         lambda: self.set_state("pokedex"))
        self.draw_button("Quit", WIDTH // 2 - 125, 410, 250, 50, BUTTON_RED, self.quit_game)

    def pokemon_selection(self):
        self.draw_background("pokemon_selection")
        self.draw_text("Choose Your Pokemon", FONT_TITLE, TEXT_COLOR, WIDTH // 2, 50, center=True)
        pokemons = self.game.get_pokemon_list()
        items = []
        for i, pokemon in enumerate(pokemons):
            types_str = "/".join(pokemon.get_type())
            items.append(
                f"{i + 1}. {pokemon.name} ({types_str}) - Lv.{pokemon.level} "
                f"- ATK:{pokemon.get_attack()} DEF:{pokemon.defense}"
            )
        self.draw_listbox(items, 50, 100, 800, 400, self.selected_pokemon_index)
        
        if self.selected_pokemon_index == -1:
            self.draw_text("Click on a Pokemon to select it", FONT_SMALL, (255, 200, 0),
                           WIDTH // 2, 520, center=True)
        
        self.draw_button("Confirm", WIDTH // 2 - 100, 550, 150, 50, BUTTON_GREEN,
                         self.confirm_pokemon_selection)
        self.draw_button("Back", WIDTH // 2 + 60, 550, 150, 50, BUTTON_GRAY,
                         lambda: self.set_state("main_menu"))

    def confirm_pokemon_selection(self):
        if self.selected_pokemon_index >= 0:
            self.game.choose_player_pokemon(self.selected_pokemon_index)
            self.game.choose_random_opponent_pokemon()
            self.game.fight = None 
            self.battle_done = False
            self.battle_history = []
            self.game.start_battle()  
            self.set_state("battle")

    def battle(self):
        self.draw_background("battle")
        self.draw_text("POKEMON BATTLE", FONT_TITLE, TEXT_COLOR, WIDTH // 2, 50, center=True)

        pygame.draw.rect(self.screen, BUTTON_GREEN, (100, 100, 300, 150))
        self.draw_text("YOUR POKEMON", FONT_BUTTON, TEXT_COLOR, 250, 110, center=True)
        
        if self.game.player_pokemon:
            pokemon_info = str(self.game.player_pokemon).split('\n')
            y_offset = 130
            for line in pokemon_info[:5]:
                self.draw_text(line, FONT_SMALL, TEXT_COLOR, 110, y_offset)
                y_offset += 15

        self.draw_text("VS", FONT_TITLE, BUTTON_RED, WIDTH // 2, 175, center=True)

        pygame.draw.rect(self.screen, BUTTON_RED, (500, 100, 300, 150))
        self.draw_text("OPPONENT", FONT_BUTTON, TEXT_COLOR, 650, 110, center=True)
        
        if self.game.opponent_pokemon:
            opponent_info = str(self.game.opponent_pokemon).split('\n')
            y_offset = 130
            for line in opponent_info[:5]:
                self.draw_text(line, FONT_SMALL, TEXT_COLOR, 510, y_offset)
                y_offset += 15

        self.draw_scrolled_text(self.battle_history, 50, 300, 800, 250)
        
        if not self.battle_done:
            self.draw_button("FIGHT!", WIDTH // 2 - 230, 580, 140, 50,
                 (243, 156, 18), self.start_battle)
            self.draw_button("Potion", WIDTH // 2 - 70, 580, 140, 50,
                 BUTTON_GREEN, self.use_potion)
            self.draw_button("Escape", WIDTH // 2 + 90, 580, 140, 50,
                 BUTTON_RED, self.escape)
        else:
            self.draw_button("Back to Menu", WIDTH // 2 - 100, 580, 200, 50,
                             BUTTON_GRAY, lambda: self.set_state("main_menu"))
            
    def use_potion(self):
     if not self.battle_done and self.game.fight:
        self.game.use_potion()
        self.battle_history.append(
            f"{self.game.player_pokemon.name} used a potion! "
            f"({self.game.player_pokemon.hp}/{self.game.player_pokemon.hp_max}HP)")

    def escape(self):
      if not self.battle_done and self.game.fight:
        escaped = self.game.try_to_escape()
        if escaped:
            self.battle_history.append("You escaped!")
            self.battle_done = True
        else:
            self.battle_history.append("Escape failed! Opponent attacks!")
            self.battle_history.append(
                f"{self.game.player_pokemon.name}: "
                f"{self.game.player_pokemon.hp}/{self.game.player_pokemon.hp_max}HP")
            if not self.game.player_pokemon.is_alive():
                self.battle_history.append(f"{self.game.player_pokemon.name} fainted!")
                self.battle_done = True

    def start_battle(self):
      if self.battle_done or not self.game.fight:
        return

      result,message = self.game.battle_turn()

      for msg in message:
          self.battle_history.append(msg)

      hp_msg = (f"{self.game.player_pokemon.name}: {self.game.player_pokemon.hp}/{self.game.player_pokemon.hp_max}HP  |  "
              f"{self.game.opponent_pokemon.name}: {self.game.opponent_pokemon.hp}/{self.game.opponent_pokemon.hp_max}HP")
      self.battle_history.append(hp_msg)

      if result is True:
        self.battle_history.append(f">>> {self.game.player_pokemon.name} WINS!")
        old_xp = self.game.player_pokemon.xp
        old_level = self.game.player_pokemon.level
        evo_msg=self.game.player_pokemon.raise_xp_level(self.game.all_data)
        self.battle_history.append(f"+50 XP! ({self.game.player_pokemon.xp}/100)")
        if self.game.player_pokemon.level > old_level:
         self.battle_history.append(f"Level UP! {old_level} → {self.game.player_pokemon.level}")
        if evo_msg:
            self.battle_history.append(f">>> {evo_msg}")
        
        captured = self.game.fight.catch_pokemon()
        if captured:
         self.battle_history.append(f"You caught {self.game.opponent_pokemon.name}!")
        else:
         self.battle_history.append(f"{self.game.opponent_pokemon.name} escaped!")

        self.game.add_to_pokedex(self.game.opponent_pokemon, captured)
        self.battle_done = True
      elif result is False:
        self.battle_history.append(f">>> {self.game.player_pokemon.name} loses...")
        self.game.add_to_pokedex(self.game.opponent_pokemon, False)
        self.battle_done = True

    def add_pokemon(self):
        self.draw_background("add_pokemon")
        self.draw_text("Add Pokemon", FONT_TITLE, TEXT_COLOR, WIDTH // 2, 50, center=True)
        pygame.draw.rect(self.screen, FRAME_COLOR, (100, 100, 700, 500))

        fields = [
            ("Name:", "name", 120),
            ("HP:", "hp", 200),
            ("Level:", "level", 240),
            ("Attack:", "attack", 280),
            ("Defense:", "defense", 320),
        ]

        for label, key, y in fields:
            self.draw_text(label, FONT_NORMAL, TEXT_COLOR, 120, y)
            if self.current_input_field == key:
                self.screen.blit(self.text_input.surface, (300, y))
            else:
                self.draw_text(self.form_data[key], FONT_NORMAL, TEXT_COLOR, 300, y)
                if pygame.Rect(300, y, 400, 30).collidepoint(pygame.mouse.get_pos()) \
                        and pygame.mouse.get_pressed()[0]:
                    self.current_input_field = key
                    self.text_input.value = self.form_data[key]

        self.draw_text("Type 1:", FONT_NORMAL, TEXT_COLOR, 120, 160)
        self.draw_button(self.form_data["type1"], 300, 160, 200, 30,
                         BUTTON_BLUE, lambda: self.cycle_type("type1"))

        self.draw_text("Type 2 (optional):", FONT_NORMAL, TEXT_COLOR, 120, 360)
        self.draw_button(self.form_data["type2"], 300, 360, 200, 30,
                         BUTTON_BLUE, lambda: self.cycle_type("type2"))

        self.draw_button("Add", WIDTH // 2 - 100, 620, 150, 50,
                         BUTTON_GREEN, self.confirm_add_pokemon)
        self.draw_button("Back", WIDTH // 2 + 60, 620, 150, 50,
                         BUTTON_GRAY, lambda: self.set_state("main_menu"))

    def cycle_type(self, key):
        types = list(TYPE_DAMAGE.keys()) if key == "type1" else ["None"] + list(TYPE_DAMAGE.keys())
        current = self.form_data[key]
        index = types.index(current) if current in types else 0
        self.form_data[key] = types[(index + 1) % len(types)]

    def confirm_add_pokemon(self):
        try:
            name = self.form_data["name"].strip()
            if not name:
                return

            types = [self.form_data["type1"]]
            if self.form_data["type2"] != "None":
                types.append(self.form_data["type2"])

            self.game.add_custom_pokemon(
                name,
                types,
                int(self.form_data["hp"]),
                int(self.form_data["level"]),
                int(self.form_data["attack"]),
                int(self.form_data["defense"])
            )
            self.set_state("main_menu")

        except ValueError:
            pass

    def pokedex(self):
        self.draw_background("pokedex")
        self.draw_text("POKEDEX", FONT_TITLE, TEXT_COLOR, WIDTH // 2, 50, center=True)
        self.pokedex_content = self.game.get_pokedex().display_pokedex()
        self.draw_scrolled_text(self.pokedex_content, 50, 100, 800, 500)
        self.draw_button("Back to Menu", WIDTH // 2 - 100, 620, 200, 50,
                         BUTTON_GRAY, lambda: self.set_state("main_menu"))

    def set_state(self, new_state):
        self.state = new_state
        self.scroll_offset = 0
        self.selected_pokemon_index = -1
        if new_state == "pokedex":
            self.pokedex_content = self.game.get_pokedex().display_pokedex()

    def run(self):
        while self.running:
            self.handle_events()
            if not self.running:
                break
                
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
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    GraphicalInterface()
import pygame
import pygame_textinput
import os
import sys
from src.game import Game
from src.type import TYPE_DAMAGE
from src.constants import *
from src.sounds_manager import SoundManager

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
        self.running = True
        self.flash_messages = []  
        self.battle_winner = None

        # Audio
        self.sound = SoundManager()
        self.sound.play_menu()
        
        # Load background images
        self.backgrounds = {}
        self.load_backgrounds()
        
        self.run()

    def load_backgrounds(self):
        """Load background images"""
        background_files = {
            "main_menu": "assets/backgrounds/menu.png",
            "pokemon_selection": "assets/backgrounds/selection.png",
            "battle": "assets/backgrounds/battle.png",
            "add_pokemon": "assets/backgrounds/add.png",
            "pokedex": "assets/backgrounds/pokedex.png"
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
        """Display background image"""
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
            
            # Handle clicks on the Pokemon selection listbox
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
            self.flash_messages = []
            self.battle_winner = None
            self.game.start_battle()
            self.sound.play_battle()
            self.set_state("battle")

    def draw_pokemon_sprite(self, pokemon, cx, cy, size=160, flip=False):
        if pokemon and pokemon.sprite:
            sprite = pygame.transform.scale(pokemon.sprite, (size, size))
            if flip:
                sprite = pygame.transform.flip(sprite, True, False)
            rect = sprite.get_rect(center=(cx, cy))
            self.screen.blit(sprite, rect)
        else:
            # Placeholder if no sprite
            box = pygame.Rect(cx - size // 2, cy - size // 2, size, size)
            pygame.draw.rect(self.screen, FRAME_COLOR, box, border_radius=10)
            self.draw_text("?", FONT_TITLE, TEXT_COLOR, cx, cy, center=True)

    def draw_hp_bar(self, pokemon, x, y, width=200):
        """HP bar colored with text"""
        bar_h = 14
        ratio = max(0.0, pokemon.hp / pokemon.hp_max)
        if ratio > 0.5:
            color = BUTTON_GREEN
        elif ratio > 0.25:
            color = BUTTON_ORANGE
        else:
            color = BUTTON_RED
        pygame.draw.rect(self.screen, (40, 40, 40), (x, y, width, bar_h), border_radius=5)
        if ratio > 0:
            pygame.draw.rect(self.screen, color, (x, y, int(width * ratio), bar_h), border_radius=5)
        pygame.draw.rect(self.screen, (200, 200, 200), (x, y, width, bar_h), 1, border_radius=5)
        self.draw_text(f"HP: {pokemon.hp}/{pokemon.hp_max}", FONT_SMALL, TEXT_COLOR, x, y + bar_h + 3)

    def draw_info_panel(self, pokemon, x, y, width=250, align_right=False):
        """Panel name / type / HP bar semi-transparent."""
        s = pygame.Surface((width, 70), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        self.screen.blit(s, (x, y))
        name_x = x + width - 8 if align_right else x + 8
        self.draw_text(f"{pokemon.name}  Lv.{pokemon.level}", FONT_BUTTON, TEXT_COLOR,
                       name_x, y + 8, center=align_right)
        types_str = "/".join(pokemon.get_type())
        self.draw_text(types_str, FONT_SMALL, (180, 220, 255),
                       name_x, y + 26, center=align_right)
        bar_x = x + (width - 200) // 2
        self.draw_hp_bar(pokemon, bar_x, y + 44, width=200)

    def draw_flash_messages(self):
        """Show last tour message under sprites"""
        if not self.flash_messages:
            return
        panel_w = 600
        line_h = 26
        panel_h = len(self.flash_messages) * line_h + 20
        px = WIDTH // 2 - panel_w // 2
        py = 430  # under sprites
        s = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        s.fill((0, 0, 0, 190))
        self.screen.blit(s, (px, py))
        pygame.draw.rect(self.screen, (255, 220, 0), (px, py, panel_w, panel_h), 2, border_radius=6)
        for i, (msg, color) in enumerate(self.flash_messages):
            self.draw_text(msg, FONT_NORMAL, color, WIDTH // 2, py + 10 + i * line_h, center=True)

    def draw_winner_banner(self):
        if self.battle_winner == "player":
            text = f"  {self.game.player_pokemon.name} WINS!"
            color = (255, 215, 0)
            bg = (30, 100, 30, 210)
        elif self.battle_winner == "opponent":
            text = f"  {self.game.player_pokemon.name} fainted..."
            color = (255, 80, 80)
            bg = (100, 20, 20, 210)
        elif self.battle_winner == "escaped":
            text = "  You escaped!"
            color = (150, 220, 255)
            bg = (20, 60, 100, 210)
        else:
            return

        bw, bh = 600, 70
        bx, by = WIDTH // 2 - bw // 2, 440
        s = pygame.Surface((bw, bh), pygame.SRCALPHA)
        s.fill(bg)
        self.screen.blit(s, (bx, by))
        pygame.draw.rect(self.screen, color, (bx, by, bw, bh), 3, border_radius=10)
        self.draw_text(text, FONT_TITLE, color, WIDTH // 2, by + bh // 2, center=True)

    def battle(self):
        self.draw_background("battle")

        # Title
        self.draw_text("POKEMON BATTLE", FONT_TITLE, TEXT_COLOR, WIDTH // 2, 22, center=True)

        # Sprites and infos
        SPRITE_Y = 310
        if self.game.player_pokemon:
            self.draw_pokemon_sprite(self.game.player_pokemon, cx=200, cy=SPRITE_Y,
                                     size=200, flip=True)
            self.draw_info_panel(self.game.player_pokemon, x=30, y=55, width=270)

        # VS
        self.draw_text("VS", FONT_TITLE, BUTTON_RED, WIDTH // 2, SPRITE_Y, center=True)

        # Opponents sprites
        if self.game.opponent_pokemon:
            self.draw_pokemon_sprite(self.game.opponent_pokemon, cx=700, cy=SPRITE_Y,
                                     size=200, flip=False)
            self.draw_info_panel(self.game.opponent_pokemon, x=600, y=55, width=270)

        # Flash message
        if self.battle_winner:
            self.draw_winner_banner()
        else:
            self.draw_flash_messages()

        # Buttons
        if not self.battle_done:
            self.draw_button("FIGHT!", WIDTH // 2 - 230, 620, 140, 50,
                             (243, 156, 18), self.start_battle)
            self.draw_button("Potion", WIDTH // 2 - 70, 620, 140, 50,
                             BUTTON_GREEN, self.use_potion)
            self.draw_button("Escape", WIDTH // 2 + 90, 620, 140, 50,
                             BUTTON_RED, self.escape)
        else:
            self.draw_button("Back to Menu", WIDTH // 2 - 100, 620, 200, 50,
                             BUTTON_GRAY, lambda: self.set_state("main_menu"))
            
    def use_potion(self):
        if not self.battle_done and self.game.fight:
            self.game.use_potion()
            msg = (f"{self.game.player_pokemon.name} used a potion! "
                   f"({self.game.player_pokemon.hp}/{self.game.player_pokemon.hp_max} HP)")
            self.battle_history.append(msg)
            self.flash_messages = [(msg, BUTTON_GREEN)]

    def escape(self):
        if not self.battle_done and self.game.fight:
            escaped = self.game.try_to_escape()
            if escaped:
                self.battle_history.append("You escaped!")
                self.flash_messages = [("You escaped!", (150, 220, 255))]
                self.battle_winner = "escaped"
                self.battle_done = True
            else:
                atk_msg = (f"Escape failed! {self.game.opponent_pokemon.name} attacks!")
                hp_msg = (f"{self.game.player_pokemon.name}: "
                          f"{self.game.player_pokemon.hp}/{self.game.player_pokemon.hp_max} HP")
                self.battle_history.append(atk_msg)
                self.battle_history.append(hp_msg)
                self.flash_messages = [
                    ("Escape failed!", BUTTON_RED),
                    (hp_msg, TEXT_COLOR),
                ]
                if not self.game.player_pokemon.is_alive():
                    self.battle_history.append(f"{self.game.player_pokemon.name} fainted!")
                    self.flash_messages.append((f"{self.game.player_pokemon.name} fainted!", BUTTON_RED))
                    self.battle_winner = "opponent"
                    self.battle_done = True

    def start_battle(self):
        if self.battle_done or not self.game.fight:
            return

        result, message = self.game.battle_turn()

        # Build flash message
        self.flash_messages = []
        for msg in message:
            self.battle_history.append(msg)
            color = (255, 220, 50) if "super effective" in msg.lower() else \
                    (255, 100, 100) if "no effect" in msg.lower() else \
                    (200, 200, 200) if "missed" in msg.lower() else TEXT_COLOR
            self.flash_messages.append((msg, color))

        hp_msg = (f"{self.game.player_pokemon.name}: {self.game.player_pokemon.hp}/"
                  f"{self.game.player_pokemon.hp_max} HP   |   "
                  f"{self.game.opponent_pokemon.name}: {self.game.opponent_pokemon.hp}/"
                  f"{self.game.opponent_pokemon.hp_max} HP")
        self.battle_history.append(hp_msg)
        self.flash_messages.append((hp_msg, (180, 180, 255)))

        if result is True:
            old_level = self.game.player_pokemon.level
            evo_msg = self.game.player_pokemon.raise_xp_level(self.game.all_data)
            xp_line = f"+50 XP! ({self.game.player_pokemon.xp}/100)"
            self.battle_history.append(f" {self.game.player_pokemon.name} WINS!")
            self.battle_history.append(xp_line)
            if self.game.player_pokemon.level > old_level:
                lv_line = f"Level UP! {old_level} → {self.game.player_pokemon.level}"
                self.battle_history.append(lv_line)
            if evo_msg:
                self.battle_history.append(f" {evo_msg}")

            captured = self.game.fight.catch_pokemon()
            if captured:
                self.battle_history.append(f"You caught {self.game.opponent_pokemon.name}!")
            else:
                self.battle_history.append(f"{self.game.opponent_pokemon.name} escaped!")

            self.game.add_to_pokedex(self.game.opponent_pokemon, captured)
            self.battle_winner = "player"
            self.battle_done = True

        elif result is False:
            self.battle_history.append(f" {self.game.player_pokemon.name} loses...")
            self.game.add_to_pokedex(self.game.opponent_pokemon, False)
            self.battle_winner = "opponent"
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
        # handle game sounds
        if new_state == "add_pokemon":
            self.sound.play_add_sfx()  # one-shot over menu.mp3
        
        # back to menu.mp3 if we left battle screen
        if self.state == "battle" and new_state != "battle":
            self.sound.stop_battle()

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
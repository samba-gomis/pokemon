# 🎮 Pokémon Battle Game

A fully functional Pokémon battle game built with Python and Pygame, featuring turn-based combat, Pokédex management, and custom Pokémon creation.

![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.6+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [How to Play](#-how-to-play)
- [Project Structure](#-project-structure)
- [Game Mechanics](#-game-mechanics)
- [Customization](#-customization)
- [Technical Details](#-technical-details)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Gameplay
- 🎯 **Turn-based combat system** with type advantages
- 📊 **36 Generation 1 Pokémon** with authentic stats
- 🔄 **Evolution system** - Pokémon evolve at specific levels
- 💪 **Experience and leveling** - Pokémon grow stronger after battles
- 📖 **Pokédex tracking** - Keep track of captured and encountered Pokémon

### User Interface
- 🖼️ **Custom backgrounds** support for all screens
- 🎨 **Sprite support** for all Pokémon
- 📝 **Battle log** with detailed combat information
- 🖱️ **Click-based selection** for easy navigation
- ⚙️ **Smooth animations** and responsive controls

### Additional Features
- ➕ **Custom Pokémon creator** - Design your own Pokémon
- 🎲 **Random opponent selection** for varied battles
- 💾 **Automatic save system** for Pokédex entries
- 🛡️ **Type effectiveness system** following official Pokémon rules

---

## 📸 Screenshots

### Main Menu
```
┌─────────────────────────────────────┐
│         POKEMON GAME                │
│       Catch them all!               │
│                                     │
│       [ Start Game      ]           │
│       [ Add Pokemon     ]           │
│       [ View Pokedex    ]           │
│       [ Quit            ]           │
└─────────────────────────────────────┘
```

### Battle Screen
```
┌─────────────────────────────────────┐
│       POKEMON BATTLE                │
│                                     │
│  [YOUR POKEMON]      VS  [OPPONENT] │
│   Pikachu (Lv.5)        Bulbasaur   │
│   HP: 35/35             HP: 45/45   │
│   Type: Electric        Type: Grass │
│                                     │
│  ⚔️ Pikachu attacks Bulbasaur       │
│     and deals 42 damage!            │
│  ⚔️ Bulbasaur attacks Pikachu       │
│     and deals 25 damage             │
│     (Not very effective...)         │
│                                     │
│         [ FIGHT! ]                  │
└─────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/pokemon-game.git
cd pokemon-game
```

### Step 2: Install dependencies

```bash
pip install -r requirement.txt
```

Or manually:
```bash
pip install pygame
pip install pygame_textinput
```

### Step 3: Run the game

```bash
python main.py
```

---

## 🎮 How to Play

### Starting a Battle

1. **Launch the game** - Run `python main.py`
2. **Click "Start Game"** from the main menu
3. **Select your Pokémon** - Click on a Pokémon from the list
4. **Click "Confirm"** - Your opponent will be randomly selected
5. **Click "FIGHT!"** - The battle begins automatically

### Battle System

- Battles are **turn-based** and **automatic**
- Your Pokémon attacks first, then the opponent
- Combat continues until one Pokémon faints (HP reaches 0)
- The winner gains **XP and levels up**
- Defeated opponents are added to your **Pokédex**

### Type Advantages

The game follows official Pokémon type effectiveness:

| Attack Type | Strong Against | Weak Against |
|------------|----------------|--------------|
| 🔥 Fire | Grass, Bug, Ice, Steel | Water, Rock, Dragon |
| 💧 Water | Fire, Ground, Rock | Grass, Electric, Dragon |
| ⚡ Electric | Water, Flying | Ground, Grass, Dragon |
| 🌿 Grass | Water, Ground, Rock | Fire, Flying, Bug, Poison |
| 🧊 Ice | Grass, Ground, Flying, Dragon | Fire, Water, Steel |

*See `type.py` for the complete type chart*

### Pokédex

- View all encountered and captured Pokémon
- Shows stats: HP, Attack, Defense
- Indicates capture status: ✓ Captured / ✗ Seen only

### Custom Pokémon

Create your own Pokémon with:
- Custom name
- Type(s) selection (single or dual-type)
- Custom stats (HP, Attack, Defense)
- Custom level

---

## 📁 Project Structure

```
pokemon-game/
├── assets/
│   └── images/              # Sprites and backgrounds
│       ├── menu.png
│       ├── battle.png
│       ├── selection.png
│       ├── add.png
│       ├── pokedex.png
│       ├── pikachu.png
│       ├── bulbasaur.png
│       └── ... (other sprites)
│
├── game.py                  # Main game logic
├── graphical_interface.py   # UI and rendering
├── pokemon.py               # Pokémon class
├── pokedex.py              # Pokédex management
├── type.py                 # Type effectiveness system
├── constants.py            # Game constants (colors, fonts)
├── main.py                 # Entry point
├── test.py                 # Unit tests
│
├── pokemon.json            # Pokémon database
├── pokedex.json           # Save file for Pokédex
├── requirement.txt        # Python dependencies
└── README.md             # This file
```

---

## 🎯 Game Mechanics

### Combat System

```python
# Damage calculation
base_damage = attacker.attack * type_multiplier
final_damage = max(0, base_damage - defender.defense)
defender.hp -= final_damage
```

### Type Multipliers

- **Super Effective**: 2x damage
- **Normal**: 1x damage
- **Not Very Effective**: 0.5x or 0.75x damage
- **No Effect**: 0x damage

### Experience & Leveling

- **+10 XP** per battle won
- **100 XP** = Level up
- **Stats increase** each level:
  - HP: +5
  - HP Max: +5
  - Attack: +3
  - Defense: +3

### Evolution

- Pokémon evolve at **predetermined levels**
- Evolution is **automatic** when level requirement is met
- Stats are updated to evolved form

---

## 🎨 Customization

### Adding Custom Backgrounds

Place 900x700px PNG images in `assets/images/`:

- `menu.png` - Main menu background
- `selection.png` - Pokémon selection background
- `battle.png` - Battle screen background
- `add.png` - Add Pokémon background
- `pokedex.png` - Pokédex background

**If images are missing**, the game uses default solid colors.

### Adding Custom Sprites

1. Add sprite images to `assets/images/`
2. Update `pokemon.json` with the sprite path:

```json
{
  "37": {
    "name": "MyPokemon",
    "sprite": "assets/images/mypokemon.png",
    ...
  }
}
```

### Modifying Stats

Edit `pokemon.json`:

```json
{
  "1": {
    "name": "Pikachu",
    "type": ["Electric"],
    "level": 1,
    "hp": 35,
    "attack": 55,
    "defense": 40,
    "evolution_id": 2,
    "evolution_level": 30
  }
}
```

### Changing Colors

Edit `constants.py`:

```python
BG_COLOR = (44, 62, 80)        # Dark blue-gray
BUTTON_GREEN = (39, 174, 96)   # Green
BUTTON_RED = (231, 76, 60)     # Red
TEXT_COLOR = (236, 240, 241)   # White
```

---

## 🔧 Technical Details

### Technologies Used

- **Python 3.12** - Core language
- **Pygame 2.6** - Game framework
- **pygame_textinput** - Text input handling
- **JSON** - Data storage

### Architecture

- **MVC Pattern**: Game logic separated from UI
- **Object-Oriented**: Pokémon, Game, and Pokedex classes
- **Event-Driven**: Pygame event loop
- **File-Based Save**: JSON persistence

### Performance

- **60 FPS** target framerate
- **Instant battles** - No delays
- **Lightweight** - Low memory footprint
- **Fast startup** - Loads in <2 seconds

---

## 🐛 Troubleshooting

### Game won't start

```bash
# Check Python version
python --version  # Should be 3.12+

# Reinstall dependencies
pip install --upgrade pygame pygame_textinput
```

### Sprites not loading

- Verify sprite paths in `pokemon.json`
- Check that `assets/images/` exists
- Game will still work without sprites

### "video system not initialized" error

- The quit button should work properly now
- If issue persists, use Alt+F4 or close window

### Combat not working

- Ensure `type.py` has the `damage_multiplying` function
- Check console for error messages
- Run `python test.py` to verify all systems

### Pokédex empty

- Win at least one battle to add Pokémon
- Check that `pokedex.json` has write permissions

---

## 🧪 Testing

Run the test suite:

```bash
python test.py
```

Expected output:
```
Test 1: Checking imports... ✓
Test 2: Checking Game attributes... ✓
Test 3: Checking Pokedex.display_pokedex()... ✓
Test 4: Checking damage_multiplying... ✓
Test 5: Checking Pokemon.__str__()... ✓
Test 6: Checking add_custom_pokemon()... ✓

Passed: 6/6
✓ ALL TESTS PASSED!
```

---

## 🚀 Future Enhancements

Planned features for future versions:

- [ ] **Sound effects** and background music
- [ ] **Animations** for attacks and transitions
- [ ] **More Pokémon** (Gen 2-9)
- [ ] **Special moves** system
- [ ] **Status effects** (poison, paralysis, etc.)
- [ ] **Multiplayer mode** via network
- [ ] **Save/Load system** for game progress
- [ ] **AI difficulty levels**
- [ ] **Tournament mode**
- [ ] **Achievements system**

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Keep commits atomic and well-described

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Pokemon Game Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

- **Nintendo/Game Freak** - Original Pokémon concept
- **Pygame Community** - Excellent game framework
- **PokeAPI** - Pokémon data reference
- **Contributors** - Everyone who helped improve this project

---

## 📧 Contact

- **Project Link**: https://github.com/samba-gomis/pokemon-game
- **Issues**: https://github.com/samba-gomis/pokemon-game/issues
- **Discussions**: https://github.com/samba-gomis/pokemon-game/discussions

---

## 🎮 Enjoy the Game!

```
                 ⢀⣀⣤⣤⣤⣤⣀⡀
             ⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄
          ⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀
        ⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀
       ⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆
      ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
     ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
    ⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆
    ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
         
              Gotta Code 'Em All! 💻⚡
```

---

<p align="center">Made with ❤️ and Python</p>
<p align="center">Happy Gaming! 🎮</p>
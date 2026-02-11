import json

def save_to_pokedex(pokemon_obj, captured_status):
    try:
        with open("pokedex.json", "r") as f:
            pokedex = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pokedex = []

    if not any(p["name"] == pokemon_obj.name for p in pokedex):
        new_entry = {
            "name": pokemon_obj.name,
            "type": pokemon_obj.type,
            "hp": pokemon_obj.hp_max,
            "attack": pokemon_obj.attack,
            "defense": pokemon_obj.defense,
            "captured": captured_status
        }
        pokedex.append(new_entry)
        with open("pokedex.json", "w") as f:
            json.dump(pokedex, f, indent=4)
        return True
    return False
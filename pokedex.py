import json

class Pokedex:
    def __init__(self):
        self.entries = self.load_pokedex()

    # Now returns a list of strings
    def display_pokedex(self):
        """Returns a list of strings describing each Pokémon in the Pokédex"""
        if not self.entries:
            return ["Your Pokedex is empty. Catch some Pokemon to fill it!"]
        
        result = []
        for entry in self.entries:
            status = "✓ Captured" if entry["captured"] else "✗ Seen only"
            types = "/".join(entry["type"])
            line = (
                f"{entry['name']} ({types}) - "
                f"HP:{entry['hp']} ATK:{entry['attack']} DEF:{entry['defense']} "
                f"[{status}]"
            )
            result.append(line)
        
        return result
             
    # Function to save a Pokémon's data into the JSON file
    def save_to_pokedex(self, pokemon_obj, captured_status):
        """Saves a Pokémon into the Pokédex JSON file"""
        
        # Check if the Pokémon name is not already in the list
        if not any(p["name"] == pokemon_obj.name for p in self.entries):
            # FIXED: Use get_type() instead of .type
            new_entry = {
                "name": pokemon_obj.name,
                "type": pokemon_obj.get_type(),
                "hp": pokemon_obj.hp_max,
                "attack": pokemon_obj.get_attack(),
                "defense": pokemon_obj.defense,
                "captured": captured_status
            }
            
            # Add the new entry to the list
            self.entries.append(new_entry)
            
            # Write the updated list back into the JSON file
            try:
                with open("pokedex.json", "w") as f:
                    json.dump(self.entries, f, indent=4)
                return True
            except Exception as e:
                print(f"Error saving to pokedex.json: {e}")
                return False
        
        return False  # Returns False if the Pokémon was already in the Pokédex

    # Function to load and return the full Pokédex list
    def load_pokedex(self):
        """Loads the Pokédex from the JSON file"""
        try:
            with open("pokedex.json", "r") as f:
                content = f.read().strip()
                if not content:  # Empty file
                    return []
                return json.loads(content)
        except FileNotFoundError:
            # Create the file if it does not exist
            with open("pokedex.json", "w") as f:
                json.dump([], f)
            return []
        except json.JSONDecodeError:
            # Corrupted file, reset it
            print("Warning: pokedex.json corrupted, resetting...")
            with open("pokedex.json", "w") as f:
                json.dump([], f)
            return []
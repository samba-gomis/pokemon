import json

class Pokedex:
    def __init__(self):
        self.entries=self.load_pokedex()

    def display_pokedex(self):
       for entries in self.entries:
          print(entries["name"])
          print(entries["type"])
          print(entries["hp"])
          print(entries["attack"])
          print(entries["defense"])
          print(entries["captured"])
             
    #Function to save a Pokemon's data into the JSON file
    def save_to_pokedex(self, pokemon_obj, captured_status):

      #Check if the Pokemon name is not already in the list
      if not any(p["name"]==pokemon_obj.name for p in self.entries):
        #Prepare the data dictionary for the new entry
        new_entry = {
            "name": pokemon_obj.name,
            "type": pokemon_obj.type,
            "hp": pokemon_obj.hp_max,
            "attack": pokemon_obj.attack,
            "defense": pokemon_obj.defense,
            "captured": captured_status
        }
        #Add the new entry to our list
        self.entries.append(new_entry)
        
        #Write the updated list back into the JSON file
        with open("pokedex.json", "w") as f:
            json.dump(self.entries, f, indent=4)
        return True
      return False #Returns False if the Pokemon was already in the pokedex

    #Function to load and return the full pokedex list
    def load_pokedex(self):
      try:
        with open("pokedex.json", "r") as f:
            return json.load(f)
      except (FileNotFoundError,json.JSONDecodeError):
        #Returns an empty list if there's an error or no file
        return []
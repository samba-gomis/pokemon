#full dictionnary with the attacker type and the defenter type and their bonus

TYPE_DAMAGE = {
    "Normal": {
        "Normal": 1, "Fire": 0.75, "Water": 0.75, "Electric": 0.75, "Grass": 0.75, 
        "Ice": 0.75, "Fighting": 0.75, "Poison": 0.75, "Ground": 0.75, "Flying": 0.75, 
        "Psychic": 0.75, "Bug": 0.75, "Rock": 0.5, "Ghost": 0, "Dragon": 0.75, 
        "Dark": 0.75, "Steel": 0.5, "Fairy": 0.75},
    
    "Fire": {
        "Normal": 1, "Fire": 0.5, "Water": 0.5, "Electric": 0.75, "Grass": 2, 
        "Ice": 2, "Fighting": 0.75, "Poison": 0.75, "Ground": 0.75, "Flying": 0.75, 
        "Psychic": 0.75, "Bug": 2, "Rock": 0.5, "Ghost": 0.75, "Dragon": 0.5, 
        "Dark": 0.75, "Steel": 2, "Fairy": 0.75},
    
    "Water": {
        "Normal": 1, "Fire": 2, "Water": 0.5, "Electric": 0.75, "Grass": 0.5, 
        "Ice": 0.75, "Fighting": 0.75, "Poison": 0.75, "Ground": 2, "Flying": 0.75, 
        "Psychic": 0.75, "Bug": 0.75, "Rock": 2, "Ghost": 0.75, "Dragon": 0.5, 
        "Dark": 0.75, "Steel": 0.75, "Fairy": 0.75},
    
    "Electric": {
        "Normal": 1, "Fire": 0.75, "Water": 2, "Electric": 0.5, "Grass": 0.5, 
        "Ice": 0.75, "Fighting": 0.75, "Poison": 0.75, "Ground": 0, "Flying": 2, 
        "Psychic": 0.75, "Bug": 0.75, "Rock": 0.75, "Ghost": 0.75, "Dragon": 0.5, 
        "Dark": 0.75, "Steel": 0.75, "Fairy": 0.75},
    
    "Grass": {
        "Normal": 1, "Fire": 0.5, "Water": 2, "Electric": 0.75, "Grass": 0.5, 
        "Ice": 0.75, "Fighting": 0.75, "Poison": 0.5, "Ground": 2, "Flying": 0.5, 
        "Psychic": 0.75, "Bug": 0.5, "Rock": 2, "Ghost": 0.75, "Dragon": 0.5, 
        "Dark": 0.75, "Steel": 0.5, "Fairy": 0.75},
    
    "Ice": {
        "Normal": 1, "Fire": 0.5, "Water": 0.5, "Electric": 0.75, "Grass": 2, 
        "Ice": 0.5, "Fighting": 0.75, "Poison": 0.75, "Ground": 2, "Flying": 2, 
        "Psychic": 0.75, "Bug": 0.75, "Rock": 0.75, "Ghost": 0.75, "Dragon": 2, 
        "Dark": 0.75, "Steel": 0.5, "Fairy": 0.75},
    
    "Fighting": {
        "Normal": 2, "Fire": 0.75, "Water": 0.75, "Electric": 0.75, "Grass": 0.75, 
        "Ice": 2, "Fighting": 0.75, "Poison": 0.5, "Ground": 0.75, "Flying": 0.5, 
        "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0, "Dragon": 0.75, 
        "Dark": 2, "Steel": 2, "Fairy": 0.5},
    
    "Poison": {
        "Normal": 1, "Fire": 0.75, "Water": 0.75, "Electric": 0.75, "Grass": 2, 
        "Ice": 0.75, "Fighting": 0.75, "Poison": 0.5, "Ground": 0.5, "Flying": 0.75, 
        "Psychic": 0.75, "Bug": 0.75, "Rock": 0.5, "Ghost": 0.5, "Dragon": 0.75, 
        "Dark": 0.75, "Steel": 0, "Fairy": 2},
    
    "Ground": {
        "Normal": 1, "Fire": 2, "Water": 0.75, "Electric": 2, "Grass": 0.5, 
        "Ice": 0.75, "Fighting": 0.75, "Poison": 2, "Ground": 0.75, "Flying": 0, 
        "Psychic": 0.75, "Bug": 0.5, "Rock": 2, "Ghost": 0.75, "Dragon": 0.75, 
        "Dark": 0.75, "Steel": 2, "Fairy": 0.75},
    
    "Flying": {
        "Normal": 1, "Fire": 0.75, "Water": 0.75, "Electric": 0.5, "Grass": 2, 
        "Ice": 0.75, "Fighting": 2, "Poison": 0.75, "Ground": 0.75, "Flying": 0.75, 
        "Psychic": 0.75, "Bug": 2, "Rock": 0.5, "Ghost": 0.75, "Dragon": 0.75, 
        "Dark": 0.75, "Steel": 0.5, "Fairy": 0.75},
    
    "Psychic": {
        "Normal": 1, "Fire": 0.75, "Water": 0.75, "Electric": 0.75, "Grass": 0.75, 
        "Ice": 0.75, "Fighting": 2, "Poison": 2, "Ground": 0.75, "Flying": 0.75, 
        "Psychic": 0.5, "Bug": 0.75, "Rock": 0.75, "Ghost": 0.75, "Dragon": 0.75, 
        "Dark": 0, "Steel": 0.5, "Fairy": 0.75},
    
    "Bug": {
        "Normal": 1, "Fire": 0.5, "Water": 0.75, "Electric": 0.75, "Grass": 2, 
        "Ice": 0.75, "Fighting": 0.5, "Poison": 0.5, "Ground": 0.75, "Flying": 0.5, 
        "Psychic": 2, "Bug": 0.75, "Rock": 0.75, "Ghost": 0.5, "Dragon": 0.75, 
        "Dark": 2, "Steel": 0.5, "Fairy": 0.5},
    
    "Rock": {
        "Normal": 1, "Fire": 2, "Water": 0.75, "Electric": 0.75, "Grass": 0.75, 
        "Ice": 2, "Fighting": 0.5, "Poison": 0.75, "Ground": 0.5, "Flying": 2, 
        "Psychic": 0.75, "Bug": 2, "Rock": 0.75, "Ghost": 0.75, "Dragon": 0.75, 
        "Dark": 0.75, "Steel": 0.5, "Fairy": 0.75},
    
    "Ghost": {
        "Normal": 0, "Fire": 0.75, "Water": 0.75, "Electric": 0.75, "Grass": 0.75, 
        "Ice": 0.75, "Fighting": 0.75, "Poison": 0.75, "Ground": 0.75, "Flying": 0.75, 
        "Psychic": 2, "Bug": 0.75, "Rock": 0.75, "Ghost": 2, "Dragon": 0.75, 
        "Dark": 0.5, "Steel": 0.75, "Fairy": 0.75},
    
    "Dragon": {
        "Normal": 1, "Fire": 0.75, "Water": 0.75, "Electric": 0.75, "Grass": 0.75, 
        "Ice": 0.75, "Fighting": 0.75, "Poison": 0.75, "Ground": 0.75, "Flying": 0.75, 
        "Psychic": 0.75, "Bug": 0.75, "Rock": 0.75, "Ghost": 0.75, "Dragon": 2, 
        "Dark": 0.75, "Steel": 0.5, "Fairy": 0},
    
    "Dark": {
        "Normal": 1, "Fire": 0.75, "Water": 0.75, "Electric": 0.75, "Grass": 0.75, 
        "Ice": 0.75, "Fighting": 0.5, "Poison": 0.75, "Ground": 0.75, "Flying": 0.75, 
        "Psychic": 2, "Bug": 0.75, "Rock": 0.75, "Ghost": 2, "Dragon": 0.75, 
        "Dark": 0.5, "Steel": 0.75, "Fairy": 0.5},
    
    "Steel": {
        "Normal": 1, "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Grass": 0.75, 
        "Ice": 2, "Fighting": 0.75, "Poison": 0.75, "Ground": 0.75, "Flying": 0.75, 
        "Psychic": 0.75, "Bug": 0.75, "Rock": 2, "Ghost": 0.75, "Dragon": 0.75, 
        "Dark": 0.75, "Steel": 0.5, "Fairy": 2},
    
    "Fairy": {
        "Normal": 1, "Fire": 0.5, "Water": 0.75, "Electric": 0.75, "Grass": 0.75, 
        "Ice": 0.75, "Fighting": 2, "Poison": 0.5, "Ground": 0.75, "Flying": 0.75, 
        "Psychic": 0.75, "Bug": 0.75, "Rock": 0.75, "Ghost": 0.75, "Dragon": 2, 
        "Dark": 2, "Steel": 0.5, "Fairy": 0.75}
}

def damage_mutliplying(attacker_type,defender_type): #method to multiply the damage using the dictionnary
      total_multiplicator=1 #default multiplicator
      for t in defender_type:       
         bonus=TYPE_DAMAGE.get(attacker_type,{}).get(t,1) #get the attacker type and the defender type, leave empty if not found and leave 1 by default
         total_multiplicator*=bonus
      return total_multiplicator #return final multiplicator
"""
Test script to verify that all fixes are working correctly
"""
import sys
import os

def test_imports():
    """Test 1: Check that all imports work correctly"""
    print("Test 1: Checking imports...")
    try:
        from game import Game
        from pokemon import Pokemon
        from pokedex import Pokedex
        from type import damage_mutliplying, TYPE_DAMAGE
        print(" All imports successful")
        return True
    except ImportError as e:
        print(f" Import failed: {e}")
        return False

def test_game_attributes():
    """Test 2: Check Game attributes"""
    print("\nTest 2: Checking Game attributes...")
    try:
        from game import Game
        game = Game()
        
        # Check new attribute names
        assert hasattr(game, 'player_pokemon'), "Missing player_pokemon"
        assert hasattr(game, 'opponent_pokemon'), "Missing opponent_pokemon"
        assert hasattr(game, 'pokedex_manager'), "Missing pokedex_manager"
        
        # Check methods
        assert hasattr(game, 'add_custom_pokemon'), "Missing add_custom_pokemon method"
        assert hasattr(game, 'get_pokedex'), "Missing get_pokedex method"
        
        print(" Game attributes are correct")
        return True
    except AssertionError as e:
        print(f" Game attribute check failed: {e}")
        return False
    except Exception as e:
        print(f" Unexpected error: {e}")
        return False

def test_pokedex_return():
    """Test 3: Check that display_pokedex returns a list"""
    print("\nTest 3: Checking Pokedex.display_pokedex() return...")
    try:
        from pokedex import Pokedex
        pokedex = Pokedex()
        result = pokedex.display_pokedex()
        
        assert isinstance(result, list), f"Expected list, got {type(result)}"
        assert len(result) > 0, "Result should not be empty"
        assert isinstance(result[0], str), f"Expected str, got {type(result[0])}"
        
        print(f" display_pokedex() returns a list: {result[0]}")
        return True
    except AssertionError as e:
        print(f" Pokedex check failed: {e}")
        return False
    except Exception as e:
        print(f" Unexpected error: {e}")
        return False

def test_damage_function():
    """Test 4: Check that damage_mutliplying exists and works"""
    print("\nTest 4: Checking damage_mutliplying function...")
    try:
        from type import damage_mutliplying
        
        # Basic tests
        result = damage_mutliplying("Fire", ["Grass"])
        assert result == 2, f"Fire vs Grass should be 2x, got {result}"
        
        result = damage_mutliplying("Water", ["Fire"])
        assert result == 2, f"Water vs Fire should be 2x, got {result}"
        
        print(" damage_mutliplying works correctly")
        return True
    except Exception as e:
        print(f" damage_mutliplying test failed: {e}")
        return False

def test_pokemon_str():
    """Test 5: Check that Pokemon.__str__ returns a valid string"""
    print("\nTest 5: Checking Pokemon.__str__()...")
    try:
        # Create minimal test data
        test_data = {
            "1": {
                "name": "TestMon",
                "type": ["Normal"],
                "level": 5,
                "hp": 50,
                "attack": 40,
                "defense": 30,
                "evolution_id": None,
                "evolution_level": None,
                "sprite": "nonexistent.png"
            }
        }
        
        from pokemon import Pokemon
        pokemon = Pokemon("1", test_data)
        result = str(pokemon)
        
        assert result is not None, "str(pokemon) returned None"
        assert isinstance(result, str), f"Expected str, got {type(result)}"
        assert len(result) > 0, "str(pokemon) is empty"
        assert "TestMon" in result, "Pokemon name not found in string"
        
        print(f" Pokemon.__str__() works:\n{result[:100]}...")
        return True
    except Exception as e:
        print(f" Pokemon.__str__() test failed: {e}")
        return False

def test_add_custom_pokemon():
    """Test 6: Check that add_custom_pokemon works"""
    print("\nTest 6: Checking add_custom_pokemon()...")
    try:
        from game import Game
        game = Game()
        
        initial_count = len(game.pokemons)
        
        # Add a custom Pokémon
        new_pokemon = game.add_custom_pokemon(
            name="TestPokemon",
            types=["Fire", "Flying"],
            hp=100,
            level=10,
            attack=80,
            defense=60
        )
        
        assert len(game.pokemons) == initial_count + 1, "Pokemon not added to list"
        assert new_pokemon.name == "TestPokemon", "Wrong name"
        assert new_pokemon.get_type() == ["Fire", "Flying"], "Wrong types"
        
        print(" add_custom_pokemon() works correctly")
        return True
    except Exception as e:
        print(f" add_custom_pokemon() test failed: {e}")
        return False

def run_all_tests():
    """Runs all tests"""
    print("=" * 60)
    print("RUNNING VALIDATION TESTS")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_game_attributes,
        test_pokedex_return,
        test_damage_function,
        test_pokemon_str,
        test_add_custom_pokemon
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f" Test crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print(" ALL TESTS PASSED! You're good to go!")
        return True
    else:
        print(" Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
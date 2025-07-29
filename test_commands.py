#!/usr/bin/env python3
"""
Test script untuk memverifikasi semua perintah game berfungsi
"""

from game_state import GameState
from game import Game

def test_game_state():
    """Test GameState initialization"""
    print("Testing GameState initialization...")
    state = GameState()
    
    # Test basic properties
    assert state.player_name == "Pahlawan"
    assert state.current_location == "hutan"
    assert state.health == 100
    assert state.game_over == False
    
    # Test locations
    assert "hutan" in state.locations
    assert "gua" in state.locations
    assert "kota" in state.locations
    
    # Test quests
    assert len(state.quests) == 3
    quest_ids = [q.quest_id for q in state.quests]
    assert "quest_1" in quest_ids
    assert "quest_2" in quest_ids
    assert "quest_3" in quest_ids
    
    print("✅ GameState initialization passed!")

def test_location_movement():
    """Test location movement"""
    print("Testing location movement...")
    state = GameState()
    
    # Test initial location
    assert state.current_location == "hutan"
    
    # Test valid movement
    assert state.move_to("gua") == True
    assert state.current_location == "gua"
    
    # Test invalid movement
    assert state.move_to("kastil") == False  # Can't go directly from gua to kastil
    assert state.current_location == "gua"  # Should still be in gua
    
    # Test available locations
    available = state.get_available_locations()
    assert "hutan" in available
    assert "dalam_gua" in available
    
    print("✅ Location movement passed!")

def test_inventory_system():
    """Test inventory system"""
    print("Testing inventory system...")
    state = GameState()
    
    # Test initial inventory
    assert len(state.inventory) == 0
    
    # Test adding item
    from game_state import Item
    test_item = Item("test_sword", "A test sword", 2.0, 50, True)
    state.add_item_to_inventory(test_item)
    assert len(state.inventory) == 1
    assert state.inventory[0].name == "test_sword"
    
    # Test has_item
    assert state.has_item("test_sword") == True
    assert state.has_item("nonexistent") == False
    
    # Test remove item
    assert state.remove_item_from_inventory("test_sword") == True
    assert len(state.inventory) == 0
    assert state.remove_item_from_inventory("nonexistent") == False
    
    print("✅ Inventory system passed!")

def test_quest_system():
    """Test quest system"""
    print("Testing quest system...")
    state = GameState()
    
    # Test quest initialization
    assert len(state.quests) == 3
    
    # Test starting quest
    assert state.start_quest("quest_1") == True
    quest_1 = next(q for q in state.quests if q.quest_id == "quest_1")
    assert quest_1.started == True
    assert quest_1.completed == False
    
    # Test starting same quest again
    assert state.start_quest("quest_1") == False
    
    # Test quest progress
    progress = state.get_quest_progress("quest_1")
    assert progress is not None
    assert "ranting" in progress
    
    print("✅ Quest system passed!")

def test_game_commands():
    """Test game command handling"""
    print("Testing game command handling...")
    game = Game()
    
    # Test basic commands
    commands_to_test = [
        "help",
        "status", 
        "inventaris",
        "quest",
        "lihat"
    ]
    
    for cmd in commands_to_test:
        try:
            game.handle_command(cmd)
            print(f"✅ Command '{cmd}' works")
        except Exception as e:
            print(f"❌ Command '{cmd}' failed: {e}")
    
    print("✅ Basic command testing completed!")

def main():
    """Run all tests"""
    print("🧪 Running Game Tests...\n")
    
    try:
        test_game_state()
        test_location_movement()
        test_inventory_system()
        test_quest_system()
        test_game_commands()
        
        print("\n🎉 All tests passed! Game should work correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
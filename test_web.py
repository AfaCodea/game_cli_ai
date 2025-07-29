#!/usr/bin/env python3
"""
Test script untuk web application
"""

import requests
import json
import time

def test_web_app():
    """Test web application endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Web Application...")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure web app is running on http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False
    
    # Test 2: Start game
    try:
        response = requests.post(f"{base_url}/api/game/start", 
                               json={"session_id": "test_session"})
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print(f"✅ Game started successfully. Session ID: {session_id}")
        else:
            print(f"❌ Failed to start game. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error starting game: {e}")
        return False
    
    # Test 3: Get game status
    try:
        response = requests.get(f"{base_url}/api/game/status?session_id={session_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Game status retrieved. Player: {data.get('player_name')}")
            print(f"   Location: {data.get('current_location', {}).get('name')}")
            print(f"   Health: {data.get('health')}/{data.get('max_health')}")
        else:
            print(f"❌ Failed to get game status. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting game status: {e}")
        return False
    
    # Test 4: Execute commands
    test_commands = [
        "lihat",
        "status", 
        "inventaris",
        "help"
    ]
    
    for cmd in test_commands:
        try:
            response = requests.post(f"{base_url}/api/game/command",
                                   json={"session_id": session_id, "command": cmd})
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Command '{cmd}' executed successfully")
            else:
                print(f"❌ Command '{cmd}' failed. Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error executing command '{cmd}': {e}")
    
    print("\n🎉 Web application tests completed!")
    print("🌐 Open http://localhost:5000 in your browser to play!")
    return True

if __name__ == "__main__":
    test_web_app() 
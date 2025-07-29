#!/usr/bin/env python3
"""
Simple Web Application Test untuk Game AI Petualangan
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
        print("🔍 Testing server connection...")
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responding")
        else:
            print(f"⚠️  Server returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server.")
        print("💡 Make sure web app is running:")
        print("   - For demo: python run_demo.py")
        print("   - For full: python run_web.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False
    
    # Test 2: Start game
    try:
        print("\n🎮 Testing game start...")
        response = requests.post(f"{base_url}/api/game/start", 
                               json={"session_id": "test_session"})
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print(f"✅ Game started successfully")
            print(f"   Session ID: {session_id}")
            print(f"   Message: {data.get('message')}")
        else:
            print(f"❌ Failed to start game. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error starting game: {e}")
        return False
    
    # Test 3: Get game status
    try:
        print("\n📊 Testing game status...")
        response = requests.get(f"{base_url}/api/game/status?session_id={session_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Game status retrieved successfully")
            print(f"   Player: {data.get('player_name')}")
            print(f"   Location: {data.get('current_location', {}).get('name')}")
            print(f"   Health: {data.get('health')}/{data.get('max_health')}")
        else:
            print(f"❌ Failed to get game status. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting game status: {e}")
        return False
    
    # Test 4: Execute basic commands
    print("\n🎯 Testing basic commands...")
    test_commands = [
        ("lihat", "Look around"),
        ("status", "Check status"), 
        ("inventaris", "Check inventory"),
        ("help", "Get help")
    ]
    
    for cmd, description in test_commands:
        try:
            print(f"   Testing '{cmd}' ({description})...")
            response = requests.post(f"{base_url}/api/game/command",
                                   json={"session_id": session_id, "command": cmd})
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   ✅ '{cmd}' executed successfully")
                else:
                    print(f"   ❌ '{cmd}' failed: {data.get('error')}")
            else:
                print(f"   ❌ '{cmd}' failed with status {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error executing '{cmd}': {e}")
    
    print("\n🎉 Web application tests completed!")
    print("🌐 Open http://localhost:5000 in your browser to play!")
    return True

if __name__ == "__main__":
    test_web_app() 
#!/usr/bin/env python3
"""
Quick Demo untuk Game AI Petualangan Web
"""

import os
import sys
import subprocess
import time
import threading

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "requests"])
        print("✅ Requirements installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def start_demo_server():
    """Start the demo server in a separate thread"""
    try:
        from web_app_demo import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Server error: {e}")

def test_connection():
    """Test if server is responding"""
    import requests
    try:
        response = requests.get("http://localhost:5000", timeout=3)
        return response.status_code == 200
    except:
        return False

def main():
    """Main function"""
    print("🎮 Game AI Petualangan - Quick Demo")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Start server in background
    print("\n🚀 Starting demo server...")
    server_thread = threading.Thread(target=start_demo_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    for i in range(10):
        if test_connection():
            break
        time.sleep(1)
        print(f"   {i+1}/10 seconds...")
    else:
        print("❌ Server failed to start")
        return False
    
    print("✅ Server is running!")
    print("\n🌐 Web app is ready at: http://localhost:5000")
    print("📱 Open your browser and visit the URL above!")
    print("\n🎯 Available commands to try:")
    print("   - lihat")
    print("   - status") 
    print("   - inventaris")
    print("   - help")
    print("   - quest")
    print("   - ai_learn")
    print("   - ai_suggest")
    print("   - pergi ke [lokasi]")
    print("   - ambil [item]")
    print("   - bicara dengan [npc]")
    print("\n⏹️  Press Ctrl+C to stop")
    print("-" * 50)
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    
    return True

if __name__ == "__main__":
    main() 
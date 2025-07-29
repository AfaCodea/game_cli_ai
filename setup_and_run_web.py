#!/usr/bin/env python3
"""
Setup dan Run Web Application untuk Game AI Petualangan
"""

import os
import sys
import subprocess
import time

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-socketio", "requests"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_api_key():
    """Check if API key is set"""
    print("\n🔑 Checking API key...")
    
    # Check environment variable
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key and api_key != "ISI_API_KEY_ANDA_DISINI":
        print("✅ API key found in environment variable")
        return True
    
    # Check .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.environ.get("GOOGLE_API_KEY")
        if api_key and api_key != "ISI_API_KEY_ANDA_DISINI":
            print("✅ API key found in .env file")
            return True
    except ImportError:
        print("⚠️  python-dotenv not installed, skipping .env check")
    
    print("❌ API key not found!")
    print("\n📝 To set API key:")
    print("1. Get API key from: https://aistudio.google.com/app/apikey")
    print("2. Set environment variable:")
    print("   Windows: set GOOGLE_API_KEY=your_api_key")
    print("   Linux/Mac: export GOOGLE_API_KEY=your_api_key")
    print("3. Or create .env file with: GOOGLE_API_KEY=your_api_key")
    
    return False

def test_imports():
    """Test if all modules can be imported"""
    print("\n🧪 Testing imports...")
    
    modules = [
        "flask",
        "flask_socketio", 
        "requests",
        "game_state",
        "ai_integration",
        "ai_learning_system"
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    
    return True

def start_web_app():
    """Start the web application"""
    print("\n🚀 Starting web application...")
    print("📱 Web app will run at: http://localhost:5000")
    print("🌐 Open your browser and visit the URL above!")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        from web_app import app, socketio
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Error starting web app: {e}")
        return False
    
    return True

def main():
    """Main setup and run function"""
    print("🎮 Game AI Petualangan - Web Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check API key
    if not check_api_key():
        print("\n⚠️  Continuing without API key (some features may not work)")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return False
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Please check the errors above.")
        return False
    
    # Start web app
    return start_web_app()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Web app stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 
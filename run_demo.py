#!/usr/bin/env python3
"""
Demo Web Application untuk Game AI Petualangan
Tidak memerlukan API key - untuk testing koneksi
"""

import os
import sys
import subprocess

def install_flask():
    """Install Flask if not available"""
    try:
        import flask
        print("✅ Flask already installed")
        return True
    except ImportError:
        print("📦 Installing Flask...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            print("✅ Flask installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Flask")
            return False

def run_demo():
    """Run the demo web application"""
    print("🎮 Game AI Petualangan - Web Demo")
    print("=" * 40)
    print("📱 Web app will run at: http://localhost:5000")
    print("🌐 Open your browser and visit the URL above!")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    print("⚠️  This is DEMO mode - no AI integration")
    print("🎯 Perfect for testing web interface!")
    print("-" * 50)
    
    try:
        from web_app_demo import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ Error importing demo app: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running demo app: {e}")
        return False

def main():
    """Main function"""
    # Install Flask
    if not install_flask():
        return False
    
    # Run demo
    return run_demo()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo web app stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 
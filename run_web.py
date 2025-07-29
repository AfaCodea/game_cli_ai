#!/usr/bin/env python3
"""
Script untuk menjalankan Game AI Petualangan Web Edition
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is set
if not os.environ.get("GOOGLE_API_KEY"):
    print("❌ Error: GOOGLE_API_KEY tidak ditemukan!")
    print("📝 Silakan set API key di file .env:")
    print("   GOOGLE_API_KEY=your_api_key_here")
    sys.exit(1)

# Import and run web app
try:
    from web_app import app, socketio
    
    print("🚀 Starting Game AI Petualangan Web Edition...")
    print("📱 Web app akan berjalan di: http://localhost:5000")
    print("🌐 Buka browser dan kunjungi URL di atas untuk mulai bermain!")
    print("⏹️  Tekan Ctrl+C untuk menghentikan server")
    print("-" * 50)
    
    # Run the app
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("📦 Pastikan semua dependensi terinstall:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error running web app: {e}")
    sys.exit(1) 
# 📁 Project Structure - Game AI Petualangan

```
game_cli_ai/
├── 📄 main.py                    # CLI Entry point - Game versi terminal
├── 📄 run_web.py                 # Web Entry point - Game versi web
├── 📄 web_app.py                 # Flask Web Application - Backend web
├── 📄 game.py                    # Main game logic & UI (CLI) - Game controller
├── 📄 game_state.py              # Game state management - State & data
├── 📄 ai_integration.py          # AI integration & functions - Gemini AI
├── 📄 ai_learning_system.py      # AI Learning System - Auto-learning
├── 📄 requirements.txt           # Dependencies - Python packages
├── 📄 README.md                 # Documentation - Panduan lengkap
├── 📄 test_commands.py          # Test script - Testing CLI
├── 📄 test_web.py               # Test script - Testing Web
├── 📄 start_web.bat             # Windows batch - Jalankan web app
├── 📄 start_web.ps1             # PowerShell script - Jalankan web app
├── 📄 PROJECT_STRUCTURE.md      # This file - Struktur project
├── 📁 templates/                # Web Templates
│   └── 📄 index.html           # Main Web Interface - Frontend
├── 📄 game_learning_data.json   # AI Learning Data - Auto-generated
├── 📄 learned_patterns.pkl      # Learned Patterns - Auto-generated
└── 📄 .env                      # API key - Create this file
```

## 🎮 Versi Game

### **1. CLI Version (Terminal)**
- **File**: `main.py`
- **Command**: `python main.py`
- **Interface**: Rich terminal dengan warna dan panel
- **Platform**: Windows, Mac, Linux

### **2. Web Version (Browser)**
- **File**: `run_web.py` atau `start_web.bat`/`start_web.ps1`
- **Command**: `python run_web.py`
- **Interface**: Modern web UI dengan responsive design
- **URL**: http://localhost:5000
- **Platform**: Browser (cross-platform)

## 🔧 Core Components

### **Game Logic**
- **`game.py`**: Main game controller untuk CLI version
- **`game_state.py`**: Manajemen state game (lokasi, inventaris, quest)
- **`web_app.py`**: Flask backend untuk web version

### **AI Integration**
- **`ai_integration.py`**: Integrasi dengan Google Gemini AI
- **`ai_learning_system.py`**: Sistem pembelajaran AI otomatis

### **Data Classes**
- **`GameState`**: Centralized game state
- **`Location`**: Representasi lokasi dengan items & NPCs
- **`Item`**: Representasi item dengan properties
- **`Quest`**: Representasi quest dengan requirements & rewards
- **`PlayerAction`**: Data structure untuk aksi pemain
- **`GamePattern`**: Pattern yang dipelajari dari aksi pemain

## 🌐 Web Application Structure

### **Backend (Flask)**
```
web_app.py
├── Flask App Setup
├── Game Session Management
├── API Endpoints:
│   ├── / (index) - Main page
│   ├── /api/game/start - Start game
│   ├── /api/game/status - Get game status
│   ├── /api/game/command - Execute command
│   └── /api/game/save - Save game
└── Command Processing Logic
```

### **Frontend (HTML/CSS/JavaScript)**
```
templates/index.html
├── Modern UI Design
├── Responsive Layout
├── Real-time Chat Interface
├── Status Panels
├── Quick Commands
├── Inventory Display
├── Quest Display
└── Interactive Elements
```

## 🧠 AI Learning System

### **Data Collection**
- **`PlayerAction`**: Records setiap aksi pemain
- **Pattern Analysis**: Menganalisis pola perilaku
- **Learning Reports**: Generate laporan pembelajaran

### **Auto-Development**
- **Smart Suggestions**: Saran berdasarkan pola pemain
- **Content Generation**: Generate konten baru otomatis
- **Behavioral Analysis**: Analisis preferensi pemain

## 📊 Data Files

### **Auto-Generated**
- **`game_learning_data.json`**: Data pembelajaran AI
- **`learned_patterns.pkl`**: Pattern yang dipelajari
- **`game_learning_data_{session_id}.json`**: Session-specific data

### **Configuration**
- **`.env`**: API key configuration
- **`requirements.txt`**: Python dependencies

## 🚀 How to Run

### **CLI Version**
```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
echo GOOGLE_API_KEY=your_api_key > .env

# Run CLI game
python main.py
```

### **Web Version**
```bash
# Method 1: Direct Python
python run_web.py

# Method 2: Windows Batch
start_web.bat

# Method 3: PowerShell
.\start_web.ps1
```

## 🧪 Testing

### **CLI Testing**
```bash
python test_commands.py
```

### **Web Testing**
```bash
# Start web app first, then:
python test_web.py
```

## 📁 File Descriptions

| File | Purpose | Type |
|------|---------|------|
| `main.py` | CLI game entry point | Python |
| `run_web.py` | Web game entry point | Python |
| `web_app.py` | Flask web application | Python |
| `game.py` | Main game logic (CLI) | Python |
| `game_state.py` | Game state management | Python |
| `ai_integration.py` | AI integration | Python |
| `ai_learning_system.py` | AI learning system | Python |
| `requirements.txt` | Dependencies | Text |
| `README.md` | Documentation | Markdown |
| `test_commands.py` | CLI testing | Python |
| `test_web.py` | Web testing | Python |
| `start_web.bat` | Windows launcher | Batch |
| `start_web.ps1` | PowerShell launcher | PowerShell |
| `templates/index.html` | Web interface | HTML |
| `.env` | API configuration | Environment |

## 🔄 Development Workflow

1. **Setup**: Install dependencies, set API key
2. **Development**: Edit game logic, AI functions, or UI
3. **Testing**: Run test scripts for both CLI and Web
4. **Deployment**: Run appropriate launcher for desired version
5. **AI Learning**: Game automatically learns and improves

## 🎯 Key Features by File

### **Core Gameplay**
- `game.py` + `game_state.py`: All game mechanics
- `ai_integration.py`: Dynamic AI responses
- `ai_learning_system.py`: Auto-improvement

### **User Interface**
- `main.py`: Rich CLI interface
- `web_app.py` + `templates/index.html`: Modern web interface

### **Data Management**
- `game_state.py`: Game data structures
- `ai_learning_system.py`: Learning data persistence

### **Testing & Quality**
- `test_commands.py`: CLI functionality testing
- `test_web.py`: Web functionality testing

---

**🎮 Choose your adventure: CLI for classic terminal experience, or Web for modern browser interface!** 
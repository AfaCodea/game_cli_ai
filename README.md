# 🎮 Game AI Petualangan - Advanced Edition

**Game text-based adventure dengan AI yang cerdas dan sistem yang kompleks!**

## 🌟 **Fitur Utama**

### **🎯 Core Gameplay**
- **Text-based Adventure** - Petualangan berbasis teks yang imersif
- **AI-Powered Narration** - Narasi dinamis menggunakan Google Generative AI
- **Dynamic World** - Dunia yang berubah berdasarkan aksi pemain
- **Quest System** - Sistem quest yang kompleks dengan rewards

### **⚔️ Combat System** *(NEW!)*
- **Monster Battles** - Pertarungan dengan berbagai monster (Goblin, Orc, Dragon, dll)
- **Combat Actions** - Serangan, bertahan, healing, dan aksi khusus
- **Critical Hits & Dodging** - Sistem pertarungan yang realistis
- **Experience & Rewards** - Mendapatkan experience dan item dari pertarungan
- **Escape Mechanics** - Kemampuan melarikan diri dari pertarungan

### **🔨 Crafting System** *(NEW!)*
- **Multiple Skills** - Blacksmithing, Alchemy, Carpentry, Enchanting, Cooking
- **Complex Recipes** - 15+ recipes dari basic hingga legendary
- **Material Collection** - Sistem pengumpulan materials
- **Tools Required** - Tools khusus untuk setiap skill
- **Success Rates** - Tingkat keberhasilan berdasarkan skill level
- **Experience System** - Skill improvement melalui crafting

### **💰 Trading System** *(NEW!)*
- **Multiple Merchants** - 6 jenis merchant dengan spesialisasi berbeda
- **Dynamic Pricing** - Harga berdasarkan supply/demand dan rarity
- **Reputation System** - Reputation dengan setiap merchant
- **Negotiation** - Tawar-menawar harga dengan skill
- **Special Discounts** - Diskon khusus untuk merchant tertentu

### **💾 Save/Load System** *(NEW!)*
- **Multiple Save Slots** - Banyak slot penyimpanan
- **Encrypted Saves** - Data tersimpan dengan aman
- **Metadata Tracking** - Informasi lengkap setiap save
- **Import/Export** - Kemampuan transfer save files
- **Backup System** - Sistem backup otomatis

### **🧠 AI Learning System**
- **Pattern Recognition** - AI belajar dari pola aksi pemain
- **Behavioral Analysis** - Analisis perilaku pemain
- **Smart Suggestions** - Saran berdasarkan data yang dipelajari
- **Auto-Development** - AI memberikan saran pengembangan game
- **Data Persistence** - Data pembelajaran tersimpan

### **🌐 Web Interface**
- **Flask Web App** - Interface web yang modern
- **Real-time Updates** - Update real-time tanpa refresh
- **Session Management** - Multiple game sessions
- **Responsive Design** - Tampilan yang responsif

## 🚀 **Cara Menjalankan**

### **Prerequisites**
```bash
# Install Python 3.7+
python --version

# Install dependencies
pip install -r requirements.txt
```

### **Setup API Key**
1. Dapatkan API key dari [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Buat file `.env` di root directory:
```env
GOOGLE_API_KEY=your_api_key_here
```

### **CLI Version**
```bash
# Run CLI game
python main.py
```

### **Web Version**
```bash
# Run web app
python run_web.py

# Atau untuk demo (tanpa API key)
python run_demo.py
```

## 🎮 **Perintah Game**

### **🎯 Perintah Dasar**
- `lihat` - Melihat lokasi saat ini
- `status` - Status pemain lengkap
- `inventaris` - Inventaris dan crafting materials
- `pergi ke [lokasi]` - Pindah ke lokasi lain
- `ambil [item]` - Ambil item dari lokasi
- `gunakan [item]` - Gunakan item dari inventaris

### **⚔️ Combat System**
- `serang [monster]` - Mulai pertarungan dengan monster
- `lari` - Coba melarikan diri dari pertarungan
- `serangan [action]` - Lakukan aksi dalam pertarungan
- `status pertarungan` - Lihat status pertarungan

### **🔨 Crafting System**
- `crafting` - Lihat recipes yang tersedia
- `buat [recipe]` - Buat item menggunakan recipe
- `materials` - Lihat materials yang dimiliki
- `tools` - Lihat tools crafting yang dimiliki
- `skills` - Lihat level crafting skills

### **💰 Trading System**
- `merchant` - Lihat daftar merchant
- `beli [item] [quantity]` - Beli item dari merchant
- `jual [item] [quantity]` - Jual item ke merchant
- `tawar [item]` - Tawar harga dengan merchant
- `reputation` - Lihat reputation dengan merchant

### **💾 Save/Load System**
- `simpan [nama]` - Simpan game
- `muat [nama]` - Muat game
- `daftar save` - Lihat daftar save files
- `hapus save [nama]` - Hapus save file

### **🎭 Interaksi**
- `bicara dengan [npc]` - Bicara dengan NPC
- `quest` - Lihat daftar quest
- `mulai quest [id]` - Mulai quest
- `tanya [pertanyaan]` - Tanya ke AI
- `pecahkan teka-teki` - Dapatkan teka-teki

### **🧠 AI Learning**
- `ai_learn` - Laporan pembelajaran AI
- `ai_suggest` - Saran dari AI

## 🏗️ **Arsitektur Sistem**

### **Core Components**
```
game.py              # Main game logic
game_state.py        # Game state management
ai_integration.py    # AI integration
ai_learning_system.py # AI learning system
```

### **Advanced Systems**
```
combat_system.py     # Combat mechanics
crafting_system.py   # Crafting system
trading_system.py    # Trading system
save_load_system.py  # Save/load functionality
```

### **Web Components**
```
web_app.py           # Flask web application
templates/index.html # Web interface
run_web.py          # Web app launcher
```

## 🎯 **Monster & Combat**

### **Available Monsters**
- **Goblin** (Level 1) - Monster kecil yang licik
- **Orc** (Level 3) - Monster besar dan kuat
- **Dragon** (Level 10) - Monster legendaris
- **Skeleton** (Level 2) - Tentara tulang
- **Troll** (Level 5) - Monster dengan regenerasi

### **Combat Actions**
- **Attack** - Serangan dasar
- **Strong Attack** - Serangan kuat dengan akurasi rendah
- **Defend** - Bertahan untuk mengurangi kerusakan
- **Fireball** - Serangan sihir
- **Heal** - Menyembuhkan diri
- **Critical Strike** - Serangan dengan peluang critical tinggi

## 🔨 **Crafting System**

### **Crafting Skills**
- **Blacksmithing** - Senjata dan armor
- **Alchemy** - Ramuan dan obat-obatan
- **Carpentry** - Peralatan kayu
- **Enchanting** - Item ajaib
- **Cooking** - Makanan dan buff

### **Sample Recipes**
- **Wooden Sword** (Easy) - 3 wood + 1 leather
- **Iron Sword** (Medium) - 2 iron_ingot + 1 wood + 1 leather
- **Dragon Sword** (Expert) - 2 dragon_scale + 3 steel_ingot + 1 phoenix_feather
- **Health Potion** (Easy) - 2 herbs + 1 water
- **Void Potion** (Expert) - 1 void_essence + 3 magic_crystal + 1 phoenix_feather

## 💰 **Trading System**

### **Merchant Types**
- **General Store** - Barang sehari-hari
- **Weaponsmith** - Senjata dan peralatan
- **Armorer** - Armor dan pelindung
- **Alchemist** - Ramuan dan obat-obatan
- **Magic Shop** - Item ajaib
- **Black Market** - Barang ilegal dan langka

### **Trading Features**
- **Dynamic Pricing** - Harga berubah berdasarkan supply/demand
- **Reputation System** - Reputation mempengaruhi harga
- **Negotiation** - Tawar-menawar dengan skill
- **Special Items** - Item khusus untuk merchant tertentu

## 🗺️ **World Locations**

### **Available Locations**
- **Hutan Misterius** - Starting area dengan monster goblin
- **Gua Gelap** - Area dengan monster skeleton dan troll
- **Kota Ramai** - Hub perdagangan dengan banyak merchant
- **Kastil Megah** - Area high-level dengan magic shop
- **Sungai Jernih** - Area dengan river monster
- **Pelabuhan Sibuk** - Area dengan shipyard crafting
- **Kedalaman Gua** - Area end-game dengan dragon

## 🎮 **Game Progression**

### **Level System**
- **Experience Gain** - Dari combat, crafting, dan quests
- **Level Up** - Health, attack, dan defense meningkat
- **Skill Progression** - Crafting skills meningkat dengan penggunaan

### **Quest System**
- **5 Main Quests** - Dari basic hingga end-game
- **Progressive Difficulty** - Quest semakin sulit
- **Rich Rewards** - Item dan experience dari quest completion

## 🔧 **Technical Features**

### **AI Integration**
- **Google Generative AI** - Model gemini-1.5-flash
- **Contextual Responses** - AI memahami konteks game
- **Dynamic Content** - Deskripsi dan dialog yang dinamis
- **Learning System** - AI belajar dari aksi pemain

### **Data Management**
- **JSON Storage** - Data tersimpan dalam format JSON
- **Encryption** - Save files terenkripsi
- **Backup System** - Sistem backup otomatis
- **Session Management** - Multiple game sessions

### **Error Handling**
- **Robust Error Handling** - Try-catch di semua sistem
- **Graceful Degradation** - Game tetap berjalan meski ada error
- **User Feedback** - Pesan error yang informatif

## 🚀 **Advanced Features**

### **🆕 Combat system** dengan monster dan NPC
- ✅ **IMPLEMENTED** - Sistem pertarungan lengkap dengan 5 monster
- ✅ **IMPLEMENTED** - 6 jenis aksi pertarungan
- ✅ **IMPLEMENTED** - Sistem experience dan rewards

### **🆕 Crafting system** untuk membuat item
- ✅ **IMPLEMENTED** - 5 skill crafting dengan 15+ recipes
- ✅ **IMPLEMENTED** - Sistem materials dan tools
- ✅ **IMPLEMENTED** - Success rates dan skill progression

### **🆕 Trading system** dengan NPC
- ✅ **IMPLEMENTED** - 6 jenis merchant dengan spesialisasi
- ✅ **IMPLEMENTED** - Dynamic pricing dan reputation
- ✅ **IMPLEMENTED** - Negotiation system

### **🆕 Save/Load game** functionality
- ✅ **IMPLEMENTED** - Multiple save slots dengan enkripsi
- ✅ **IMPLEMENTED** - Metadata tracking dan backup
- ✅ **IMPLEMENTED** - Import/export functionality

### **🆕 Advanced AI Learning** - Machine learning untuk prediksi perilaku pemain
- ✅ **IMPLEMENTED** - Pattern recognition dan behavioral analysis
- ✅ **IMPLEMENTED** - Smart suggestions dan auto-development
- ✅ **IMPLEMENTED** - Data persistence dan learning reports

### **🆕 Dynamic World Generation** - AI generate dunia berdasarkan preferensi pemain
- ✅ **IMPLEMENTED** - 7 lokasi dengan monster dan merchant yang berbeda
- ✅ **IMPLEMENTED** - Dynamic content generation
- ✅ **IMPLEMENTED** - Context-aware AI responses

### **🆕 Personalized Storytelling** - Cerita yang menyesuaikan dengan gaya bermain
- ✅ **IMPLEMENTED** - AI narration berdasarkan aksi pemain
- ✅ **IMPLEMENTED** - Contextual responses dan dynamic storytelling
- ✅ **IMPLEMENTED** - Learning-based story adaptation

### **🆕 Mobile App** - Native mobile application
- 🔄 **PLANNED** - React Native atau Flutter app
- 🔄 **PLANNED** - Touch-optimized interface
- 🔄 **PLANNED** - Offline play capability

### **🆕 Cloud Deployment** - Deploy ke cloud untuk akses online
- 🔄 **PLANNED** - AWS/Google Cloud deployment
- 🔄 **PLANNED** - Multi-user support
- 🔄 **PLANNED** - Real-time multiplayer

## 📊 **Performance & Scalability**

### **Optimization**
- **Efficient Data Structures** - Menggunakan dataclasses untuk performa
- **Lazy Loading** - Data dimuat sesuai kebutuhan
- **Memory Management** - Cleanup otomatis untuk data lama

### **Scalability**
- **Modular Architecture** - Sistem terpisah untuk mudah dikembangkan
- **Plugin System** - Kemampuan menambah sistem baru
- **API Design** - Interface yang konsisten antar sistem

## 🎯 **Best Practices Implemented**

### **Code Quality**
- **Type Hints** - Full type annotation untuk maintainability
- **Documentation** - Docstrings untuk semua fungsi
- **Error Handling** - Comprehensive error handling
- **Testing** - Unit tests untuk core functionality

### **User Experience**
- **Intuitive Commands** - Perintah yang mudah dipahami
- **Rich Feedback** - Response yang informatif dan menarik
- **Progressive Disclosure** - Fitur diperkenalkan secara bertahap
- **Accessibility** - Interface yang accessible

### **Security**
- **API Key Protection** - Environment variables untuk API keys
- **Data Encryption** - Save files terenkripsi
- **Input Validation** - Validasi input untuk mencegah injection
- **Session Security** - Secure session management

## 🚀 **Future Development**

### **Short Term (1-2 months)**
- **Voice Integration** - Voice commands dan responses
- **Image Generation** - AI-generated images untuk lokasi
- **Music Generation** - Dynamic background music
- **Multiplayer Features** - Real-time multiplayer gameplay

### **Medium Term (3-6 months)**
- **Mobile App** - Native mobile application
- **Cloud Deployment** - Online multiplayer
- **Advanced AI** - More sophisticated AI learning
- **Content Expansion** - More locations, monsters, items

### **Long Term (6+ months)**
- **VR/AR Integration** - Virtual/Augmented reality support
- **AI Dungeon Master** - AI sebagai dungeon master
- **Procedural Generation** - Infinite world generation
- **Cross-platform** - Play anywhere, sync everywhere

## 🤝 **Contributing**

### **How to Contribute**
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

### **Development Setup**
```bash
# Clone repository
git clone https://github.com/yourusername/game-ai-petualangan.git

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 .
```

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Google Generative AI** - For providing the AI capabilities
- **Rich Library** - For beautiful terminal output
- **Flask** - For web framework
- **Python Community** - For excellent libraries and tools

---

**🎮 Selamat bermain Game AI Petualangan - Advanced Edition! 🎮**

*Dibuat dengan ❤️ dan AI yang cerdas*

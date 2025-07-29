# Game CLI AI Petualangan - Advanced Edition

Game petualangan berbasis teks yang terintegrasi dengan AI Gemini (Google Generative AI) untuk pengalaman interaktif dan narasi dinamis dengan fitur-fitur canggih.

## 🎮 Fitur Utama

### 🌍 **Dunia Dinamis**
- **7 lokasi berbeda** yang bisa dieksplorasi: Hutan Misterius, Gua Gelap, Kota Ramai, Kastil Megah, Sungai Jernih, Pelabuhan Sibuk, Kedalaman Gua
- **Sistem perpindahan lokasi** dengan koneksi antar area
- **Deskripsi lokasi yang dinamis** - berbeda saat kunjungan pertama vs kunjungan ulang

### 🎒 **Sistem Inventaris & Item**
- **Item yang bisa diambil** dari setiap lokasi
- **Item yang bisa digunakan** dengan efek yang berbeda
- **Item consumable** yang habis setelah digunakan
- **Sistem berat dan nilai** untuk setiap item

### 📋 **Sistem Quest**
- **3 quest berbeda** dengan requirements dan rewards
- **Progress tracking** real-time
- **Quest completion** otomatis dengan reward
- **Quest status** (Tersedia/Aktif/Selesai)

### 🤖 **AI Cerdas dengan Memory**
- **Context-aware responses** berdasarkan lokasi, inventaris, dan state game
- **Conversation history** - AI mengingat percakapan sebelumnya
- **Player action tracking** - AI tahu aksi pemain terakhir
- **Dynamic storytelling** - cerita berubah berdasarkan pilihan pemain

### 🎯 **Perintah Lengkap**
- **Perintah khusus**: lihat, status, inventaris, pergi ke, ambil, gunakan, bicara dengan, quest, mulai quest, pecahkan teka-teki, tanya, help, keluar
- **Perintah bebas**: ketik apapun, AI akan merespons sebagai narasi petualangan
- **Natural language processing** - AI memahami perintah dalam bahasa natural

### 🎨 **UI/UX Canggih**
- **Rich CLI interface** dengan warna, panel, dan tabel
- **Status bar** menampilkan health, level, experience, gold
- **Progress tracking** untuk quest
- **Beautiful tables** untuk inventaris dan quest

## 🚀 Instalasi

1. **Clone repository** (jika belum):
   ```bash
   git clone <repo-anda>
   cd game_cli_ai
   ```

2. **Install dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Siapkan API Key Google Gemini**
   - Dapatkan API key dari [Google AI Studio](https://aistudio.google.com/app/apikey) atau Google Cloud Console.

4. **Buat file `.env` di folder project**
   Isi dengan:
   ```env
   GOOGLE_API_KEY=ISI_API_KEY_ANDA
   ```
   Ganti `ISI_API_KEY_ANDA` dengan API key Anda.

## 🎮 Menjalankan Game

Jalankan di terminal:
```bash
python main.py
```

## 🎯 Cara Bermain

### **Perintah Dasar**
- `lihat` - Melihat deskripsi lokasi saat ini
- `status` - Melihat status pemain (health, level, gold)
- `inventaris` - Melihat inventaris dengan detail
- `help` - Menampilkan bantuan lengkap

### **Eksplorasi Dunia**
- `pergi ke [lokasi]` - Pindah ke lokasi lain (contoh: `pergi ke gua`)
- `ambil [item]` - Mengambil item dari lokasi (contoh: `ambil ranting`)
- `gunakan [item]` - Menggunakan item dari inventaris (contoh: `gunakan ranting`)

### **Interaksi NPC**
- `bicara dengan [npc]` - Bicara dengan NPC di lokasi (contoh: `bicara dengan penjaga_hutan`)

### **Sistem Quest**
- `quest` - Melihat daftar quest dan progress
- `mulai quest [id]` - Memulai quest tertentu (contoh: `mulai quest quest_1`)

### **AI Interaction**
- `tanya [pertanyaan]` - Bertanya bebas ke AI (contoh: `tanya siapa penemu komputer?`)
- `pecahkan teka-teki` - Mendapatkan teka-teki dari AI
- **Perintah bebas** - Ketik apapun, AI akan merespons sebagai narasi petualangan

### **Contoh Perintah Bebas**
- `panjat pohon`
- `nyalakan api unggun`
- `cari harta karun`
- `tidur di bawah bintang`
- `berenang di sungai`
- `makan ikan segar`
- `buka peti harta`
- `lompat ke sungai`
- `cari jalan keluar`
- `berdoa di kuil`

## 🗺️ Peta Dunia

```
Hutan Misterius
├── Gua Gelap
│   └── Kedalaman Gua
├── Kota Ramai
│   ├── Kastil Megah
│   └── Pelabuhan Sibuk
└── Sungai Jernih
    └── Pelabuhan Sibuk
```

## 📋 Daftar Quest

1. **Quest 1: Mengumpulkan Kayu**
   - ID: `quest_1`
   - Tugas: Kumpulkan 3 ranting
   - Reward: Api unggun

2. **Quest 2: Mencari Batu Api**
   - ID: `quest_2`
   - Tugas: Temukan 1 batu api
   - Reward: Korek api

3. **Quest 3: Mengumpulkan Harta**
   - ID: `quest_3`
   - Tugas: Kumpulkan 100 koin emas
   - Reward: Pedang kerajaan

## 🛠️ Error Umum & Solusi

### Import "google.generativeai" could not be resolved
**Solusi:**
```bash
pip install google-generativeai
```

### "load_dotenv" is not defined
**Solusi:**
```bash
pip install python-dotenv
```

### No API_KEY or ADC found
**Solusi:**
- Pastikan file `.env` sudah ada dan berisi baris:
  ```env
  GOOGLE_API_KEY=ISI_API_KEY_ANDA
  ```
- Atau, set environment variable secara manual:
  ```powershell
  $env:GOOGLE_API_KEY="ISI_API_KEY_ANDA"
  python main.py
  ```

## 🏗️ Arsitektur Kode

### **File Structure**
```
game_cli_ai/
├── main.py              # Entry point
├── game.py              # Main game logic & UI
├── game_state.py        # Game state management
├── ai_integration.py    # AI integration & functions
├── requirements.txt     # Dependencies
├── README.md           # Documentation
└── .env                # API key (create this)
```

### **Classes**
- **GameState**: Mengelola state game (lokasi, inventaris, quest, memory)
- **Location**: Representasi lokasi dengan items dan NPCs
- **Item**: Representasi item dengan properties
- **Quest**: Representasi quest dengan requirements dan rewards
- **Game**: Main game controller dengan UI

## 🎯 Best Practices Implemented

1. **Separation of Concerns** - Logika game, AI, dan UI terpisah
2. **State Management** - Centralized state dengan GameState class
3. **Error Handling** - Comprehensive error handling untuk AI calls
4. **Memory Management** - AI memory untuk conversation dan action history
5. **Extensibility** - Mudah menambah lokasi, item, quest, dan fitur baru
6. **User Experience** - Rich UI dengan feedback yang jelas
7. **Documentation** - Comprehensive documentation dan help system

## 🚀 Pengembangan Lebih Lanjut

Game ini bisa dikembangkan lebih lanjut dengan:
- **Combat system** dengan monster dan NPC
- **Crafting system** untuk membuat item
- **Trading system** dengan NPC
- **Save/Load game** functionality
- **Multiplayer features**
- **Voice interaction**
- **Image generation** untuk lokasi
- **Music generation** untuk mood

## 📄 Lisensi
Bebas digunakan untuk pembelajaran dan pengembangan.

---

**Selamat bermain dan eksplorasi dunia petualangan yang tak terbatas!** 🎮✨

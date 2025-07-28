# Game CLI AI Petualangan

Game petualangan berbasis teks yang terintegrasi dengan AI Gemini (Google Generative AI) untuk pengalaman interaktif dan narasi dinamis.

## Fitur
- Perintah bebas: ketik perintah apapun, AI akan merespons sebagai narasi petualangan.
- Perintah khusus: lihat, inventaris, bicara dengan [npc], pecahkan teka-teki, tanya [pertanyaan], help, keluar.
- Tampilan CLI menarik dengan [rich](https://github.com/Textualize/rich).

## Instalasi

1. **Clone repository** (jika belum):
   ```bash
   git clone <repo-anda>
   cd game_cli_ai
   ```

2. **Install dependensi**:
   ```bash
   pip install -r requirements.txt
   ```
   Jika belum ada `requirements.txt`, install manual:
   ```bash
   pip install google-generativeai rich python-dotenv
   ```

3. **Siapkan API Key Google Gemini**
   - Dapatkan API key dari [Google AI Studio](https://aistudio.google.com/app/apikey) atau Google Cloud Console.

4. **Buat file `.env` di folder project**
   Isi dengan:
   ```env
   GOOGLE_API_KEY=ISI_API_KEY_ANDA
   ```
   Ganti `ISI_API_KEY_ANDA` dengan API key Anda.

## Menjalankan Game

Jalankan di terminal:
```bash
python main.py
```

## Cara Bermain
- Ketik perintah apapun, misal:
  - `lihat`
  - `inventaris`
  - `bicara dengan penjaga`
  - `pecahkan teka-teki`
  - `tanya siapa penemu komputer?`
  - `pergi ke gua`
  - `ambil pedang`
  - `buka pintu`
  - dan lain-lain
- Ketik `help` untuk melihat daftar perintah.
- Ketik `keluar` untuk keluar dari game.

## Error Umum & Solusi

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
Pastikan juga sudah ada baris berikut di kode:
```python
from dotenv import load_dotenv
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

## Lisensi
Bebas digunakan untuk pembelajaran dan pengembangan.

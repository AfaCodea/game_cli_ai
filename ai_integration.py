import google.generativeai as genai
import os
from dotenv import load_dotenv

# Konfigurasi API Key dari environment variable (WAJIB SET GOOGLE_API_KEY di environment)
load_dotenv()  # otomatis membaca file .env
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

def generate_description(prompt_text):
    """
    Menghasilkan deskripsi teks menggunakan model Gemini.
    """
    try:
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        print(f"Error generating content from AI: {e}")
        return "Tidak dapat menghasilkan deskripsi saat ini."

def generate_puzzle(context):
    """
    Menghasilkan teka-teki berdasarkan konteks yang diberikan.
    """
    prompt = f"Buat teka-teki singkat dan jawabannya berdasarkan konteks ini: {context}\n\nTeka-teki:"
    return generate_description(prompt)

def generate_npc_dialogue(character_name, situation):
    """
    Menghasilkan dialog untuk NPC.
    """
    prompt = f"Buat dialog singkat untuk karakter bernama {character_name} dalam situasi: {situation}. Dialog harus terdengar seperti dia sedang memberikan petunjuk."
    return generate_description(prompt)

# Contoh penggunaan (bisa dihapus setelah pengujian)
if __name__ == "__main__":
    print("Mencoba menghasilkan deskripsi lokasi...")
    desc = generate_description("Deskripsikan sebuah gua gelap dan misterius dengan aliran air di dalamnya.")
    print(desc)

    print("\nMencoba menghasilkan teka-teki...")
    puzzle = generate_puzzle("sebuah perpustakaan kuno yang penuh buku debu")
    print(puzzle)
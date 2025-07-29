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

def generate_contextual_response(command, game_context, conversation_history=None, player_actions=None):
    """
    Menghasilkan respons kontekstual berdasarkan perintah pemain dan state game.
    """
    context_prompt = f"""
    Kamu adalah engine game petualangan berbasis teks yang cerdas.
    
    KONTEKS GAME:
    {game_context}
    
    RIWAYAT PERCAKAPAN TERAKHIR:
    {conversation_history[-3:] if conversation_history else 'Belum ada percakapan'}
    
    AKSI PEMAIN TERAKHIR:
    {player_actions[-3:] if player_actions else 'Belum ada aksi'}
    
    PERINTAH PEMAIN: {command}
    
    TUGAS:
    1. Jika perintah adalah aksi game (seperti 'pergi ke', 'ambil', 'gunakan', 'bicara dengan', dll), 
       berikan narasi yang sesuai dengan aksi tersebut dan konsekuensinya.
    2. Jika perintah adalah pertanyaan umum, jawablah dengan informatif.
    3. Gunakan konteks lokasi, inventaris, dan state game untuk memberikan respons yang relevan.
    4. Berikan respons yang menarik dan mendorong eksplorasi lebih lanjut.
    5. Jika pemain melakukan aksi yang tidak mungkin atau berbahaya, berikan peringatan yang masuk akal.
    
    JAWABAN (dalam format narasi game):
    """
    
    return generate_description(context_prompt)

def generate_quest_description(quest, progress=None):
    """
    Menghasilkan deskripsi quest yang dinamis berdasarkan progress.
    """
    if progress:
        progress_text = "\n".join([f"- {item}: {data['current']}/{data['required']}" for item, data in progress.items()])
        prompt = f"""
        Quest: {quest.title}
        Deskripsi: {quest.description}
        Progress saat ini:
        {progress_text}
        
        Berikan motivasi dan petunjuk untuk menyelesaikan quest ini.
        """
    else:
        prompt = f"""
        Quest: {quest.title}
        Deskripsi: {quest.description}
        
        Berikan penjelasan menarik tentang quest ini dan mengapa pemain harus melakukannya.
        """
    
    return generate_description(prompt)

def generate_location_description(location_name, location_info, visited=False):
    """
    Menghasilkan deskripsi lokasi yang dinamis.
    """
    if visited:
        prompt = f"""
        Lokasi: {location_name}
        Deskripsi: {location_info.description}
        
        Pemain sudah pernah mengunjungi tempat ini. Berikan deskripsi yang berbeda, 
        mungkin ada detail baru yang terlihat atau perubahan yang terjadi.
        """
    else:
        prompt = f"""
        Lokasi: {location_name}
        Deskripsi: {location_info.description}
        
        Ini adalah kunjungan pertama pemain ke tempat ini. Berikan deskripsi yang 
        menarik dan mendorong eksplorasi lebih lanjut.
        """
    
    return generate_description(prompt)

def generate_combat_narration(action, enemy_name="monster", player_health=100, enemy_health=100):
    """
    Menghasilkan narasi pertarungan.
    """
    prompt = f"""
    Pertarungan melawan {enemy_name}!
    
    Aksi pemain: {action}
    Health pemain: {player_health}
    Health musuh: {enemy_health}
    
    Berikan narasi pertarungan yang menarik dan epik berdasarkan aksi pemain.
    """
    
    return generate_description(prompt)

# Contoh penggunaan (bisa dihapus setelah pengujian)
if __name__ == "__main__":
    print("Mencoba menghasilkan deskripsi lokasi...")
    desc = generate_description("Deskripsikan sebuah gua gelap dan misterius dengan aliran air di dalamnya.")
    print(desc)

    print("\nMencoba menghasilkan teka-teki...")
    puzzle = generate_puzzle("sebuah perpustakaan kuno yang penuh buku debu")
    print(puzzle)
from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-secret-key'

# Demo game state
demo_game_state = {
    'player_name': 'Pahlawan Demo',
    'health': 100,
    'max_health': 100,
    'level': 1,
    'experience': 0,
    'gold': 50,
    'current_location': {
        'name': 'Hutan Misterius',
        'description': 'Hutan yang penuh dengan misteri dan petualangan. Pepohonan tinggi menjulang dan suara burung terdengar dari kejauhan.',
        'items': [{'name': 'Ranting', 'description': 'Ranting kayu yang bisa digunakan untuk berbagai keperluan'}],
        'npcs': ['Penjaga Hutan']
    },
    'inventory': [],
    'available_locations': ['hutan', 'gua', 'kota', 'kastil', 'sungai', 'pelabuhan'],
    'quests': [
        {
            'id': 'quest_1',
            'title': 'Mengumpulkan Kayu',
            'description': 'Kumpulkan 3 ranting untuk membuat api unggun',
            'started': False,
            'completed': False
        }
    ]
}

@app.route('/')
def index():
    """Main game page"""
    return render_template('index.html')

@app.route('/api/game/start', methods=['POST'])
def start_game():
    """Start new game session"""
    session_id = request.json.get('session_id', str(datetime.now().timestamp()))
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': f"Selamat datang, {demo_game_state['player_name']}, di dunia petualangan demo!"
    })

@app.route('/api/game/status', methods=['GET'])
def get_game_status():
    """Get current game status"""
    return jsonify(demo_game_state)

@app.route('/api/game/command', methods=['POST'])
def execute_command():
    """Execute game command"""
    command = request.json.get('command', '').strip()
    
    if not command:
        return jsonify({'error': 'Command is required'}), 400
    
    # Demo responses
    demo_responses = {
        'lihat': '**Hutan Misterius**\n\nHutan yang penuh dengan misteri dan petualangan. Pepohonan tinggi menjulang dan suara burung terdengar dari kejauhan.\n\n**Item yang terlihat:** Ranting\n\n**NPC yang terlihat:** Penjaga Hutan',
        'status': '**Status Pemain:**\n- Nama: Pahlawan Demo\n- Health: 100/100\n- Level: 1\n- Experience: 0\n- Gold: 50\n- Lokasi: Hutan Misterius',
        'inventaris': 'Inventaris Anda kosong.',
        'help': '**Perintah yang bisa digunakan:**\n\n**Dasar:**\n- `lihat` - Melihat deskripsi lokasi saat ini\n- `status` - Melihat status pemain\n- `inventaris` - Melihat inventaris Anda\n- `help` - Menampilkan bantuan ini\n\n**Eksplorasi:**\n- `pergi ke [lokasi]` - Pindah ke lokasi lain\n- `ambil [item]` - Mengambil item dari lokasi\n- `gunakan [item]` - Menggunakan item dari inventaris\n\n**Interaksi:**\n- `bicara dengan [npc]` - Bicara dengan NPC tertentu\n- `quest` - Melihat daftar quest\n- `mulai quest [id]` - Memulai quest tertentu\n\n**AI:**\n- `tanya [pertanyaan]` - Bertanya bebas ke AI\n- `pecahkan teka-teki` - Mendapatkan teka-teki dari AI\n- `ai_learn` - Melihat laporan pembelajaran AI\n- `ai_suggest` - Minta saran dari AI\n\n**Perintah bebas:** Ketik apapun dan AI akan merespons sebagai narasi petualangan!',
        'quest': '**Daftar Quest:**\n\n- **Mengumpulkan Kayu** (quest_1) - 📋 Tersedia\n  Kumpulkan 3 ranting untuk membuat api unggun\n\n',
        'ai_learn': '**AI Learning Report (Demo Mode):**\n\n📊 STATISTICS:\n- Total Actions: 0\n- Patterns Discovered: 0\n- Learning Sessions: 0\n\n🎯 MOST POPULAR:\n- Commands: belum ada data\n- Locations: belum ada data\n- Items: belum ada data\n- NPCs: belum ada data\n\n💡 SUGGESTED FEATURES:\n- exploration_system, interaction_improvements, quest_expansion\n\n🎮 PLAYER BEHAVIOR:\n- Belum ada data yang cukup untuk analisis\n\n🚀 AUTO-GENERATED CONTENT:\n- new_locations: Hutan Dalam, Gua Kristal\n- new_items: Pedang Legendaris, Mantel Pelindung\n- new_npcs: Master Petualang, Penjaga Harta\n- game_improvements: Save/Load system, Achievement system',
        'ai_suggest': '**AI Suggestions (Demo Mode):**\n\n💡 Coba perintah "lihat" untuk melihat lokasi saat ini\n💡 Gunakan "status" untuk melihat status pemain Anda\n💡 Ketik "help" untuk melihat semua perintah yang tersedia\n💡 Coba "quest" untuk melihat quest yang tersedia\n💡 Eksplorasi dengan "pergi ke [lokasi]" untuk menemukan tempat baru\n💡 Interaksi dengan NPC menggunakan "bicara dengan [npc]"\n💡 Ambil item dengan "ambil [item]" untuk menambah inventaris\n💡 Bertanya bebas dengan "tanya [pertanyaan]" untuk mendapatkan jawaban dari AI'
    }
    
    cmd = command.lower()
    
    if cmd in demo_responses:
        result = demo_responses[cmd]
    elif cmd.startswith('pergi ke'):
        location = command.split(' ', 2)[2] if len(command.split(' ', 2)) >= 3 else ''
        if location in demo_game_state['available_locations']:
            result = f"Anda pindah ke **{location.title()}**\n\nLokasi baru yang menarik untuk dieksplorasi!"
        else:
            result = f"Tidak bisa pergi ke '{location}'. Lokasi yang tersedia: {', '.join(demo_game_state['available_locations'])}"
    elif cmd.startswith('ambil'):
        item_name = command.split(' ', 1)[1] if len(command.split(' ', 1)) >= 2 else ''
        if item_name.lower() == 'ranting':
            result = f"Anda mengambil **Ranting**: Ranting kayu yang bisa digunakan untuk berbagai keperluan"
        else:
            result = f"Item '{item_name}' tidak ditemukan di lokasi ini."
    elif cmd.startswith('bicara dengan'):
        npc = command.split(' ', 2)[2] if len(command.split(' ', 2)) >= 3 else ''
        if npc.lower() == 'penjaga hutan':
            result = "**Penjaga Hutan berkata:**\n\n\"Selamat datang di hutan kami, petualang! Berhati-hatilah dengan bahaya yang mengintai di balik pepohonan.\""
        else:
            result = f"NPC '{npc}' tidak ada di lokasi ini. NPC yang tersedia: Penjaga Hutan"
    else:
        # Default response for unknown commands
        result = f"**Narasi Petualangan:**\n\nAnda mencoba '{command}' dan sesuatu yang menarik terjadi! Dalam dunia petualangan ini, setiap aksi membawa cerita baru."
    
    return jsonify({
        'success': True,
        'result': result,
        'game_status': demo_game_state
    })

@app.route('/api/game/save', methods=['POST'])
def save_game():
    """Save game data"""
    return jsonify({'success': True, 'message': 'Game saved successfully (demo mode)'})

if __name__ == '__main__':
    print("🎮 Game AI Petualangan - Web Demo")
    print("=" * 40)
    print("📱 Web app will run at: http://localhost:5000")
    print("🌐 Open your browser and visit the URL above!")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    print("⚠️  This is DEMO mode - no AI integration")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 
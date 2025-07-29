from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import json
import os
from datetime import datetime
from game_state import GameState
from ai_integration import generate_description, generate_puzzle, generate_npc_dialogue, generate_contextual_response, generate_quest_description, generate_location_description
from ai_learning_system import AILearningSystem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global game instances (in production, use database)
game_instances = {}

def get_or_create_game(session_id):
    """Get or create game instance for session"""
    if session_id not in game_instances:
        game_instances[session_id] = {
            'state': GameState(),
            'ai_learning': AILearningSystem(f"game_learning_data_{session_id}.json", f"learned_patterns_{session_id}.pkl")
        }
    return game_instances[session_id]

@app.route('/')
def index():
    """Main game page"""
    return render_template('index.html')

@app.route('/api/game/start', methods=['POST'])
def start_game():
    """Start new game session"""
    session_id = request.json.get('session_id', str(datetime.now().timestamp()))
    game_data = get_or_create_game(session_id)
    
    # Reset game state
    game_data['state'] = GameState()
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': f"Selamat datang, {game_data['state'].player_name}, di dunia petualangan!"
    })

@app.route('/api/game/status', methods=['GET'])
def get_game_status():
    """Get current game status"""
    session_id = request.args.get('session_id')
    if not session_id or session_id not in game_instances:
        return jsonify({'error': 'Game session not found'}), 404
    
    game_data = game_instances[session_id]
    state = game_data['state']
    current_loc = state.get_current_location_info()
    
    return jsonify({
        'player_name': state.player_name,
        'health': state.health,
        'max_health': state.max_health,
        'level': state.level,
        'experience': state.experience,
        'gold': state.gold,
        'current_location': {
            'name': current_loc.name,
            'description': current_loc.description,
            'items': [{'name': item.name, 'description': item.description} for item in current_loc.items],
            'npcs': current_loc.npcs
        },
        'inventory': [{'name': item.name, 'description': item.description, 'weight': item.weight, 'value': item.value} for item in state.inventory],
        'available_locations': state.get_available_locations(),
        'quests': [{
            'id': quest.quest_id,
            'title': quest.title,
            'description': quest.description,
            'started': quest.started,
            'completed': quest.completed
        } for quest in state.quests]
    })

@app.route('/api/game/command', methods=['POST'])
def execute_command():
    """Execute game command"""
    session_id = request.json.get('session_id')
    command = request.json.get('command', '').strip()
    
    if not session_id or session_id not in game_instances:
        return jsonify({'error': 'Game session not found'}), 404
    
    if not command:
        return jsonify({'error': 'Command is required'}), 400
    
    game_data = game_instances[session_id]
    state = game_data['state']
    ai_learning = game_data['ai_learning']
    
    try:
        # Process command
        result = process_command(command, state, ai_learning)
        
        # Get updated game status directly from state
        current_loc = state.get_current_location_info()
        game_status = {
            'player_name': state.player_name,
            'health': state.health,
            'max_health': state.max_health,
            'level': state.level,
            'experience': state.experience,
            'gold': state.gold,
            'current_location': {
                'name': current_loc.name,
                'description': current_loc.description,
                'items': [{'name': item.name, 'description': item.description} for item in current_loc.items],
                'npcs': current_loc.npcs
            },
            'inventory': [{'name': item.name, 'description': item.description, 'weight': item.weight, 'value': item.value} for item in state.inventory],
            'available_locations': state.get_available_locations(),
            'quests': [{
                'id': quest.quest_id,
                'title': quest.title,
                'description': quest.description,
                'started': quest.started,
                'completed': quest.completed
            } for quest in state.quests]
        }
        
        return jsonify({
            'success': True,
            'result': result,
            'game_status': game_status
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def process_command(command, state, ai_learning):
    """Process game command and return result"""
    cmd = command.lower()
    success = True
    response_type = "success"
    response_text = ""
    
    # Add action to history
    state.add_action(command)
    
    if cmd == "keluar":
        response_text = "Anda meninggalkan petualangan. Sampai jumpa!"
        response_type = "exit"
    
    elif cmd == "lihat":
        current_loc = state.get_current_location_info()
        description = generate_location_description(
            state.current_location, 
            current_loc, 
            current_loc.visited
        )
        response_text = f"**{current_loc.name}**\n\n{description}"
        
        if current_loc.items:
            items_text = ", ".join([item.name for item in current_loc.items])
            response_text += f"\n\n**Item yang terlihat:** {items_text}"
        
        if current_loc.npcs:
            npcs_text = ", ".join(current_loc.npcs)
            response_text += f"\n\n**NPC yang terlihat:** {npcs_text}"
    
    elif cmd == "status":
        response_text = f"""
**Status Pemain:**
- Nama: {state.player_name}
- Health: {state.health}/{state.max_health}
- Level: {state.level}
- Experience: {state.experience}
- Gold: {state.gold}
- Lokasi: {state.get_current_location_info().name}
        """
    
    elif cmd == "inventaris":
        if state.inventory:
            response_text = "**Inventaris Anda:**\n"
            for item in state.inventory:
                response_text += f"- {item.name}: {item.description} (Berat: {item.weight}, Nilai: {item.value})\n"
        else:
            response_text = "Inventaris Anda kosong."
    
    elif cmd.startswith("pergi ke"):
        parts = command.split(" ", 2)
        if len(parts) >= 3:
            location = parts[2].strip()
            if state.move_to(location):
                response_text = f"Anda pindah ke **{state.get_current_location_info().name}**"
                # Auto-show location description
                current_loc = state.get_current_location_info()
                description = generate_location_description(
                    state.current_location, 
                    current_loc, 
                    current_loc.visited
                )
                response_text += f"\n\n{description}"
            else:
                available = ", ".join(state.get_available_locations())
                response_text = f"Tidak bisa pergi ke '{location}'. Lokasi yang tersedia: {available}"
                success = False
                response_type = "error"
        else:
            response_text = "Format: pergi ke [nama_lokasi]"
            success = False
            response_type = "error"
    
    elif cmd.startswith("ambil"):
        parts = command.split(" ", 1)
        if len(parts) >= 2:
            item_name = parts[1].strip()
            current_loc = state.get_current_location_info()
            
            for item in current_loc.items:
                if item.name.lower() == item_name.lower():
                    state.add_item_to_inventory(item)
                    current_loc.items.remove(item)
                    response_text = f"Anda mengambil **{item.name}**: {item.description}"
                    return response_text
            
            response_text = f"Item '{item_name}' tidak ditemukan di lokasi ini."
            success = False
            response_type = "error"
        else:
            response_text = "Format: ambil [nama_item]"
            success = False
            response_type = "error"
    
    elif cmd.startswith("gunakan"):
        parts = command.split(" ", 1)
        if len(parts) >= 2:
            item_name = parts[1].strip()
            item = state.get_inventory_item(item_name)
            
            if item:
                if item.usable:
                    if item.consumable:
                        state.remove_item_from_inventory(item_name)
                    
                    prompt = f"Pemain menggunakan {item.name} di {state.get_current_location_info().name}. Berikan narasi yang menarik tentang apa yang terjadi."
                    result = generate_description(prompt)
                    response_text = f"**Menggunakan {item.name}:**\n\n{result}"
                else:
                    response_text = f"Item '{item_name}' tidak bisa digunakan."
                    success = False
                    response_type = "error"
            else:
                response_text = f"Item '{item_name}' tidak ada di inventaris."
                success = False
                response_type = "error"
        else:
            response_text = "Format: gunakan [nama_item]"
            success = False
            response_type = "error"
    
    elif cmd.startswith("bicara dengan"):
        parts = command.split(" ", 2)
        if len(parts) >= 3:
            npc = parts[2].strip()
            current_loc = state.get_current_location_info()
            
            if npc in current_loc.npcs:
                dialog = generate_npc_dialogue(npc, f"dia sedang berada di {current_loc.name}")
                response_text = f"**{npc.capitalize()} berkata:**\n\n\"{dialog}\""
            else:
                available_npcs = ", ".join(current_loc.npcs) if current_loc.npcs else "tidak ada"
                response_text = f"NPC '{npc}' tidak ada di lokasi ini. NPC yang tersedia: {available_npcs}"
                success = False
                response_type = "error"
        else:
            response_text = "Format: bicara dengan [nama_npc]"
            success = False
            response_type = "error"
    
    elif cmd == "quest":
        response_text = "**Daftar Quest:**\n"
        for quest in state.quests:
            status = "✅ Selesai" if quest.completed else "🔄 Aktif" if quest.started else "📋 Tersedia"
            response_text += f"- **{quest.title}** ({quest.quest_id}) - {status}\n  {quest.description}\n\n"
    
    elif cmd.startswith("mulai quest"):
        parts = command.split(" ", 2)
        if len(parts) >= 3:
            quest_id = parts[2].strip()
            if state.start_quest(quest_id):
                quest = next((q for q in state.quests if q.quest_id == quest_id), None)
                if quest:
                    description = generate_quest_description(quest)
                    response_text = f"**Quest Dimulai:**\n\n{description}"
            else:
                available_quests = ", ".join([q.quest_id for q in state.quests])
                response_text = f"Quest '{quest_id}' tidak ditemukan atau sudah dimulai. Quest yang tersedia: {available_quests}"
                success = False
                response_type = "error"
        else:
            response_text = "Format: mulai quest [quest_id]"
            success = False
            response_type = "error"
    
    elif cmd == "pecahkan teka-teki":
        puzzle_text = generate_puzzle(f"tentang {state.get_current_location_info().name} dan misterinya")
        response_text = f"**Teka-teki dari misteri {state.get_current_location_info().name}:**\n\n{puzzle_text}"
    
    elif cmd.startswith("tanya"):
        question = command[5:].strip()
        if not question:
            response_text = "Format: tanya [pertanyaan]"
            success = False
            response_type = "error"
        else:
            ai_answer = generate_description(question)
            response_text = f"**Pertanyaan:** {question}\n\n**AI menjawab:**\n{ai_answer}"
    
    elif cmd == "ai_learn":
        report = ai_learning.get_learning_report()
        response_text = f"**AI Learning Report:**\n\n{report}"
    
    elif cmd == "ai_suggest":
        current_context = {
            'location': state.current_location,
            'inventory': [item.name for item in state.inventory],
            'npcs': state.get_current_location_info().npcs,
            'health': state.health,
            'level': state.level,
            'available_locations': state.get_available_locations()
        }
        
        suggestions = ai_learning.generate_ai_suggestions(current_context)
        if suggestions:
            response_text = "**AI Suggestions:**\n\n" + "\n".join([f"💡 {suggestion}" for suggestion in suggestions])
        else:
            response_text = "AI belum memiliki cukup data untuk memberikan saran. Terus bermain untuk mendapatkan saran yang lebih baik!"
    
    elif cmd == "help":
        response_text = """
**Perintah yang bisa digunakan:**

**Dasar:**
- `lihat` - Melihat deskripsi lokasi saat ini
- `status` - Melihat status pemain
- `inventaris` - Melihat inventaris Anda
- `help` - Menampilkan bantuan ini

**Eksplorasi:**
- `pergi ke [lokasi]` - Pindah ke lokasi lain
- `ambil [item]` - Mengambil item dari lokasi
- `gunakan [item]` - Menggunakan item dari inventaris

**Interaksi:**
- `bicara dengan [npc]` - Bicara dengan NPC tertentu
- `quest` - Melihat daftar quest
- `mulai quest [id]` - Memulai quest tertentu

**AI:**
- `tanya [pertanyaan]` - Bertanya bebas ke AI
- `pecahkan teka-teki` - Mendapatkan teka-teki dari AI
- `ai_learn` - Melihat laporan pembelajaran AI
- `ai_suggest` - Minta saran dari AI

**Perintah bebas:** Ketik apapun dan AI akan merespons sebagai narasi petualangan!
        """
    
    else:
        # Perintah bebas: kirim ke AI sebagai narasi petualangan dengan context
        game_context = state.get_context_for_ai()
        ai_narration = generate_contextual_response(
            command, 
            game_context, 
            state.conversation_history, 
            state.player_actions
        )
        response_text = f"**Narasi Petualangan:**\n\n{ai_narration}"
        response_type = "ai_response"
        
        # Add to conversation history
        state.add_conversation(f"Player: {command} | AI: {ai_narration[:100]}...")
        
        # Check quest completion after any action
        completed_quest = state.check_quest_completion()
        if completed_quest:
            quest_complete_text = f"🎉 Quest '{completed_quest.title}' selesai! Anda mendapatkan reward!"
            response_text += f"\n\n{quest_complete_text}"
    
    # Record action for AI learning
    try:
        ai_learning.record_action(command, state, success, response_type, response_text)
    except Exception as e:
        print(f"Error recording action: {e}")
    
    return response_text

@app.route('/api/game/save', methods=['POST'])
def save_game():
    """Save game data"""
    session_id = request.json.get('session_id')
    if not session_id or session_id not in game_instances:
        return jsonify({'error': 'Game session not found'}), 404
    
    game_data = game_instances[session_id]
    try:
        game_data['ai_learning'].save_data()
        return jsonify({'success': True, 'message': 'Game saved successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 
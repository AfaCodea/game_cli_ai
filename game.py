from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich import box
import time
import readline
from game_state import GameState
from ai_integration import generate_description, generate_puzzle, generate_npc_dialogue, generate_contextual_response, generate_quest_description, generate_location_description
from ai_learning_system import AILearningSystem
from combat_system import CombatSystem
from crafting_system import CraftingSystem
from trading_system import TradingSystem
from save_load_system import SaveLoadSystem

class Game:
    def __init__(self):
        self.console = Console()
        self.state = GameState()
        self.ai_learning = AILearningSystem()
        
        # Initialize new systems
        self.combat_system = CombatSystem()
        self.crafting_system = CraftingSystem()
        self.trading_system = TradingSystem()
        self.save_load_system = SaveLoadSystem()
        
        # Combat state
        self.in_combat = False
        self.current_enemy = None
        
        # Command aliases for user-friendliness
        self.command_aliases = {
            "i": "inventaris",
            "s": "status",
            "l": "lihat",
            "p": "pergi ke",
            "a": "ambil",
            "g": "gunakan",
            "h": "help",
            "q": "quest",
            "m": "merchant"
        }
        
        # Setup command autocomplete
        self.setup_autocomplete()
    
    def setup_autocomplete(self):
        """Setup command autocomplete functionality"""
        # List of all available commands for autocomplete
        commands = [
            "lihat", "status", "inventaris", "pergi ke", "ambil", "gunakan",
            "serang", "lari", "serangan", "status pertarungan",
            "crafting", "buat", "materials", "tools", "skills",
            "merchant", "beli", "jual", "tawar", "reputation",
            "simpan", "muat", "daftar save", "hapus save",
            "bicara dengan", "quest", "mulai quest", "tanya", "pecahkan teka-teki",
            "ai_learn", "ai_suggest", "help", "keluar", "tutorial"
        ]
        
        # Add aliases to commands list
        for alias in self.command_aliases.keys():
            commands.append(alias)
        
        def completer(text, state):
            options = [cmd for cmd in commands if cmd.startswith(text.lower())]
            if state < len(options):
                return options[state]
            else:
                return None
        
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)
    
    def show_tutorial(self):
        """Show interactive tutorial for new players"""
        tutorial_text = """
🎮 **Tutorial Game AI Petualangan** 🎮

Selamat datang di tutorial interaktif! Mari belajar cara bermain:

1️⃣ **Melihat Sekitar**: Ketik 'lihat' atau 'l' untuk melihat lokasi saat ini
2️⃣ **Cek Status**: Ketik 'status' atau 's' untuk melihat status karakter
3️⃣ **Inventaris**: Ketik 'inventaris' atau 'i' untuk melihat barang yang dimiliki
4️⃣ **Bergerak**: Ketik 'pergi ke [lokasi]' atau 'p [lokasi]' untuk berpindah
5️⃣ **Mengambil Item**: Ketik 'ambil [item]' atau 'a [item]' untuk mengambil barang

Tips:
- Gunakan Tab untuk autocomplete perintah
- Ketik 'help' atau 'h' kapan saja untuk melihat daftar perintah
- Perintah singkat tersedia untuk aksi umum (i, s, l, p, a, g, h, q, m)

Apakah Anda ingin mencoba tutorial interaktif? (ya/tidak)
        """
        
        self.console.print(Panel.fit(tutorial_text, style="bold green", title="[bold yellow]Tutorial[/bold yellow]"))
        choice = Prompt.ask("Pilihan Anda", choices=["ya", "tidak"], default="ya")
        
        if choice.lower() == "ya":
            self.interactive_tutorial()
        else:
            self.console.print("[yellow]Anda dapat mengetik 'tutorial' kapan saja untuk memulai tutorial.[/yellow]")
    
    def interactive_tutorial(self):
        """Run interactive tutorial with guided steps"""
        self.console.print("\n[bold green]Mari mulai tutorial interaktif![/bold green]")
        
        # Step 1: Look around
        self.console.print("\n[bold]Langkah 1:[/bold] Ketik 'lihat' atau 'l' untuk melihat lokasi saat ini")
        while True:
            cmd = Prompt.ask(">").strip().lower()
            if cmd in ["lihat", "l"]:
                self.handle_command(cmd)
                break
            else:
                self.console.print("[yellow]Coba ketik 'lihat' atau 'l'[/yellow]")
        
        # Step 2: Check status
        self.console.print("\n[bold]Langkah 2:[/bold] Ketik 'status' atau 's' untuk melihat status karakter")
        while True:
            cmd = Prompt.ask(">").strip().lower()
            if cmd in ["status", "s"]:
                self.handle_command(cmd)
                break
            else:
                self.console.print("[yellow]Coba ketik 'status' atau 's'[/yellow]")
        
        # Step 3: Check inventory
        self.console.print("\n[bold]Langkah 3:[/bold] Ketik 'inventaris' atau 'i' untuk melihat inventaris")
        while True:
            cmd = Prompt.ask(">").strip().lower()
            if cmd in ["inventaris", "i"]:
                self.handle_command(cmd)
                break
            else:
                self.console.print("[yellow]Coba ketik 'inventaris' atau 'i'[/yellow]")
        
        # Tutorial complete
        self.console.print("\n[bold green]Selamat! Anda telah menyelesaikan tutorial dasar![/bold green]")
        self.console.print("[green]Anda dapat mengetik 'help' atau 'h' kapan saja untuk melihat daftar perintah lengkap.[/green]")
        self.console.print("[green]Selamat berpetualang![/green]\n")
    
    def start_game(self):
        """Start the game"""
        welcome_text = """
🎮 **Game AI Petualangan - Advanced Edition** 🎮

Selamat datang di dunia petualangan yang penuh dengan misteri, 
pertarungan epik, crafting yang kompleks, dan perdagangan yang dinamis!

Fitur baru yang tersedia:
⚔️ Combat System - Pertarungan dengan monster dan NPC
🔨 Crafting System - Buat senjata, armor, dan ramuan
💰 Trading System - Berdagang dengan merchant
💾 Save/Load System - Simpan dan muat progress
🧠 AI Learning - AI yang terus belajar dari aksi Anda

Ketik 'help' untuk melihat semua perintah yang tersedia!
Ketik 'tutorial' untuk memulai tutorial interaktif!
        """
        
        self.console.print(Panel.fit(welcome_text, style="bold blue", title="[bold yellow]Selamat Datang[/bold yellow]"))
        
        # Ask if player wants to start tutorial
        start_tutorial = Prompt.ask("Apakah Anda ingin memulai tutorial? (pemain baru disarankan)", choices=["ya", "tidak"], default="ya")
        if start_tutorial.lower() == "ya":
            self.show_tutorial()
        else:
            self.show_help()
            
        self.main_game_loop()
    
    def show_contextual_help(self, command):
        """Show contextual help based on current command and game state"""
        # Dictionary of contextual help tips
        contextual_tips = {
            "lihat": {
                "tips": [
                    "Perhatikan item dan NPC yang ada di lokasi ini.",
                    "Anda dapat mengambil item dengan perintah 'ambil [item]' atau 'a [item]'.",
                    "Untuk berbicara dengan NPC, gunakan 'bicara dengan [npc]'."
                ],
                "related_commands": ["ambil", "bicara dengan", "pergi ke"]
            },
            "status": {
                "tips": [
                    "Health rendah? Gunakan item penyembuhan dengan 'gunakan [item]'.",
                    "Tingkatkan level dengan menyelesaikan quest dan mengalahkan monster.",
                    "Gold dapat digunakan untuk membeli item dari merchant."
                ],
                "related_commands": ["gunakan", "quest", "merchant"]
            },
            "inventaris": {
                "tips": [
                    "Item dapat digunakan dengan perintah 'gunakan [item]' atau 'g [item]'.",
                    "Beberapa item dapat digunakan untuk crafting.",
                    "Item yang tidak diperlukan dapat dijual ke merchant."
                ],
                "related_commands": ["gunakan", "crafting", "jual"]
            },
            "pergi ke": {
                "tips": [
                    "Pastikan Anda telah mengambil semua item penting sebelum berpindah.",
                    "Beberapa lokasi mungkin memiliki monster atau teka-teki.",
                    "Gunakan 'lihat' setelah berpindah untuk melihat lokasi baru."
                ],
                "related_commands": ["lihat", "ambil", "serang"]
            }
        }
        
        # Show contextual help if available
        if command in contextual_tips:
            tips = contextual_tips[command]["tips"]
            related = contextual_tips[command]["related_commands"]
            
            # Randomly select one tip to show (to avoid overwhelming the player)
            import random
            tip = random.choice(tips)
            
            # Only show tips occasionally (30% chance)
            if random.random() < 0.3:
                self.console.print(f"\n[dim italic]💡 Tip: {tip}[/dim italic]")
                self.console.print(f"[dim italic]Perintah terkait: {', '.join(related)}[/dim italic]")
    
    def show_help(self):
        """Show comprehensive help"""
        help_text = """
**🎯 PERINTAH DASAR:**
- `lihat` - Melihat lokasi saat ini
- `status` - Status pemain lengkap
- `inventaris` - Inventaris dan crafting materials
- `pergi ke [lokasi]` - Pindah ke lokasi lain
- `ambil [item]` - Ambil item dari lokasi
- `gunakan [item]` - Gunakan item dari inventaris

**⚔️ COMBAT SYSTEM:**
- `serang [monster]` - Mulai pertarungan dengan monster
- `lari` - Coba melarikan diri dari pertarungan
- `serangan [action]` - Lakukan aksi dalam pertarungan
- `status pertarungan` - Lihat status pertarungan

**🔨 CRAFTING SYSTEM:**
- `crafting` - Lihat recipes yang tersedia
- `buat [recipe]` - Buat item menggunakan recipe
- `materials` - Lihat materials yang dimiliki
- `tools` - Lihat tools crafting yang dimiliki
- `skills` - Lihat level crafting skills

**💰 TRADING SYSTEM:**
- `merchant` - Lihat daftar merchant
- `beli [item] [quantity]` - Beli item dari merchant
- `jual [item] [quantity]` - Jual item ke merchant
- `tawar [item]` - Tawar harga dengan merchant
- `reputation` - Lihat reputation dengan merchant

**💾 SAVE/LOAD SYSTEM:**
- `simpan [nama]` - Simpan game
- `muat [nama]` - Muat game
- `daftar save` - Lihat daftar save files
- `hapus save [nama]` - Hapus save file

**🎭 INTERAKSI:**
- `bicara dengan [npc]` - Bicara dengan NPC
- `quest` - Lihat daftar quest
- `mulai quest [id]` - Mulai quest
- `tanya [pertanyaan]` - Tanya ke AI
- `pecahkan teka-teki` - Dapatkan teka-teki

**🧠 AI LEARNING:**
- `ai_learn` - Laporan pembelajaran AI
- `ai_suggest` - Saran dari AI

**📋 LAINNYA:**
- `help` atau `h` - Tampilkan bantuan ini
- `tutorial` - Mulai tutorial interaktif
- `keluar` - Keluar dari game

**⚡ ALIAS PERINTAH:**
- `i` - Alias untuk inventaris
- `s` - Alias untuk status
- `l` - Alias untuk lihat
- `p` - Alias untuk pergi ke
- `a` - Alias untuk ambil
- `g` - Alias untuk gunakan
- `h` - Alias untuk help
- `q` - Alias untuk quest
- `m` - Alias untuk merchant
        """
        
        self.console.print(Panel.fit(help_text, style="bold green", title="[bold yellow]Bantuan Lengkap[/bold yellow]"))
    
    def handle_command(self, command):
        """Handle player commands with enhanced systems"""
        command = command.strip()
        if not command:
            self.console.print("[red]Masukkan perintah yang valid.[/red]")
            return
        
        try:
            # Process command aliases
            cmd = command.lower()
            
            # Check if command is an alias and replace with full command
            if cmd in self.command_aliases:
                full_command = self.command_aliases[cmd]
                # If the alias is a prefix (like 'p' for 'pergi ke'), preserve the rest of the command
                if len(command) > len(cmd) and command[len(cmd)] == ' ':
                    command = full_command + command[len(cmd):]
                else:
                    command = full_command
                cmd = command.lower()
                self.console.print(f"[dim](Menggunakan alias: {full_command})[/dim]")
            
            self.state.add_action(command)
            success = True
            response_type = "success"
            response_text = ""
            
            # Tutorial command
            if cmd == "tutorial":
                self.show_tutorial()
                return
            
            # Basic commands
            elif cmd == "keluar":
                self.state.game_over = True
                response_text = "Anda meninggalkan petualangan. Sampai jumpa!"
                self.console.print(Panel.fit(response_text, style="bold red", title="[bold yellow]Keluar[/bold yellow]"))
            
            elif cmd == "help" or cmd == "h":
                self.show_help()
                return
            
            elif cmd == "lihat":
                response_text = self.describe_current_location()
                # Tambahkan bantuan kontekstual
                self.show_contextual_help("lihat")
            
            elif cmd == "status":
                response_text = self.show_status()
                # Tambahkan bantuan kontekstual
                self.show_contextual_help("status")
            
            elif cmd == "inventaris":
                response_text = self.show_inventory()
                # Tambahkan bantuan kontekstual
                self.show_contextual_help("inventaris")
            
            elif cmd.startswith("pergi ke"):
                response_text = self.handle_movement(command)
            
            elif cmd.startswith("ambil"):
                response_text = self.handle_take_item(command)
            
            elif cmd.startswith("gunakan"):
                response_text = self.handle_use_item(command)
            
            # Combat commands
            elif cmd.startswith("serang"):
                response_text = self.handle_combat_start(command)
            
            elif cmd == "lari":
                response_text = self.handle_escape()
            
            elif cmd.startswith("serangan"):
                response_text = self.handle_combat_action(command)
            
            elif cmd == "status pertarungan":
                response_text = self.show_combat_status()
            
            # Crafting commands
            elif cmd == "crafting":
                response_text = self.show_crafting_recipes()
            
            elif cmd.startswith("buat"):
                response_text = self.handle_crafting(command)
            
            elif cmd == "materials":
                response_text = self.show_materials()
            
            elif cmd == "tools":
                response_text = self.show_tools()
            
            elif cmd == "skills":
                response_text = self.show_crafting_skills()
            
            # Trading commands
            elif cmd == "merchant":
                response_text = self.show_merchants()
            
            elif cmd.startswith("beli"):
                response_text = self.handle_buy_item(command)
            
            elif cmd.startswith("jual"):
                response_text = self.handle_sell_item(command)
            
            elif cmd.startswith("tawar"):
                response_text = self.handle_haggle(command)
            
            elif cmd == "reputation":
                response_text = self.show_reputation()
            
            # Save/Load commands
            elif cmd.startswith("simpan"):
                response_text = self.handle_save_game(command)
            
            elif cmd.startswith("muat"):
                response_text = self.handle_load_game(command)
            
            elif cmd == "daftar save":
                response_text = self.show_save_files()
            
            elif cmd.startswith("hapus save"):
                response_text = self.handle_delete_save(command)
            
            # Interaction commands
            elif cmd.startswith("bicara dengan"):
                response_text = self.handle_npc_conversation(command)
            
            elif cmd == "quest":
                response_text = self.show_quests()
            
            elif cmd.startswith("mulai quest"):
                response_text = self.handle_start_quest(command)
            
            elif cmd.startswith("tanya"):
                response_text = self.handle_ai_question(command)
            
            elif cmd == "pecahkan teka-teki":
                response_text = self.handle_puzzle()
            
            # AI Learning commands
            elif cmd == "ai_learn":
                response_text = self.show_ai_learning_report()
            
            elif cmd == "ai_suggest":
                response_text = self.show_ai_suggestions_detailed()
            
            elif cmd == "help":
                self.show_help()
                response_text = "Bantuan ditampilkan"
            
            else:
                # Free-form commands for AI narration
                game_context = self.state.get_context_for_ai()
                ai_narration = generate_contextual_response(
                    command, 
                    game_context, 
                    self.state.conversation_history, 
                    self.state.player_actions
                )
                response_text = f"**Narasi Petualangan:**\n\n{ai_narration}"
                response_type = "ai_response"
                
                self.state.add_conversation(f"Player: {command} | AI: {ai_narration[:100]}...")
                
                # Check quest completion
                completed_quest = self.state.check_quest_completion()
                if completed_quest:
                    quest_complete_text = f"🎉 Quest '{completed_quest.title}' selesai! Anda mendapatkan reward!"
                    self.console.print(Panel.fit(quest_complete_text, title="[bold green]Quest Selesai[/bold green]", style="bold green"))
                    response_text += f"\n\n{quest_complete_text}"
            
            # Record action for AI learning
            self.record_action_for_learning(command, success, response_type, response_text)
            
            # Display response
            if response_text:
                if response_type == "ai_response":
                    self.console.print(Panel.fit(response_text, title="[bold cyan]Narasi Petualangan[/bold cyan]", style="cyan"))
                elif response_type == "error":
                    self.console.print(f"[red]{response_text}[/red]")
                else:
                    self.console.print(Panel.fit(response_text, title="[bold green]Game[/bold green]", style="green"))
        
        except Exception as e:
            error_msg = f"Error saat memproses perintah: {e}"
            friendly_message = error_msg
            
            # Pesan error yang lebih jelas dan informatif
            friendly_errors = {
                "index out of range": "Perintah tidak lengkap. Gunakan format yang benar, misalnya 'pergi ke [lokasi]'.",
                "not found": "Item atau lokasi tidak ditemukan. Periksa penulisan atau gunakan 'lihat' untuk melihat apa yang tersedia.",
                "not enough": "Anda tidak memiliki cukup sumber daya untuk melakukan tindakan ini.",
                "already": "Anda sudah melakukan tindakan ini sebelumnya.",
                "cannot": "Anda tidak dapat melakukan tindakan ini sekarang.",
                "invalid": "Perintah tidak valid. Gunakan 'help' untuk melihat daftar perintah yang tersedia."
            }
            
            # Cek apakah error cocok dengan salah satu pesan yang lebih ramah
            for key, message in friendly_errors.items():
                if key in str(e).lower():
                    friendly_message = message
                    break
            
            # Tampilkan pesan error yang lebih ramah
            self.console.print(f"[red]{friendly_message}[/red]")
            self.console.print("[yellow]Coba ketik 'help' untuk melihat perintah yang tersedia.[/yellow]")
            
            # Tambahkan saran perintah yang mungkin dimaksud jika perintah tidak valid
            if "invalid" in str(e).lower() and len(command.split()) > 0:
                cmd_word = command.split()[0].lower()
                all_commands = list(self.command_aliases.values()) + ["lihat", "status", "inventaris", "pergi ke", "ambil", "gunakan", "help", "tutorial"]
                
                # Cari perintah yang mirip
                import difflib
                similar_commands = difflib.get_close_matches(cmd_word, all_commands, n=3, cutoff=0.6)
                
                if similar_commands:
                    suggestion = "Mungkin maksud Anda: " + ", ".join(f"'{cmd}'" for cmd in similar_commands)
                    self.console.print(f"[yellow]{suggestion}[/yellow]")
            
            self.record_action_for_learning(command, False, "error", friendly_message)
    
    def describe_current_location(self):
        """Describe current location with enhanced features"""
        current_loc = self.state.get_current_location_info()
        description = generate_location_description(
            self.state.current_location, 
            current_loc, 
            current_loc.visited
        )
        
        response = f"**{current_loc.name}**\n\n{description}"
        
        # Add items
        if current_loc.items:
            items_text = ", ".join([item.name for item in current_loc.items])
            response += f"\n\n**Item yang terlihat:** {items_text}"
        
        # Add NPCs
        if current_loc.npcs:
            npcs_text = ", ".join(current_loc.npcs)
            response += f"\n\n**NPC yang terlihat:** {npcs_text}"
        
        # Add monsters
        if current_loc.monsters:
            monsters_text = ", ".join(current_loc.monsters)
            response += f"\n\n**Monster yang mungkin muncul:** {monsters_text}"
        
        # Add crafting stations
        if current_loc.crafting_stations:
            stations_text = ", ".join(current_loc.crafting_stations)
            response += f"\n\n**Crafting stations:** {stations_text}"
        
        # Add merchants
        if current_loc.merchants:
            merchants_text = ", ".join(current_loc.merchants)
            response += f"\n\n**Merchants:** {merchants_text}"
        
        return response
    
    def show_status(self):
        """Show comprehensive player status"""
        current_loc = self.state.get_current_location_info()
        
        status = f"""
**Status Pemain:**
- Nama: {self.state.player_name}
- Health: {self.state.health}/{self.state.max_health}
- Level: {self.state.level}
- Experience: {self.state.experience}
- Gold: {self.state.gold}
- Lokasi: {current_loc.name}

**Combat Stats:**
- Attack: {self.state.combat_stats.attack}
- Defense: {self.state.combat_stats.defense}
- Speed: {self.state.combat_stats.speed}
- Critical Chance: {self.state.combat_stats.critical_chance:.1%}
- Dodge Chance: {self.state.combat_stats.dodge_chance:.1%}

**Crafting Skills:**
"""
        
        for skill, level in self.state.crafting_skills.items():
            status += f"- {skill.capitalize()}: Level {level}\n"
        
        status += f"\n**Play Time:** {self.state.get_play_time() // 60} menit {self.state.get_play_time() % 60} detik"
        
        return status
    
    def show_inventory(self):
        """Show inventory with crafting materials"""
        if not self.state.inventory and not self.state.crafting_materials:
            return "Inventaris Anda kosong."
        
        inventory_text = "**Inventaris Anda:**\n"
        
        # Group items by type
        items_by_type = {}
        for item in self.state.inventory:
            item_type = item.item_type
            if item_type not in items_by_type:
                items_by_type[item_type] = []
            items_by_type[item_type].append(item)
        
        for item_type, items in items_by_type.items():
            inventory_text += f"\n**{item_type.upper()}:**\n"
            for item in items:
                stats_text = ""
                if item.stats:
                    stats_text = f" ({', '.join([f'{k}: {v}' for k, v in item.stats.items()])})"
                inventory_text += f"- {item.name}: {item.description}{stats_text} (Berat: {item.weight}, Nilai: {item.value})\n"
        
        # Show crafting materials
        if self.state.crafting_materials:
            inventory_text += "\n**Crafting Materials:**\n"
            for material, quantity in self.state.crafting_materials.items():
                inventory_text += f"- {material}: {quantity}\n"
        
        return inventory_text
    
    def handle_movement(self, command):
        """Handle movement command"""
        parts = command.split(" ", 2)
        if len(parts) >= 3:
            location = parts[2].strip()
            if self.state.move_to(location):
                response = f"Anda pindah ke **{self.state.get_current_location_info().name}**"
                # Auto-show location description
                response += f"\n\n{self.describe_current_location()}"
                return response
            else:
                available = ", ".join(self.state.get_available_locations())
                return f"Tidak bisa pergi ke '{location}'. Lokasi yang tersedia: {available}"
        else:
            return "Format: pergi ke [nama_lokasi]"
    
    def handle_take_item(self, command):
        """Handle take item command"""
        parts = command.split(" ", 1)
        if len(parts) >= 2:
            item_name = parts[1].strip()
            current_loc = self.state.get_current_location_info()
            
            for item in current_loc.items:
                if item.name.lower() == item_name.lower():
                    self.state.add_item_to_inventory(item)
                    current_loc.items.remove(item)
                    
                    # If it's a material, add to crafting materials
                    if item.item_type == "material":
                        self.state.add_crafting_material(item.name, 1)
                    
                    return f"Anda mengambil **{item.name}**: {item.description}"
            
            return f"Item '{item_name}' tidak ditemukan di lokasi ini."
        else:
            return "Format: ambil [nama_item]"
    
    def handle_use_item(self, command):
        """Handle use item command"""
        parts = command.split(" ", 1)
        if len(parts) >= 2:
            item_name = parts[1].strip()
            item = self.state.get_inventory_item(item_name)
            
            if item:
                if item.usable:
                    if item.consumable:
                        self.state.remove_item_from_inventory(item_name)
                    
                    # Handle different item types
                    if item.item_type == "consumable":
                        if "heal" in item.stats:
                            heal_amount = item.stats["heal"]
                            self.state.heal(heal_amount)
                            return f"**Menggunakan {item.name}:**\nAnda sembuh {heal_amount} HP!"
                        elif "mana_restore" in item.stats:
                            mana_amount = item.stats["mana_restore"]
                            self.state.combat_stats.mana = min(self.state.combat_stats.max_mana, 
                                                             self.state.combat_stats.mana + mana_amount)
                            return f"**Menggunakan {item.name}:**\nMana Anda pulih {mana_amount}!"
                    
                    # Generate AI response for other items
                    prompt = f"Pemain menggunakan {item.name} di {self.state.get_current_location_info().name}. Berikan narasi yang menarik tentang apa yang terjadi."
                    result = generate_description(prompt)
                    return f"**Menggunakan {item.name}:**\n\n{result}"
                else:
                    return f"Item '{item_name}' tidak bisa digunakan."
            else:
                return f"Item '{item_name}' tidak ada di inventaris."
        else:
            return "Format: gunakan [nama_item]"
    
    # Combat methods
    def handle_combat_start(self, command):
        """Handle combat start command"""
        if self.in_combat:
            return "Anda sudah dalam pertarungan!"
        
        parts = command.split(" ", 1)
        if len(parts) >= 2:
            monster_name = parts[1].strip()
            
            # Check if monster can spawn in current location
            current_loc = self.state.get_current_location_info()
            if monster_name in current_loc.monsters:
                # Start combat
                result = self.combat_system.start_combat(self.state.combat_stats, monster_name)
                if result["success"]:
                    self.in_combat = True
                    self.current_enemy = monster_name
                    return f"⚔️ Pertarungan dimulai dengan {monster_name}!\n\n{result['combat_log'][-1]}"
                else:
                    return result["error"]
            else:
                return f"Monster '{monster_name}' tidak ada di lokasi ini. Monster yang tersedia: {', '.join(current_loc.monsters)}"
        else:
            return "Format: serang [nama_monster]"
    
    def handle_escape(self):
        """Handle escape command"""
        if not self.in_combat:
            return "Anda tidak sedang dalam pertarungan."
        
        result = self.combat_system.escape_combat()
        if result["success"]:
            self.in_combat = False
            self.current_enemy = None
            return result["combat_log"][-1]
        else:
            return result["error"]
    
    def handle_combat_action(self, command):
        """Handle combat action command"""
        if not self.in_combat:
            return "Anda tidak sedang dalam pertarungan."
        
        parts = command.split(" ", 1)
        if len(parts) >= 2:
            action = parts[1].strip()
            result = self.combat_system.execute_action(action)
            
            if result["success"]:
                # Update player stats
                if "player_health" in result:
                    self.state.combat_stats.health = result["player_health"]
                    self.state.health = result["player_health"]
                
                # Check if combat ended
                if result["result"] in ["victory", "defeat"]:
                    self.in_combat = False
                    self.current_enemy = None
                    
                    if result["result"] == "victory":
                        # Add rewards
                        if "rewards" in result:
                            rewards = result["rewards"]
                            if "gold" in rewards:
                                self.state.add_gold(rewards["gold"])
                            if "experience" in rewards:
                                self.state.add_experience(rewards["experience"])
                            if "items" in rewards:
                                for item_name in rewards["items"]:
                                    # Create item and add to inventory
                                    pass
                
                return "\n".join(result["combat_log"][-3:])  # Show last 3 log entries
            else:
                return result["error"]
        else:
            return "Format: serangan [action]"
    
    def show_combat_status(self):
        """Show current combat status"""
        if not self.in_combat:
            return "Anda tidak sedang dalam pertarungan."
        
        status = self.combat_system.get_combat_status()
        return f"""
**Status Pertarungan:**
- Enemy: {status['enemy'].name}
- Player Health: {status['player_health']}/{self.state.combat_stats.max_health}
- Enemy Health: {status['enemy_health']}/{status['enemy'].stats.max_health}
- Turn: {status['turn_count']}

**Available Actions:**
"""
        
        for action in status["available_actions"]:
            status += f"- {action['display_name']}: {action['description']}\n"
        
        return status
    
    # Crafting methods
    def show_crafting_recipes(self):
        """Show available crafting recipes"""
        recipes = self.crafting_system.get_available_recipes(
            self.state.crafting_materials, 
            self.state.crafting_tools
        )
        
        if not recipes:
            return "Tidak ada recipe yang tersedia."
        
        recipes_text = "**Available Recipes:**\n"
        for recipe_info in recipes:
            recipe = recipe_info["recipe"]
            crafted_item = recipe_info["crafted_item"]
            status = recipe_info["status"]
            
            recipes_text += f"\n**{recipe.name}** ({status})\n"
            recipes_text += f"Description: {recipe.description}\n"
            recipes_text += f"Difficulty: {recipe.difficulty.value}\n"
            recipes_text += f"Materials: {', '.join([f'{qty} {mat}' for mat, qty in recipe.materials.items()])}\n"
            recipes_text += f"Tools: {', '.join(recipe.tools_required) if recipe.tools_required else 'None'}\n"
            recipes_text += f"Skill: {recipe.skill_required} (Level {recipe.skill_level_required})\n"
            
            if crafted_item:
                recipes_text += f"Crafted Item: {crafted_item.name} (Value: {crafted_item.value})\n"
            
            if status == "missing_materials":
                recipes_text += f"Missing: {', '.join(recipe_info['missing_materials'])}\n"
        
        return recipes_text
    
    def handle_crafting(self, command):
        """Handle crafting command"""
        parts = command.split(" ", 1)
        if len(parts) >= 2:
            recipe_name = parts[1].strip()
            
            result = self.crafting_system.craft_item(
                recipe_name, 
                self.state.crafting_materials, 
                self.state.crafting_tools
            )
            
            if result["success"]:
                # Add crafted item to inventory
                crafted_item = result["crafted_item"]
                self.state.add_item_to_inventory(crafted_item)
                
                # Improve skill
                if result["skill_improved"]:
                    self.state.improve_crafting_skill(result["skill_improved"], result["experience_gained"])
                
                return f"🔨 Berhasil membuat {crafted_item.name}!\nExperience gained: {result['experience_gained']}"
            else:
                return result["error"]
        else:
            return "Format: buat [recipe_name]"
    
    def show_materials(self):
        """Show crafting materials"""
        if not self.state.crafting_materials:
            return "Anda tidak memiliki materials."
        
        materials_text = "**Crafting Materials:**\n"
        for material, quantity in self.state.crafting_materials.items():
            materials_text += f"- {material}: {quantity}\n"
        
        return materials_text
    
    def show_tools(self):
        """Show crafting tools"""
        if not self.state.crafting_tools:
            return "Anda tidak memiliki crafting tools."
        
        tools_text = "**Crafting Tools:**\n"
        for tool in self.state.crafting_tools:
            tools_text += f"- {tool}\n"
        
        return tools_text
    
    def show_crafting_skills(self):
        """Show crafting skills"""
        skills_text = "**Crafting Skills:**\n"
        for skill, level in self.state.crafting_skills.items():
            skills_text += f"- {skill.capitalize()}: Level {level}\n"
        
        return skills_text
    
    # Trading methods
    def show_merchants(self):
        """Show available merchants"""
        merchants = self.trading_system.get_merchant_list()
        
        if not merchants:
            return "Tidak ada merchant yang tersedia."
        
        merchants_text = "**Available Merchants:**\n"
        for merchant in merchants:
            reputation = merchant["player_reputation"]
            rep_status = "Friendly" if reputation > 70 else "Neutral" if reputation > 30 else "Hostile"
            
            merchants_text += f"\n**{merchant['display_name']}** ({merchant['type']})\n"
            merchants_text += f"Location: {merchant['location']}\n"
            merchants_text += f"Reputation: {reputation}/100 ({rep_status})\n"
            merchants_text += f"Gold: {merchant['gold']}\n"
        
        return merchants_text
    
    def handle_buy_item(self, command):
        """Handle buy item command"""
        parts = command.split(" ")
        if len(parts) >= 3:
            item_name = parts[1]
            quantity = int(parts[2]) if len(parts) > 2 else 1
            
            # For now, use first available merchant
            merchants = self.trading_system.get_merchant_list()
            if not merchants:
                return "Tidak ada merchant yang tersedia."
            
            merchant_name = merchants[0]["name"]
            result = self.trading_system.buy_item(
                merchant_name, 
                item_name, 
                quantity, 
                self.state.gold,
                self.state.get_crafting_skill_level("negotiation")
            )
            
            if result["success"]:
                self.state.remove_gold(result["total_cost"])
                # Add item to inventory (simplified)
                return f"💰 Berhasil membeli {quantity} {item_name} seharga {result['total_cost']} gold!"
            else:
                return result["error"]
        else:
            return "Format: beli [item_name] [quantity]"
    
    def handle_sell_item(self, command):
        """Handle sell item command"""
        parts = command.split(" ")
        if len(parts) >= 3:
            item_name = parts[1]
            quantity = int(parts[2]) if len(parts) > 2 else 1
            
            # Check if player has the item
            item = self.state.get_inventory_item(item_name)
            if not item:
                return f"Anda tidak memiliki {item_name}."
            
            # For now, use first available merchant
            merchants = self.trading_system.get_merchant_list()
            if not merchants:
                return "Tidak ada merchant yang tersedia."
            
            merchant_name = merchants[0]["name"]
            
            # Create simplified inventory for trading
            player_inventory = {item_name: 1}  # Simplified
            
            result = self.trading_system.sell_item(
                merchant_name, 
                item_name, 
                quantity, 
                player_inventory,
                self.state.get_crafting_skill_level("negotiation")
            )
            
            if result["success"]:
                self.state.add_gold(result["total_earnings"])
                self.state.remove_item_from_inventory(item_name)
                return f"💰 Berhasil menjual {quantity} {item_name} seharga {result['total_earnings']} gold!"
            else:
                return result["error"]
        else:
            return "Format: jual [item_name] [quantity]"
    
    def handle_haggle(self, command):
        """Handle haggle command"""
        parts = command.split(" ", 1)
        if len(parts) >= 2:
            item_name = parts[1].strip()
            
            # For now, use first available merchant
            merchants = self.trading_system.get_merchant_list()
            if not merchants:
                return "Tidak ada merchant yang tersedia."
            
            merchant_name = merchants[0]["name"]
            
            # Get current price (simplified)
            current_price = 10  # Default price
            
            result = self.trading_system.haggle(
                merchant_name, 
                item_name, 
                current_price,
                self.state.get_crafting_skill_level("negotiation")
            )
            
            if result["success"]:
                return result["message"]
            else:
                return result["error"]
        else:
            return "Format: tawar [item_name]"
    
    def show_reputation(self):
        """Show reputation with merchants"""
        if not self.state.merchant_reputation:
            return "Anda belum memiliki reputation dengan merchant manapun."
        
        reputation_text = "**Merchant Reputation:**\n"
        for merchant, rep in self.state.merchant_reputation.items():
            status = "Friendly" if rep > 70 else "Neutral" if rep > 30 else "Hostile"
            reputation_text += f"- {merchant}: {rep}/100 ({status})\n"
        
        return reputation_text
    
    # Save/Load methods
    def handle_save_game(self, command):
        """Handle save game command"""
        parts = command.split(" ", 1)
        save_name = parts[1].strip() if len(parts) > 1 else f"save_{int(time.time())}"
        
        # Get current game state
        game_state_data = self.state.save_game_state()
        
        result = self.save_load_system.save_game(game_state_data, save_name)
        
        if result["success"]:
            return f"💾 Game berhasil disimpan sebagai '{save_name}'"
        else:
            return result["error"]
    
    def handle_load_game(self, command):
        """Handle load game command"""
        parts = command.split(" ", 1)
        if len(parts) < 2:
            return "Format: muat [save_name]"
        
        save_name = parts[1].strip()
        
        result = self.save_load_system.load_game(save_name)
        
        if result["success"]:
            # Load game state
            self.state.load_game_state(result["game_state"])
            return f"📂 Game berhasil dimuat dari '{save_name}'"
        else:
            return result["error"]
    
    def show_save_files(self):
        """Show available save files"""
        save_files = self.save_load_system.get_save_files()
        
        if not save_files:
            return "Tidak ada save file yang tersedia."
        
        save_text = "**Available Save Files:**\n"
        for save_file in save_files:
            if "error" in save_file:
                save_text += f"\n**{save_file['save_name']}** (Corrupted)\n"
                save_text += f"Error: {save_file['error']}\n"
            else:
                metadata = save_file["metadata"]
                save_text += f"\n**{save_file['save_name']}**\n"
                save_text += f"Player: {metadata['player_name']}\n"
                save_text += f"Level: {metadata['level']}\n"
                save_text += f"Location: {metadata['location']}\n"
                save_text += f"Save Date: {metadata['save_date']}\n"
        
        return save_text
    
    def handle_delete_save(self, command):
        """Handle delete save command"""
        parts = command.split(" ", 2)
        if len(parts) < 3:
            return "Format: hapus save [save_name]"
        
        save_name = parts[2].strip()
        
        result = self.save_load_system.delete_save(save_name)
        
        if result["success"]:
            return f"🗑️ Save file '{save_name}' berhasil dihapus"
        else:
            return result["error"]
    
    # Existing methods (simplified for brevity)
    def handle_npc_conversation(self, command):
        """Handle NPC conversation"""
        parts = command.split(" ", 2)
        if len(parts) >= 3:
            npc = parts[2].strip()
            current_loc = self.state.get_current_location_info()
            
            if npc in current_loc.npcs:
                dialog = generate_npc_dialogue(npc, f"dia sedang berada di {current_loc.name}")
                return f"**{npc.capitalize()} berkata:**\n\n\"{dialog}\""
            else:
                available_npcs = ", ".join(current_loc.npcs) if current_loc.npcs else "tidak ada"
                return f"NPC '{npc}' tidak ada di lokasi ini. NPC yang tersedia: {available_npcs}"
        else:
            return "Format: bicara dengan [nama_npc]"
    
    def show_quests(self):
        """Show quests"""
        response = "**Daftar Quest:**\n"
        for quest in self.state.quests:
            status = "✅ Selesai" if quest.completed else "🔄 Aktif" if quest.started else "📋 Tersedia"
            response += f"- **{quest.title}** ({quest.quest_id}) - {status}\n  {quest.description}\n\n"
        return response
    
    def handle_start_quest(self, command):
        """Handle start quest command"""
        parts = command.split(" ", 2)
        if len(parts) >= 3:
            quest_id = parts[2].strip()
            if self.state.start_quest(quest_id):
                quest = next((q for q in self.state.quests if q.quest_id == quest_id), None)
                if quest:
                    description = generate_quest_description(quest)
                    return f"**Quest Dimulai:**\n\n{description}"
            else:
                available_quests = ", ".join([q.quest_id for q in self.state.quests])
                return f"Quest '{quest_id}' tidak ditemukan atau sudah dimulai. Quest yang tersedia: {available_quests}"
        else:
            return "Format: mulai quest [quest_id]"
    
    def handle_ai_question(self, command):
        """Handle AI question"""
        question = command[5:].strip()
        if not question:
            return "Format: tanya [pertanyaan]"
        
        ai_answer = generate_description(question)
        return f"**Pertanyaan:** {question}\n\n**AI menjawab:**\n{ai_answer}"
    
    def handle_puzzle(self):
        """Handle puzzle command"""
        puzzle_text = generate_puzzle(f"tentang {self.state.get_current_location_info().name} dan misterinya")
        return f"**Teka-teki dari misteri {self.state.get_current_location_info().name}:**\n\n{puzzle_text}"
    
    def show_ai_learning_report(self):
        """Show AI learning report"""
        return self.ai_learning.get_learning_report()
    
    def show_ai_suggestions_detailed(self):
        """Show detailed AI suggestions"""
        current_context = {
            'location': self.state.current_location,
            'inventory': [item.name for item in self.state.inventory],
            'npcs': self.state.get_current_location_info().npcs,
            'health': self.state.health,
            'level': self.state.level,
            'available_locations': self.state.get_available_locations()
        }
        
        suggestions = self.ai_learning.generate_ai_suggestions(current_context)
        if suggestions:
            return "**AI Suggestions:**\n\n" + "\n".join([f"💡 {suggestion}" for suggestion in suggestions])
        else:
            return "AI belum memiliki cukup data untuk memberikan saran. Terus bermain untuk mendapatkan saran yang lebih baik!"
    
    def record_action_for_learning(self, command, success, response_type, response_text):
        """Record action for AI learning"""
        try:
            self.ai_learning.record_action(command, self.state, success, response_type, response_text)
        except Exception as e:
            print(f"Error recording action: {e}")
    
    def main_game_loop(self):
        """Main game loop"""
        while not self.state.game_over:
            try:
                command = Prompt.ask("\n[bold cyan]Apa yang ingin Anda lakukan?[/bold cyan]")
                self.handle_command(command)
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Game dihentikan oleh user.[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Error dalam game loop: {e}[/red]")
        
        self.console.print("\n[bold red]Game berakhir. Terima kasih telah bermain![/bold red]")
        
        # Save AI learning data
        try:
            self.ai_learning.save_data()
        except Exception as e:
            print(f"Error saving AI learning data: {e}")
from ai_integration import generate_description, generate_puzzle, generate_npc_dialogue, generate_contextual_response, generate_quest_description, generate_location_description
from game_state import GameState, Item
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv
import os

class Game:
    def __init__(self):
        self.state = GameState()
        self.console = Console()

    def start_game(self):
        self.console.print(Panel.fit(f"Selamat datang, [bold cyan]{self.state.player_name}[/bold cyan], di dunia petualangan!", title="[bold yellow]Petualangan Dimulai[/bold yellow]", style="bold magenta"))
        self.describe_current_location()
        self.show_help()
        self.main_game_loop()

    def describe_current_location(self):
        current_loc = self.state.get_current_location_info()
        description = generate_location_description(
            self.state.current_location, 
            current_loc, 
            current_loc.visited
        )
        self.console.print(Panel.fit(f"[bold]Anda berada di:[/bold] [green]{current_loc.name}[/green]\n{description}", title="[bold blue]Lokasi[/bold blue]", style="cyan"))
        
        # Show available items and NPCs
        if current_loc.items:
            items_text = ", ".join([item.name for item in current_loc.items])
            self.console.print(Panel.fit(f"[yellow]Item yang terlihat:[/yellow] {items_text}", title="[bold yellow]Item[/bold yellow]", style="yellow"))
        
        if current_loc.npcs:
            npcs_text = ", ".join(current_loc.npcs)
            self.console.print(Panel.fit(f"[cyan]NPC yang terlihat:[/cyan] {npcs_text}", title="[bold cyan]NPC[/bold cyan]", style="cyan"))

    def show_help(self):
        help_text = (
            "[bold]Perintah yang bisa digunakan:[/bold]\n"
            "[yellow]lihat[/yellow]                : Melihat deskripsi lokasi saat ini\n"
            "[yellow]status[/yellow]               : Melihat status pemain (health, level, gold)\n"
            "[yellow]inventaris[/yellow]           : Melihat inventaris Anda\n"
            "[yellow]pergi ke [lokasi][/yellow]    : Pindah ke lokasi lain\n"
            "[yellow]ambil [item][/yellow]         : Mengambil item dari lokasi\n"
            "[yellow]gunakan [item][/yellow]       : Menggunakan item dari inventaris\n"
            "[yellow]bicara dengan [npc][/yellow]  : Bicara dengan NPC tertentu\n"
            "[yellow]quest[/yellow]                : Melihat daftar quest\n"
            "[yellow]mulai quest [id][/yellow]     : Memulai quest tertentu\n"
            "[yellow]pecahkan teka-teki[/yellow]   : Mendapatkan teka-teki dari AI\n"
            "[yellow]tanya [pertanyaan][/yellow]   : Bertanya bebas ke AI\n"
            "[yellow]help[/yellow]                 : Menampilkan bantuan ini\n"
            "[yellow]keluar[/yellow]               : Keluar dari permainan\n"
            "[yellow]Perintah bebas[/yellow]       : Ketik perintah apapun dan AI akan merespons sebagai narasi petualangan!"
        )
        self.console.print(Panel.fit(help_text, title="[bold green]Bantuan[/bold green]", style="bold white"))

    def show_status(self):
        status_text = (
            f"[bold]Nama:[/bold] {self.state.player_name}\n"
            f"[bold]Health:[/bold] [red]{self.state.health}[/red]/[green]{self.state.max_health}[/green]\n"
            f"[bold]Level:[/bold] [yellow]{self.state.level}[/yellow]\n"
            f"[bold]Experience:[/bold] [cyan]{self.state.experience}[/cyan]\n"
            f"[bold]Gold:[/bold] [gold]{self.state.gold}[/gold]\n"
            f"[bold]Lokasi:[/bold] [blue]{self.state.get_current_location_info().name}[/blue]"
        )
        self.console.print(Panel.fit(status_text, title="[bold green]Status Pemain[/bold green]", style="bold white"))

    def show_inventory(self):
        if self.state.inventory:
            table = Table(title="Inventaris")
            table.add_column("Item", style="cyan")
            table.add_column("Deskripsi", style="white")
            table.add_column("Berat", style="yellow")
            table.add_column("Nilai", style="green")
            
            for item in self.state.inventory:
                table.add_row(item.name, item.description, str(item.weight), str(item.value))
            
            self.console.print(table)
        else:
            self.console.print(Panel.fit("Inventaris Anda kosong.", title="[bold green]Inventaris[/bold green]", style="white"))

    def show_quests(self):
        table = Table(title="Daftar Quest")
        table.add_column("ID", style="cyan")
        table.add_column("Judul", style="yellow")
        table.add_column("Status", style="green")
        table.add_column("Progress", style="blue")
        
        for quest in self.state.quests:
            status = "Selesai" if quest.completed else "Aktif" if quest.started else "Tersedia"
            status_color = "green" if quest.completed else "yellow" if quest.started else "cyan"
            
            if quest.started and not quest.completed:
                progress = self.state.get_quest_progress(quest.quest_id)
                if progress:
                    progress_text = ", ".join([f"{item}: {data['current']}/{data['required']}" for item, data in progress.items()])
                else:
                    progress_text = "0%"
            else:
                progress_text = "N/A"
            
            table.add_row(quest.quest_id, quest.title, f"[{status_color}]{status}[/{status_color}]", progress_text)
        
        self.console.print(table)

    def handle_command(self, command):
        command = command.strip()
        if not command:
            self.console.print("[red]Masukkan perintah yang valid.[/red]")
            return
        
        # Add action to history
        self.state.add_action(command)
        
        cmd = command.lower()
        
        if cmd == "keluar":
            self.state.game_over = True
            self.console.print(Panel.fit("Anda meninggalkan petualangan. Sampai jumpa!", style="bold red", title="[bold yellow]Keluar[/bold yellow]"))
        
        elif cmd == "lihat":
            self.describe_current_location()
        
        elif cmd == "status":
            self.show_status()
        
        elif cmd == "inventaris":
            self.show_inventory()
        
        elif cmd.startswith("pergi ke"):
            parts = command.split(" ", 2)
            if len(parts) >= 3:
                location = parts[2].strip()
                if self.state.move_to(location):
                    self.console.print(Panel.fit(f"Anda pindah ke [green]{self.state.get_current_location_info().name}[/green]", title="[bold blue]Pindah Lokasi[/bold blue]", style="cyan"))
                    self.describe_current_location()
                else:
                    self.console.print(f"[red]Tidak bisa pergi ke {location}. Lokasi yang tersedia: {', '.join(self.state.get_available_locations())}[/red]")
            else:
                self.console.print("[red]Format: pergi ke [nama_lokasi][/red]")
        
        elif cmd.startswith("ambil"):
            parts = command.split(" ", 1)
            if len(parts) >= 2:
                item_name = parts[1].strip()
                current_loc = self.state.get_current_location_info()
                
                # Find item in location
                for item in current_loc.items:
                    if item.name.lower() == item_name.lower():
                        self.state.add_item_to_inventory(item)
                        current_loc.items.remove(item)
                        self.console.print(Panel.fit(f"Anda mengambil [yellow]{item.name}[/yellow]: {item.description}", title="[bold green]Mengambil Item[/bold green]", style="green"))
                        return
                
                self.console.print(f"[red]Item '{item_name}' tidak ditemukan di lokasi ini.[/red]")
            else:
                self.console.print("[red]Format: ambil [nama_item][/red]")
        
        elif cmd.startswith("gunakan"):
            parts = command.split(" ", 1)
            if len(parts) >= 2:
                item_name = parts[1].strip()
                item = self.state.get_inventory_item(item_name)
                
                if item:
                    if item.usable:
                        # Use the item
                        if item.consumable:
                            self.state.remove_item_from_inventory(item_name)
                        
                        # Generate AI response for item usage
                        prompt = f"Pemain menggunakan {item.name} di {self.state.get_current_location_info().name}. Berikan narasi yang menarik tentang apa yang terjadi."
                        result = generate_description(prompt)
                        self.console.print(Panel.fit(result, title="[bold yellow]Menggunakan Item[/bold yellow]", style="yellow"))
                    else:
                        self.console.print(f"[red]Item '{item_name}' tidak bisa digunakan.[/red]")
                else:
                    self.console.print(f"[red]Item '{item_name}' tidak ada di inventaris.[/red]")
            else:
                self.console.print("[red]Format: gunakan [nama_item][/red]")
        
        elif cmd.startswith("bicara dengan"):
            parts = command.split(" ", 2)
            if len(parts) >= 3:
                npc = parts[2].strip()
                current_loc = self.state.get_current_location_info()
                
                if npc in current_loc.npcs:
                    dialog = generate_npc_dialogue(npc, f"dia sedang berada di {current_loc.name}")
                    self.console.print(Panel.fit(f"{npc.capitalize()} berkata: [italic yellow]'{dialog}'[/italic yellow]", title=f"[bold blue]Bicara dengan {npc.capitalize()}[/bold blue]", style="bold cyan"))
                else:
                    self.console.print(f"[red]NPC '{npc}' tidak ada di lokasi ini.[/red]")
            else:
                self.console.print("[red]Format: bicara dengan [nama_npc][/red]")
        
        elif cmd == "quest":
            self.show_quests()
        
        elif cmd.startswith("mulai quest"):
            parts = command.split(" ", 2)
            if len(parts) >= 3:
                quest_id = parts[2].strip()
                if self.state.start_quest(quest_id):
                    quest = next((q for q in self.state.quests if q.quest_id == quest_id), None)
                    if quest:
                        description = generate_quest_description(quest)
                        self.console.print(Panel.fit(description, title="[bold green]Quest Dimulai[/bold green]", style="green"))
                else:
                    self.console.print(f"[red]Quest '{quest_id}' tidak ditemukan atau sudah dimulai.[/red]")
            else:
                self.console.print("[red]Format: mulai quest [quest_id][/red]")
        
        elif cmd == "pecahkan teka-teki":
            puzzle_text = generate_puzzle(f"tentang {self.state.get_current_location_info().name} dan misterinya")
            self.console.print(Panel.fit(f"Teka-teki dari misteri {self.state.get_current_location_info().name}:\n[bold yellow]{puzzle_text}[/bold yellow]", title="[bold magenta]Teka-Teki[/bold magenta]", style="magenta"))
            answer = Prompt.ask("[green]Jawaban Anda[/green]")
            self.console.print("[green]Jawaban Anda telah dicatat. (Fitur pemeriksaan jawaban bisa dikembangkan lebih lanjut)[/green]")
        
        elif cmd.startswith("tanya"):
            question = command[5:].strip()
            if not question:
                self.console.print("[red]Format: tanya [pertanyaan][/red]")
            else:
                self.console.print(Panel.fit(f"[bold]Pertanyaan:[/bold] {question}", title="[bold blue]Tanya AI[/bold blue]", style="bold white"))
                ai_answer = generate_description(question)
                self.console.print(Panel.fit(f"[bold green]AI menjawab:[/bold green]\n{ai_answer}", style="bold green", title="[bold yellow]Jawaban AI[/bold yellow]"))
        
        elif cmd == "help":
            self.show_help()
        
        else:
            # Perintah bebas: kirim ke AI sebagai narasi petualangan dengan context
            game_context = self.state.get_context_for_ai()
            ai_narration = generate_contextual_response(
                command, 
                game_context, 
                self.state.conversation_history, 
                self.state.player_actions
            )
            self.console.print(Panel.fit(f"{ai_narration}", title="[bold cyan]Narasi Petualangan[/bold cyan]", style="cyan"))
            
            # Add to conversation history
            self.state.add_conversation(f"Player: {command} | AI: {ai_narration[:100]}...")
            
            # Check quest completion after any action
            completed_quest = self.state.check_quest_completion()
            if completed_quest:
                self.console.print(Panel.fit(f"🎉 Quest '{completed_quest.title}' selesai! Anda mendapatkan reward!", title="[bold green]Quest Selesai[/bold green]", style="bold green"))

    def main_game_loop(self):
        while not self.state.game_over:
            command = Prompt.ask("[bold cyan]\nApa yang ingin Anda lakukan?[/bold cyan]")
            self.handle_command(command)
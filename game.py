from ai_integration import generate_description, generate_puzzle, generate_npc_dialogue
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from dotenv import load_dotenv
import os

class Game:
    def __init__(self):
        self.player_name = "Pahlawan"
        self.current_location = "Hutan Misterius"
        self.inventory = []
        self.game_over = False
        self.console = Console()

    def start_game(self):
        self.console.print(Panel.fit(f"Selamat datang, [bold cyan]{self.player_name}[/bold cyan], di [bold green]{self.current_location}[/bold green]!", title="[bold yellow]Petualangan Dimulai[/bold yellow]", style="bold magenta"))
        self.describe_current_location()
        self.show_help()
        self.main_game_loop()

    def describe_current_location(self):
        prompt = f"Deskripsikan secara detail {self.current_location} dan apa yang bisa dilihat di sana."
        description = generate_description(prompt)
        self.console.print(Panel.fit(f"[bold]Anda berada di:[/bold] [green]{self.current_location}[/green]\n{description}", title="[bold blue]Lokasi[/bold blue]", style="cyan"))

    def show_help(self):
        help_text = (
            "[bold]Perintah yang bisa digunakan:[/bold]\n"
            "[yellow]lihat[/yellow]                : Melihat deskripsi lokasi saat ini\n"
            "[yellow]inventaris[/yellow]           : Melihat inventaris Anda\n"
            "[yellow]bicara dengan [npc][/yellow]  : Bicara dengan NPC tertentu (misal: bicara dengan penjaga)\n"
            "[yellow]pecahkan teka-teki[/yellow]   : Mendapatkan teka-teki dari AI\n"
            "[yellow]tanya [pertanyaan][/yellow]   : Bertanya bebas ke AI (misal: tanya siapa penemu komputer?)\n"
            "[yellow]help[/yellow]                 : Menampilkan bantuan ini\n"
            "[yellow]keluar[/yellow]               : Keluar dari permainan\n"
            "[yellow]Perintah bebas[/yellow]       : Ketik perintah apapun (misal: pergi ke gua, ambil pedang, buka pintu, dsb) dan AI akan merespons sebagai narasi petualangan!"
        )
        self.console.print(Panel.fit(help_text, title="[bold green]Bantuan[/bold green]", style="bold white"))

    def handle_command(self, command):
        command = command.strip()
        if not command:
            self.console.print("[red]Masukkan perintah yang valid.[/red]")
            return
        cmd = command.lower()
        if cmd == "keluar":
            self.game_over = True
            self.console.print(Panel.fit("Anda meninggalkan petualangan. Sampai jumpa!", style="bold red", title="[bold yellow]Keluar[/bold yellow]"))
        elif cmd == "lihat":
            self.describe_current_location()
        elif cmd == "inventaris":
            if self.inventory:
                inv = ", ".join(self.inventory)
                self.console.print(Panel.fit(f"Inventaris Anda: [cyan]{inv}[/cyan]", title="[bold green]Inventaris[/bold green]", style="white"))
            else:
                self.console.print(Panel.fit("Inventaris Anda kosong.", title="[bold green]Inventaris[/bold green]", style="white"))
        elif cmd.startswith("bicara dengan"):
            parts = command.split(" ", 2)
            if len(parts) >= 3:
                npc = parts[2].strip()
                dialog = generate_npc_dialogue(npc, f"dia sedang berada di {self.current_location}")
                self.console.print(Panel.fit(f"{npc.capitalize()} berkata: [italic yellow]'{dialog}'[/italic yellow]", title=f"[bold blue]Bicara dengan {npc.capitalize()}[/bold blue]", style="bold cyan"))
            else:
                self.console.print("[red]Format: bicara dengan [nama_npc][/red]")
        elif cmd == "pecahkan teka-teki":
            puzzle_text = generate_puzzle(f"tentang {self.current_location} dan misterinya")
            self.console.print(Panel.fit(f"Teka-teki dari misteri {self.current_location}:\n[bold yellow]{puzzle_text}[/bold yellow]", title="[bold magenta]Teka-Teki[/bold magenta]", style="magenta"))
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
            # Perintah bebas: kirim ke AI sebagai narasi petualangan
            prompt = (
                f"Kamu adalah engine game petualangan berbasis teks. Pemain berada di lokasi: {self.current_location}. "
                f"Pemain mengetik: '{command}'. Jawablah sebagai narasi game, berikan konsekuensi, deskripsi, atau aksi sesuai perintah tersebut."
            )
            ai_narration = generate_description(prompt)
            self.console.print(Panel.fit(f"{ai_narration}", title="[bold cyan]Narasi Petualangan[/bold cyan]", style="cyan"))

    def main_game_loop(self):
        while not self.game_over:
            command = Prompt.ask("[bold cyan]\nApa yang ingin Anda lakukan?[/bold cyan]")
            self.handle_command(command)
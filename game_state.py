from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from datetime import datetime

@dataclass
class Item:
    name: str
    description: str
    weight: float = 1.0
    value: int = 0
    usable: bool = False
    consumable: bool = False

@dataclass
class Location:
    name: str
    description: str
    connections: List[str] = field(default_factory=list)
    items: List[Item] = field(default_factory=list)
    npcs: List[str] = field(default_factory=list)
    visited: bool = False

@dataclass
class Quest:
    title: str
    description: str
    requirements: Dict[str, int] = field(default_factory=dict)  # item_name: count
    rewards: List[Item] = field(default_factory=list)
    completed: bool = False
    started: bool = False
    quest_id: str = ""

@dataclass
class GameState:
    player_name: str = "Pahlawan"
    current_location: str = "hutan"
    inventory: List[Item] = field(default_factory=list)
    health: int = 100
    max_health: int = 100
    level: int = 1
    experience: int = 0
    gold: int = 50
    quests: List[Quest] = field(default_factory=list)
    completed_quests: Set[str] = field(default_factory=set)
    game_start_time: datetime = field(default_factory=datetime.now)
    
    # AI Memory
    conversation_history: List[str] = field(default_factory=list)
    player_actions: List[str] = field(default_factory=list)
    
    # World state
    locations: Dict[str, Location] = field(default_factory=dict)
    
    def __post_init__(self):
        self._initialize_world()
        self._initialize_quests()
    
    def _initialize_world(self):
        """Initialize the game world with locations"""
        self.locations = {
            "hutan": Location(
                name="Hutan Misterius",
                description="Hutan lebat dengan pepohonan tinggi dan cahaya matahari yang temaram. Suara burung dan serangga terdengar di kejauhan.",
                connections=["gua", "kota", "sungai"],
                items=[Item("ranting", "Ranting pohon yang bisa digunakan untuk api unggun", 0.5, 1, True)],
                npcs=["penjaga_hutan"]
            ),
            "gua": Location(
                name="Gua Gelap",
                description="Gua dalam yang gelap dan lembab. Ada tetesan air dari stalaktit dan aroma tanah yang kuat.",
                connections=["hutan", "dalam_gua"],
                items=[Item("batu_api", "Batu yang bisa menghasilkan percikan api", 1.0, 5, True)],
                npcs=["penambang"]
            ),
            "kota": Location(
                name="Kota Ramai",
                description="Kota yang ramai dengan penduduk yang sibuk. Ada pasar, penginapan, dan berbagai toko.",
                connections=["hutan", "kastil", "pelabuhan"],
                items=[Item("koin_emas", "Koin emas yang berkilau", 0.1, 10, False)],
                npcs=["pedagang", "penjaga_kota", "penyihir"]
            ),
            "kastil": Location(
                name="Kastil Megah",
                description="Kastil besar dengan menara tinggi dan dinding batu yang kokoh. Bendera berkibar di atasnya.",
                connections=["kota"],
                items=[Item("pedang_kerajaan", "Pedang indah dengan hiasan emas", 3.0, 100, True)],
                npcs=["raja", "knight", "pelayan"]
            ),
            "sungai": Location(
                name="Sungai Jernih",
                description="Sungai yang airnya jernih dan mengalir deras. Ada jembatan kayu di atasnya.",
                connections=["hutan", "pelabuhan"],
                items=[Item("ikan_segar", "Ikan segar yang baru ditangkap", 1.0, 15, True, True)],
                npcs=["nelayan"]
            ),
            "pelabuhan": Location(
                name="Pelabuhan Sibuk",
                description="Pelabuhan dengan kapal-kapal yang berlabuh. Para pelaut sibuk bongkar muat barang.",
                connections=["kota", "sungai"],
                items=[Item("peta_laut", "Peta yang menunjukkan rute laut", 0.5, 25, True)],
                npcs=["pelaut", "kapten"]
            ),
            "dalam_gua": Location(
                name="Kedalaman Gua",
                description="Bagian terdalam dari gua. Sangat gelap dan misterius. Ada suara aneh dari kejauhan.",
                connections=["gua"],
                items=[Item("kristal_misterius", "Kristal yang berkilau dengan cahaya aneh", 2.0, 50, True)],
                npcs=["naga"]
            )
        }
    
    def _initialize_quests(self):
        """Initialize available quests"""
        self.quests = [
            Quest(
                quest_id="quest_1",
                title="Mengumpulkan Kayu",
                description="Kumpulkan 3 ranting dari hutan untuk membuat api unggun.",
                requirements={"ranting": 3},
                rewards=[Item("api_unggun", "Api unggun yang hangat", 5.0, 20, True)]
            ),
            Quest(
                quest_id="quest_2", 
                title="Mencari Batu Api",
                description="Temukan batu api di dalam gua untuk membantu membuat api.",
                requirements={"batu_api": 1},
                rewards=[Item("korek_api", "Korek api yang bisa menyalakan api", 0.1, 30, True)]
            ),
            Quest(
                quest_id="quest_3",
                title="Mengumpulkan Harta",
                description="Kumpulkan 100 koin emas untuk membeli pedang kerajaan.",
                requirements={"koin_emas": 100},
                rewards=[Item("pedang_kerajaan", "Pedang kerajaan yang kuat", 3.0, 200, True)]
            )
        ]
    
    def add_action(self, action: str):
        """Add player action to history"""
        self.player_actions.append(f"{datetime.now().strftime('%H:%M:%S')}: {action}")
        if len(self.player_actions) > 50:  # Keep only last 50 actions
            self.player_actions.pop(0)
    
    def add_conversation(self, message: str):
        """Add conversation to history"""
        self.conversation_history.append(f"{datetime.now().strftime('%H:%M:%S')}: {message}")
        if len(self.conversation_history) > 20:  # Keep only last 20 conversations
            self.conversation_history.pop(0)
    
    def move_to(self, location_name: str) -> bool:
        """Move player to a new location"""
        if location_name in self.locations:
            if location_name in self.locations[self.current_location].connections:
                self.current_location = location_name
                self.locations[location_name].visited = True
                return True
        return False
    
    def get_available_locations(self) -> List[str]:
        """Get list of locations player can move to"""
        return self.locations[self.current_location].connections
    
    def add_item_to_inventory(self, item: Item):
        """Add item to player inventory"""
        self.inventory.append(item)
    
    def remove_item_from_inventory(self, item_name: str) -> bool:
        """Remove item from inventory by name"""
        for i, item in enumerate(self.inventory):
            if item.name.lower() == item_name.lower():
                self.inventory.pop(i)
                return True
        return False
    
    def get_inventory_item(self, item_name: str) -> Optional[Item]:
        """Get item from inventory by name"""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item
        return None
    
    def has_item(self, item_name: str, count: int = 1) -> bool:
        """Check if player has specific item with required count"""
        item_count = sum(1 for item in self.inventory if item.name.lower() == item_name.lower())
        return item_count >= count
    
    def get_quest_progress(self, quest_id: str) -> Optional[Dict]:
        """Get progress of a specific quest"""
        for quest in self.quests:
            if quest.quest_id == quest_id:
                progress = {}
                for req_item, req_count in quest.requirements.items():
                    current_count = sum(1 for item in self.inventory if item.name.lower() == req_item.lower())
                    progress[req_item] = {"required": req_count, "current": current_count}
                return progress
        return None
    
    def check_quest_completion(self):
        """Check if any quests can be completed"""
        for quest in self.quests:
            if not quest.completed and quest.started:
                can_complete = True
                for req_item, req_count in quest.requirements.items():
                    if not self.has_item(req_item, req_count):
                        can_complete = False
                        break
                
                if can_complete:
                    quest.completed = True
                    self.completed_quests.add(quest.quest_id)
                    # Give rewards
                    for reward in quest.rewards:
                        self.add_item_to_inventory(reward)
                    return quest
        return None
    
    def start_quest(self, quest_id: str) -> bool:
        """Start a quest"""
        for quest in self.quests:
            if quest.quest_id == quest_id and not quest.started:
                quest.started = True
                return True
        return False
    
    def get_current_location_info(self) -> Location:
        """Get current location information"""
        return self.locations[self.current_location]
    
    def get_context_for_ai(self) -> str:
        """Get context information for AI"""
        current_loc = self.get_current_location_info()
        context = f"""
        Player: {self.player_name}
        Location: {current_loc.name} - {current_loc.description}
        Health: {self.health}/{self.max_health}
        Level: {self.level}
        Gold: {self.gold}
        Inventory: {[item.name for item in self.inventory]}
        Available locations: {self.get_available_locations()}
        Recent actions: {self.player_actions[-5:] if self.player_actions else []}
        """
        return context 
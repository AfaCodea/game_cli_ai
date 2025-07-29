from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from datetime import datetime
import json

@dataclass
class Item:
    name: str
    description: str
    weight: float = 1.0
    value: int = 0
    usable: bool = False
    consumable: bool = False
    item_type: str = "misc"  # weapon, armor, potion, tool, material, etc.
    stats: Dict[str, int] = field(default_factory=dict)
    durability: int = 100
    max_durability: int = 100
    rarity: str = "common"
    special_effects: List[str] = field(default_factory=list)

@dataclass
class Location:
    name: str
    description: str
    connections: List[str] = field(default_factory=list)
    items: List[Item] = field(default_factory=list)
    npcs: List[str] = field(default_factory=list)
    visited: bool = False
    monsters: List[str] = field(default_factory=list)  # Monster names that can spawn here
    crafting_stations: List[str] = field(default_factory=list)  # Available crafting stations
    merchants: List[str] = field(default_factory=list)  # Available merchants

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
class CombatStats:
    health: int
    max_health: int
    attack: int
    defense: int
    speed: int
    critical_chance: float = 0.1
    dodge_chance: float = 0.05
    mana: int = 0
    max_mana: int = 0

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
    game_over: bool = False
    
    # AI Memory
    conversation_history: List[str] = field(default_factory=list)
    player_actions: List[str] = field(default_factory=list)
    
    # World state
    locations: Dict[str, Location] = field(default_factory=dict)
    
    # New systems
    combat_stats: CombatStats = field(default_factory=lambda: CombatStats(100, 100, 10, 5, 8))
    crafting_materials: Dict[str, int] = field(default_factory=dict)  # material_name: quantity
    crafting_tools: List[str] = field(default_factory=list)
    crafting_skills: Dict[str, int] = field(default_factory=lambda: {
        "blacksmithing": 0,
        "alchemy": 0,
        "carpentry": 0,
        "enchanting": 0,
        "cooking": 0
    })
    merchant_reputation: Dict[str, int] = field(default_factory=dict)
    play_time: int = 0  # in seconds
    save_slots: Dict[str, str] = field(default_factory=dict)  # slot_name: save_name
    
    def __post_init__(self):
        self._initialize_world()
        self._initialize_quests()
    
    def _initialize_world(self):
        """Initialize the game world with locations, items, and NPCs"""
        # Initialize locations with enhanced features
        self.locations = {
            "hutan": Location(
                name="Hutan Misterius",
                description="Hutan yang penuh dengan misteri dan petualangan. Pepohonan tinggi menjulang dan suara burung terdengar dari kejauhan.",
                connections=["gua", "kota"],
                items=[
                    Item("ranting", "Ranting kayu yang bisa digunakan untuk berbagai keperluan", 0.5, 2, True, False, "material"),
                    Item("batu", "Batu biasa yang bisa digunakan untuk crafting", 1.0, 1, False, False, "material"),
                    Item("herbs", "Tanaman obat yang berguna untuk alchemy", 0.2, 4, False, False, "material")
                ],
                npcs=["penjaga_hutan"],
                monsters=["goblin", "wolf"],
                crafting_stations=["campfire"],
                merchants=[]
            ),
            "gua": Location(
                name="Gua Gelap",
                description="Gua yang gelap dan misterius. Suara air menetes terdengar dari dalam.",
                connections=["hutan", "kedalaman_gua"],
                items=[
                    Item("iron_ore", "Bijih besi untuk crafting", 2.0, 5, False, False, "material"),
                    Item("torch", "Obor untuk penerangan", 1.0, 8, True, False, "tool"),
                    Item("crystal", "Kristal yang berkilau", 0.5, 15, False, False, "material")
                ],
                npcs=["penambang"],
                monsters=["skeleton", "troll"],
                crafting_stations=["anvil"],
                merchants=["pedagang_gelap"]
            ),
            "kota": Location(
                name="Kota Ramai",
                description="Kota yang ramai dengan penduduk dan aktivitas perdagangan.",
                connections=["hutan", "kastil", "pelabuhan"],
                items=[
                    Item("bread", "Roti segar", 0.3, 5, True, True, "consumable"),
                    Item("water", "Air bersih", 0.5, 2, True, True, "consumable"),
                    Item("cloth", "Kain untuk crafting", 0.8, 3, False, False, "material")
                ],
                npcs=["pedagang", "penjaga_kota"],
                monsters=[],
                crafting_stations=["workbench", "cauldron"],
                merchants=["pedagang_umum", "tukang_senjata", "tukang_armor", "alkemis"]
            ),
            "kastil": Location(
                name="Kastil Megah",
                description="Kastil yang megah dengan arsitektur yang indah.",
                connections=["kota"],
                items=[
                    Item("gold_coin", "Koin emas", 0.1, 10, False, False, "currency"),
                    Item("magic_scroll", "Gulungan sihir", 0.5, 100, True, False, "magic"),
                    Item("noble_clothing", "Pakaian bangsawan", 1.0, 50, False, False, "armor")
                ],
                npcs=["raja", "penasihat"],
                monsters=[],
                crafting_stations=["enchanting_table"],
                merchants=["toko_sihir"]
            ),
            "sungai": Location(
                name="Sungai Jernih",
                description="Sungai yang airnya jernih dan mengalir dengan tenang.",
                connections=["hutan", "pelabuhan"],
                items=[
                    Item("fish", "Ikan segar", 0.5, 8, True, True, "consumable"),
                    Item("water", "Air bersih", 0.5, 2, True, True, "consumable"),
                    Item("pearl", "Mutiara yang indah", 0.3, 25, False, False, "material")
                ],
                npcs=["nelayan"],
                monsters=["river_monster"],
                crafting_stations=[],
                merchants=[]
            ),
            "pelabuhan": Location(
                name="Pelabuhan Sibuk",
                description="Pelabuhan yang sibuk dengan kapal-kapal yang berlabuh.",
                connections=["kota", "sungai"],
                items=[
                    Item("rope", "Tali yang kuat", 1.0, 12, False, False, "tool"),
                    Item("sail_cloth", "Kain layar", 2.0, 20, False, False, "material"),
                    Item("compass", "Kompas untuk navigasi", 0.5, 30, True, False, "tool")
                ],
                npcs=["pelaut", "kapten"],
                monsters=[],
                crafting_stations=["shipyard"],
                merchants=["pedagang_laut"]
            ),
            "kedalaman_gua": Location(
                name="Kedalaman Gua",
                description="Bagian terdalam dari gua yang gelap dan berbahaya.",
                connections=["gua"],
                items=[
                    Item("dragon_scale", "Sisik naga yang sangat kuat", 3.0, 200, False, False, "material"),
                    Item("magic_crystal", "Kristal ajaib", 1.0, 50, False, False, "material"),
                    Item("ancient_relic", "Relik kuno", 5.0, 500, False, False, "treasure")
                ],
                npcs=[],
                monsters=["dragon", "ancient_guardian"],
                crafting_stations=[],
                merchants=[]
            )
        }
    
    def _initialize_quests(self):
        """Initialize quests with enhanced rewards"""
        self.quests = [
            Quest(
                title="Mengumpulkan Kayu",
                description="Kumpulkan 3 ranting untuk membuat api unggun",
                requirements={"ranting": 3},
                rewards=[
                    Item("campfire", "Api unggun untuk memasak", 5.0, 20, True, False, "tool"),
                    Item("cooked_meat", "Daging yang sudah dimasak", 0.5, 15, True, True, "consumable")
                ],
                quest_id="quest_1"
            ),
            Quest(
                title="Mencari Batu Api",
                description="Temukan 1 batu api untuk membuat api",
                requirements={"flint": 1},
                rewards=[
                    Item("flint_and_steel", "Batu api dan baja", 1.0, 25, True, False, "tool"),
                    Item("torch", "Obor untuk penerangan", 1.0, 8, True, False, "tool")
                ],
                quest_id="quest_2"
            ),
            Quest(
                title="Mengumpulkan Harta",
                description="Kumpulkan 100 koin emas untuk membeli senjata",
                requirements={"gold_coin": 100},
                rewards=[
                    Item("iron_sword", "Pedang besi yang tajam", 3.0, 80, True, False, "weapon", {"attack": 15}),
                    Item("leather_armor", "Armor kulit ringan", 2.0, 45, True, False, "armor", {"defense": 5})
                ],
                quest_id="quest_3"
            ),
            Quest(
                title="Membuat Ramuan",
                description="Buat 5 health potion menggunakan alchemy",
                requirements={"health_potion": 5},
                rewards=[
                    Item("alchemy_kit", "Kit alchemy lengkap", 2.0, 100, False, False, "tool"),
                    Item("mana_potion", "Ramuan pemulih mana", 0.5, 25, True, True, "consumable")
                ],
                quest_id="quest_4"
            ),
            Quest(
                title="Mengalahkan Dragon",
                description="Kalahkan dragon di kedalaman gua",
                requirements={"dragon_defeated": 1},
                rewards=[
                    Item("dragon_sword", "Pedang legendaris dengan kekuatan naga", 5.0, 500, True, False, "weapon", {"attack": 50, "fire_damage": 10}),
                    Item("dragon_armor", "Armor dari sisik naga", 8.0, 300, True, False, "armor", {"defense": 25, "fire_resistance": 50})
                ],
                quest_id="quest_5"
            )
        ]
    
    def add_action(self, action: str):
        """Add player action to history"""
        self.player_actions.append(action)
        # Keep only last 100 actions
        if len(self.player_actions) > 100:
            self.player_actions = self.player_actions[-100:]
    
    def add_conversation(self, conversation: str):
        """Add conversation to history"""
        self.conversation_history.append(conversation)
        # Keep only last 50 conversations
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
    
    def move_to(self, location: str) -> bool:
        """Move to a new location"""
        if location in self.locations:
            current_loc = self.get_current_location_info()
            if location in current_loc.connections:
                self.current_location = location
                # Mark location as visited
                self.locations[location].visited = True
                return True
        return False
    
    def get_current_location_info(self) -> Location:
        """Get current location information"""
        return self.locations.get(self.current_location, self.locations["hutan"])
    
    def get_available_locations(self) -> List[str]:
        """Get list of available locations from current location"""
        current_loc = self.get_current_location_info()
        return current_loc.connections
    
    def add_item_to_inventory(self, item: Item):
        """Add item to inventory"""
        self.inventory.append(item)
    
    def remove_item_from_inventory(self, item_name: str) -> bool:
        """Remove item from inventory by name"""
        for i, item in enumerate(self.inventory):
            if item.name.lower() == item_name.lower():
                del self.inventory[i]
                return True
        return False
    
    def get_inventory_item(self, item_name: str) -> Optional[Item]:
        """Get item from inventory by name"""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item
        return None
    
    def add_item_to_location(self, item: Item):
        """Add item to current location"""
        current_loc = self.get_current_location_info()
        current_loc.items.append(item)
    
    def remove_item_from_location(self, item_name: str) -> bool:
        """Remove item from current location by name"""
        current_loc = self.get_current_location_info()
        for i, item in enumerate(current_loc.items):
            if item.name.lower() == item_name.lower():
                del current_loc.items[i]
                return True
        return False
    
    def start_quest(self, quest_id: str) -> bool:
        """Start a quest"""
        for quest in self.quests:
            if quest.quest_id == quest_id and not quest.started and not quest.completed:
                quest.started = True
                return True
        return False
    
    def check_quest_completion(self) -> Optional[Quest]:
        """Check if any quest is completed"""
        for quest in self.quests:
            if quest.started and not quest.completed:
                completed = True
                for item_name, required_count in quest.requirements.items():
                    # Check inventory
                    inventory_count = sum(1 for item in self.inventory if item.name.lower() == item_name.lower())
                    if inventory_count < required_count:
                        completed = False
                        break
                
                if completed:
                    quest.completed = True
                    self.completed_quests.add(quest.quest_id)
                    # Add rewards to inventory
                    for reward in quest.rewards:
                        self.add_item_to_inventory(reward)
                    return quest
        return None
    
    def get_context_for_ai(self) -> Dict:
        """Get context information for AI responses"""
        current_loc = self.get_current_location_info()
        return {
            "player_name": self.player_name,
            "current_location": self.current_location,
            "location_name": current_loc.name,
            "location_description": current_loc.description,
            "health": self.health,
            "max_health": self.max_health,
            "level": self.level,
            "experience": self.experience,
            "gold": self.gold,
            "inventory": [item.name for item in self.inventory],
            "location_items": [item.name for item in current_loc.items],
            "location_npcs": current_loc.npcs,
            "available_locations": current_loc.connections,
            "recent_actions": self.player_actions[-5:] if self.player_actions else [],
            "recent_conversations": self.conversation_history[-3:] if self.conversation_history else []
        }
    
    # New methods for enhanced systems
    
    def update_combat_stats(self, new_stats: Dict[str, int]):
        """Update combat stats"""
        for stat, value in new_stats.items():
            if hasattr(self.combat_stats, stat):
                setattr(self.combat_stats, stat, value)
    
    def add_crafting_material(self, material_name: str, quantity: int = 1):
        """Add crafting material"""
        if material_name not in self.crafting_materials:
            self.crafting_materials[material_name] = 0
        self.crafting_materials[material_name] += quantity
    
    def remove_crafting_material(self, material_name: str, quantity: int = 1) -> bool:
        """Remove crafting material"""
        if material_name in self.crafting_materials and self.crafting_materials[material_name] >= quantity:
            self.crafting_materials[material_name] -= quantity
            if self.crafting_materials[material_name] <= 0:
                del self.crafting_materials[material_name]
            return True
        return False
    
    def add_crafting_tool(self, tool_name: str):
        """Add crafting tool"""
        if tool_name not in self.crafting_tools:
            self.crafting_tools.append(tool_name)
    
    def remove_crafting_tool(self, tool_name: str) -> bool:
        """Remove crafting tool"""
        if tool_name in self.crafting_tools:
            self.crafting_tools.remove(tool_name)
            return True
        return False
    
    def improve_crafting_skill(self, skill_name: str, experience: int):
        """Improve crafting skill"""
        if skill_name in self.crafting_skills:
            self.crafting_skills[skill_name] += experience
    
    def get_crafting_skill_level(self, skill_name: str) -> int:
        """Get crafting skill level"""
        return self.crafting_skills.get(skill_name, 0)
    
    def update_merchant_reputation(self, merchant_name: str, change: int):
        """Update reputation with merchant"""
        if merchant_name not in self.merchant_reputation:
            self.merchant_reputation[merchant_name] = 50
        self.merchant_reputation[merchant_name] = max(0, min(100, self.merchant_reputation[merchant_name] + change))
    
    def get_merchant_reputation(self, merchant_name: str) -> int:
        """Get reputation with merchant"""
        return self.merchant_reputation.get(merchant_name, 50)
    
    def add_gold(self, amount: int):
        """Add gold to player"""
        self.gold += amount
    
    def remove_gold(self, amount: int) -> bool:
        """Remove gold from player"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
    
    def add_experience(self, amount: int):
        """Add experience to player"""
        self.experience += amount
        # Check for level up
        required_exp = self.level * 100
        if self.experience >= required_exp:
            self.level_up()
    
    def level_up(self):
        """Level up player"""
        self.level += 1
        self.max_health += 10
        self.health = self.max_health  # Full heal on level up
        self.combat_stats.max_health += 10
        self.combat_stats.health = self.combat_stats.max_health
        self.combat_stats.attack += 2
        self.combat_stats.defense += 1
    
    def heal(self, amount: int):
        """Heal player"""
        self.health = min(self.max_health, self.health + amount)
        self.combat_stats.health = min(self.combat_stats.max_health, self.combat_stats.health + amount)
    
    def take_damage(self, amount: int):
        """Take damage"""
        self.health = max(0, self.health - amount)
        self.combat_stats.health = max(0, self.combat_stats.health - amount)
        if self.health <= 0:
            self.game_over = True
    
    def get_play_time(self) -> int:
        """Get total play time in seconds"""
        if hasattr(self, 'game_start_time'):
            elapsed = datetime.now() - self.game_start_time
            return int(elapsed.total_seconds()) + self.play_time
        return self.play_time
    
    def save_game_state(self) -> Dict:
        """Get complete game state for saving"""
        return {
            "player_name": self.player_name,
            "current_location": self.current_location,
            "health": self.health,
            "max_health": self.max_health,
            "level": self.level,
            "experience": self.experience,
            "gold": self.gold,
            "game_over": self.game_over,
            "play_time": self.get_play_time(),
            "inventory": [self._item_to_dict(item) for item in self.inventory],
            "crafting_materials": self.crafting_materials,
            "crafting_tools": self.crafting_tools,
            "crafting_skills": self.crafting_skills,
            "merchant_reputation": self.merchant_reputation,
            "combat_stats": {
                "health": self.combat_stats.health,
                "max_health": self.combat_stats.max_health,
                "attack": self.combat_stats.attack,
                "defense": self.combat_stats.defense,
                "speed": self.combat_stats.speed,
                "critical_chance": self.combat_stats.critical_chance,
                "dodge_chance": self.combat_stats.dodge_chance,
                "mana": self.combat_stats.mana,
                "max_mana": self.combat_stats.max_mana
            },
            "locations": {
                name: {
                    "name": loc.name,
                    "description": loc.description,
                    "connections": loc.connections,
                    "visited": loc.visited,
                    "items": [self._item_to_dict(item) for item in loc.items],
                    "npcs": loc.npcs,
                    "monsters": loc.monsters,
                    "crafting_stations": loc.crafting_stations,
                    "merchants": loc.merchants
                }
                for name, loc in self.locations.items()
            },
            "quests": [
                {
                    "title": quest.title,
                    "description": quest.description,
                    "requirements": quest.requirements,
                    "rewards": [self._item_to_dict(reward) for reward in quest.rewards],
                    "completed": quest.completed,
                    "started": quest.started,
                    "quest_id": quest.quest_id
                }
                for quest in self.quests
            ],
            "completed_quests": list(self.completed_quests),
            "conversation_history": self.conversation_history,
            "player_actions": self.player_actions
        }
    
    def _item_to_dict(self, item: Item) -> Dict:
        """Convert item to dictionary"""
        return {
            "name": item.name,
            "description": item.description,
            "weight": item.weight,
            "value": item.value,
            "usable": item.usable,
            "consumable": item.consumable,
            "item_type": item.item_type,
            "stats": item.stats,
            "durability": item.durability,
            "max_durability": item.max_durability,
            "rarity": item.rarity,
            "special_effects": item.special_effects
        }
    
    def load_game_state(self, state_data: Dict):
        """Load game state from dictionary"""
        self.player_name = state_data.get("player_name", "Pahlawan")
        self.current_location = state_data.get("current_location", "hutan")
        self.health = state_data.get("health", 100)
        self.max_health = state_data.get("max_health", 100)
        self.level = state_data.get("level", 1)
        self.experience = state_data.get("experience", 0)
        self.gold = state_data.get("gold", 50)
        self.game_over = state_data.get("game_over", False)
        self.play_time = state_data.get("play_time", 0)
        
        # Load inventory
        self.inventory = []
        for item_data in state_data.get("inventory", []):
            self.inventory.append(self._dict_to_item(item_data))
        
        # Load crafting data
        self.crafting_materials = state_data.get("crafting_materials", {})
        self.crafting_tools = state_data.get("crafting_tools", [])
        self.crafting_skills = state_data.get("crafting_skills", {})
        self.merchant_reputation = state_data.get("merchant_reputation", {})
        
        # Load combat stats
        combat_data = state_data.get("combat_stats", {})
        self.combat_stats = CombatStats(
            health=combat_data.get("health", 100),
            max_health=combat_data.get("max_health", 100),
            attack=combat_data.get("attack", 10),
            defense=combat_data.get("defense", 5),
            speed=combat_data.get("speed", 8),
            critical_chance=combat_data.get("critical_chance", 0.1),
            dodge_chance=combat_data.get("dodge_chance", 0.05),
            mana=combat_data.get("mana", 0),
            max_mana=combat_data.get("max_mana", 0)
        )
        
        # Load locations
        locations_data = state_data.get("locations", {})
        for name, loc_data in locations_data.items():
            if name in self.locations:
                loc = self.locations[name]
                loc.visited = loc_data.get("visited", False)
                loc.items = [self._dict_to_item(item_data) for item_data in loc_data.get("items", [])]
                loc.npcs = loc_data.get("npcs", [])
                loc.monsters = loc_data.get("monsters", [])
                loc.crafting_stations = loc_data.get("crafting_stations", [])
                loc.merchants = loc_data.get("merchants", [])
        
        # Load quests
        quests_data = state_data.get("quests", [])
        for i, quest_data in enumerate(quests_data):
            if i < len(self.quests):
                quest = self.quests[i]
                quest.completed = quest_data.get("completed", False)
                quest.started = quest_data.get("started", False)
        
        self.completed_quests = set(state_data.get("completed_quests", []))
        self.conversation_history = state_data.get("conversation_history", [])
        self.player_actions = state_data.get("player_actions", [])
    
    def _dict_to_item(self, item_data: Dict) -> Item:
        """Convert dictionary to item"""
        return Item(
            name=item_data.get("name", ""),
            description=item_data.get("description", ""),
            weight=item_data.get("weight", 1.0),
            value=item_data.get("value", 0),
            usable=item_data.get("usable", False),
            consumable=item_data.get("consumable", False),
            item_type=item_data.get("item_type", "misc"),
            stats=item_data.get("stats", {}),
            durability=item_data.get("durability", 100),
            max_durability=item_data.get("max_durability", 100),
            rarity=item_data.get("rarity", "common"),
            special_effects=item_data.get("special_effects", [])
        ) 
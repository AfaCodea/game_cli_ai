from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class CraftingDifficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

@dataclass
class CraftingMaterial:
    name: str
    description: str
    rarity: str  # common, uncommon, rare, epic, legendary
    base_value: int
    weight: float = 1.0

@dataclass
class CraftingRecipe:
    name: str
    description: str
    materials: Dict[str, int]  # material_name: quantity
    difficulty: CraftingDifficulty
    crafting_time: int  # in seconds
    experience_gain: int
    success_rate: float
    tools_required: List[str] = field(default_factory=list)
    skill_required: Optional[str] = None
    skill_level_required: int = 0

@dataclass
class CraftedItem:
    name: str
    description: str
    item_type: str  # weapon, armor, potion, tool, etc.
    stats: Dict[str, int] = field(default_factory=dict)
    durability: int = 100
    max_durability: int = 100
    value: int = 0
    rarity: str = "common"
    special_effects: List[str] = field(default_factory=list)

class CraftingSystem:
    def __init__(self):
        self.materials = self._initialize_materials()
        self.recipes = self._initialize_recipes()
        self.crafted_items = self._initialize_crafted_items()
        self.player_crafting_skills = {
            "blacksmithing": 0,
            "alchemy": 0,
            "carpentry": 0,
            "enchanting": 0,
            "cooking": 0
        }
    
    def _initialize_materials(self) -> Dict[str, CraftingMaterial]:
        """Initialize all crafting materials"""
        return {
            # Basic materials
            "wood": CraftingMaterial("Wood", "Kayu dasar untuk crafting", "common", 2),
            "stone": CraftingMaterial("Stone", "Batu dasar untuk crafting", "common", 1),
            "iron_ore": CraftingMaterial("Iron Ore", "Bijih besi untuk membuat logam", "common", 5),
            "leather": CraftingMaterial("Leather", "Kulit hewan untuk armor", "common", 8),
            "cloth": CraftingMaterial("Cloth", "Kain untuk pakaian", "common", 3),
            
            # Intermediate materials
            "iron_ingot": CraftingMaterial("Iron Ingot", "Besi yang sudah diproses", "uncommon", 15),
            "steel_ingot": CraftingMaterial("Steel Ingot", "Baja yang kuat", "uncommon", 25),
            "magic_crystal": CraftingMaterial("Magic Crystal", "Kristal ajaib untuk enchant", "rare", 50),
            "herbs": CraftingMaterial("Herbs", "Tanaman obat untuk alchemy", "common", 4),
            
            # Advanced materials
            "dragon_scale": CraftingMaterial("Dragon Scale", "Sisik naga yang sangat kuat", "legendary", 200),
            "mithril_ore": CraftingMaterial("Mithril Ore", "Bijih mithril yang langka", "epic", 100),
            "phoenix_feather": CraftingMaterial("Phoenix Feather", "Bulu phoenix yang ajaib", "legendary", 300),
            "void_essence": CraftingMaterial("Void Essence", "Esensi dari dimensi lain", "legendary", 500)
        }
    
    def _initialize_recipes(self) -> Dict[str, CraftingRecipe]:
        """Initialize all crafting recipes"""
        return {
            # Basic weapons
            "wooden_sword": CraftingRecipe(
                name="Wooden Sword",
                description="Pedang kayu sederhana",
                materials={"wood": 3, "leather": 1},
                difficulty=CraftingDifficulty.EASY,
                crafting_time=30,
                experience_gain=10,
                success_rate=0.9,
                tools_required=["knife"],
                skill_required="carpentry",
                skill_level_required=0
            ),
            "iron_sword": CraftingRecipe(
                name="Iron Sword",
                description="Pedang besi yang tajam",
                materials={"iron_ingot": 2, "wood": 1, "leather": 1},
                difficulty=CraftingDifficulty.MEDIUM,
                crafting_time=120,
                experience_gain=25,
                success_rate=0.8,
                tools_required=["hammer", "anvil"],
                skill_required="blacksmithing",
                skill_level_required=1
            ),
            "steel_sword": CraftingRecipe(
                name="Steel Sword",
                description="Pedang baja yang sangat kuat",
                materials={"steel_ingot": 3, "iron_ingot": 1, "leather": 2},
                difficulty=CraftingDifficulty.HARD,
                crafting_time=300,
                experience_gain=50,
                success_rate=0.7,
                tools_required=["hammer", "anvil", "forge"],
                skill_required="blacksmithing",
                skill_level_required=3
            ),
            
            # Armor
            "leather_armor": CraftingRecipe(
                name="Leather Armor",
                description="Armor kulit yang ringan",
                materials={"leather": 4, "cloth": 2},
                difficulty=CraftingDifficulty.EASY,
                crafting_time=60,
                experience_gain=15,
                success_rate=0.85,
                tools_required=["needle"],
                skill_required="carpentry",
                skill_level_required=0
            ),
            "iron_armor": CraftingRecipe(
                name="Iron Armor",
                description="Armor besi yang kuat",
                materials={"iron_ingot": 4, "leather": 2},
                difficulty=CraftingDifficulty.MEDIUM,
                crafting_time=180,
                experience_gain=35,
                success_rate=0.75,
                tools_required=["hammer", "anvil"],
                skill_required="blacksmithing",
                skill_level_required=2
            ),
            
            # Potions
            "health_potion": CraftingRecipe(
                name="Health Potion",
                description="Ramuan untuk menyembuhkan luka",
                materials={"herbs": 2, "water": 1},
                difficulty=CraftingDifficulty.EASY,
                crafting_time=45,
                experience_gain=12,
                success_rate=0.9,
                tools_required=["cauldron"],
                skill_required="alchemy",
                skill_level_required=0
            ),
            "mana_potion": CraftingRecipe(
                name="Mana Potion",
                description="Ramuan untuk memulihkan mana",
                materials={"herbs": 3, "magic_crystal": 1, "water": 1},
                difficulty=CraftingDifficulty.MEDIUM,
                crafting_time=90,
                experience_gain=20,
                success_rate=0.8,
                tools_required=["cauldron"],
                skill_required="alchemy",
                skill_level_required=1
            ),
            
            # Tools
            "hammer": CraftingRecipe(
                name="Hammer",
                description="Palu untuk blacksmithing",
                materials={"iron_ingot": 1, "wood": 1},
                difficulty=CraftingDifficulty.EASY,
                crafting_time=60,
                experience_gain=10,
                success_rate=0.9,
                tools_required=["anvil"],
                skill_required="blacksmithing",
                skill_level_required=0
            ),
            "anvil": CraftingRecipe(
                name="Anvil",
                description="Landasan untuk blacksmithing",
                materials={"iron_ingot": 5, "stone": 3},
                difficulty=CraftingDifficulty.MEDIUM,
                crafting_time=240,
                experience_gain=30,
                success_rate=0.8,
                skill_required="blacksmithing",
                skill_level_required=1
            ),
            
            # Legendary items
            "dragon_sword": CraftingRecipe(
                name="Dragon Sword",
                description="Pedang legendaris dengan kekuatan naga",
                materials={"dragon_scale": 2, "steel_ingot": 3, "phoenix_feather": 1},
                difficulty=CraftingDifficulty.EXPERT,
                crafting_time=600,
                experience_gain=100,
                success_rate=0.5,
                tools_required=["hammer", "anvil", "forge", "enchanting_table"],
                skill_required="blacksmithing",
                skill_level_required=5
            ),
            "void_potion": CraftingRecipe(
                name="Void Potion",
                description="Ramuan yang membuka portal ke dimensi lain",
                materials={"void_essence": 1, "magic_crystal": 3, "phoenix_feather": 1},
                difficulty=CraftingDifficulty.EXPERT,
                crafting_time=480,
                experience_gain=80,
                success_rate=0.4,
                tools_required=["cauldron", "enchanting_table"],
                skill_required="alchemy",
                skill_level_required=5
            )
        }
    
    def _initialize_crafted_items(self) -> Dict[str, CraftedItem]:
        """Initialize all crafted items with their stats"""
        return {
            "wooden_sword": CraftedItem(
                name="Wooden Sword",
                description="Pedang kayu sederhana",
                item_type="weapon",
                stats={"attack": 8, "durability": 50},
                value=15,
                rarity="common"
            ),
            "iron_sword": CraftedItem(
                name="Iron Sword",
                description="Pedang besi yang tajam",
                item_type="weapon",
                stats={"attack": 15, "durability": 100},
                value=35,
                rarity="uncommon"
            ),
            "steel_sword": CraftedItem(
                name="Steel Sword",
                description="Pedang baja yang sangat kuat",
                item_type="weapon",
                stats={"attack": 25, "durability": 150},
                value=75,
                rarity="rare"
            ),
            "leather_armor": CraftedItem(
                name="Leather Armor",
                description="Armor kulit yang ringan",
                item_type="armor",
                stats={"defense": 5, "speed": 2},
                value=20,
                rarity="common"
            ),
            "iron_armor": CraftedItem(
                name="Iron Armor",
                description="Armor besi yang kuat",
                item_type="armor",
                stats={"defense": 12, "speed": -1},
                value=50,
                rarity="uncommon"
            ),
            "health_potion": CraftedItem(
                name="Health Potion",
                description="Ramuan untuk menyembuhkan luka",
                item_type="consumable",
                stats={"heal": 30},
                value=10,
                rarity="common",
                special_effects=["instant_heal"]
            ),
            "mana_potion": CraftedItem(
                name="Mana Potion",
                description="Ramuan untuk memulihkan mana",
                item_type="consumable",
                stats={"mana_restore": 25},
                value=15,
                rarity="uncommon",
                special_effects=["instant_mana"]
            ),
            "dragon_sword": CraftedItem(
                name="Dragon Sword",
                description="Pedang legendaris dengan kekuatan naga",
                item_type="weapon",
                stats={"attack": 50, "durability": 300, "fire_damage": 10},
                value=500,
                rarity="legendary",
                special_effects=["fire_aura", "dragon_fear"]
            ),
            "void_potion": CraftedItem(
                name="Void Potion",
                description="Ramuan yang membuka portal ke dimensi lain",
                item_type="consumable",
                stats={"teleport": 1},
                value=200,
                rarity="legendary",
                special_effects=["dimensional_travel", "void_protection"]
            )
        }
    
    def get_available_recipes(self, player_inventory: Dict[str, int], player_tools: List[str]) -> List[Dict]:
        """Get list of recipes that player can craft"""
        available = []
        
        for recipe_name, recipe in self.recipes.items():
            # Check if player has required skill level
            if recipe.skill_required:
                if self.player_crafting_skills.get(recipe.skill_required, 0) < recipe.skill_level_required:
                    continue
            
            # Check if player has required tools
            if recipe.tools_required:
                if not all(tool in player_tools for tool in recipe.tools_required):
                    continue
            
            # Check if player has required materials
            can_craft = True
            missing_materials = []
            
            for material, quantity in recipe.materials.items():
                if player_inventory.get(material, 0) < quantity:
                    can_craft = False
                    missing_materials.append(f"{material} (need {quantity}, have {player_inventory.get(material, 0)})")
            
            if can_craft:
                available.append({
                    "name": recipe_name,
                    "recipe": recipe,
                    "crafted_item": self.crafted_items.get(recipe_name),
                    "status": "available"
                })
            else:
                available.append({
                    "name": recipe_name,
                    "recipe": recipe,
                    "crafted_item": self.crafted_items.get(recipe_name),
                    "status": "missing_materials",
                    "missing_materials": missing_materials
                })
        
        return available
    
    def craft_item(self, recipe_name: str, player_inventory: Dict[str, int], player_tools: List[str]) -> Dict:
        """Craft an item using a recipe"""
        if recipe_name not in self.recipes:
            return {"success": False, "error": f"Recipe '{recipe_name}' tidak ditemukan"}
        
        recipe = self.recipes[recipe_name]
        
        # Check skill requirement
        if recipe.skill_required:
            if self.player_crafting_skills.get(recipe.skill_required, 0) < recipe.skill_level_required:
                return {
                    "success": False, 
                    "error": f"Memerlukan skill {recipe.skill_required} level {recipe.skill_level_required}"
                }
        
        # Check tools requirement
        if recipe.tools_required:
            missing_tools = [tool for tool in recipe.tools_required if tool not in player_tools]
            if missing_tools:
                return {
                    "success": False,
                    "error": f"Memerlukan tools: {', '.join(missing_tools)}"
                }
        
        # Check materials
        for material, quantity in recipe.materials.items():
            if player_inventory.get(material, 0) < quantity:
                return {
                    "success": False,
                    "error": f"Kurang material: {material} (need {quantity}, have {player_inventory.get(material, 0)})"
                }
        
        # Consume materials
        for material, quantity in recipe.materials.items():
            player_inventory[material] -= quantity
        
        # Calculate success chance based on skill level
        skill_level = self.player_crafting_skills.get(recipe.skill_required, 0) if recipe.skill_required else 0
        skill_bonus = skill_level * 0.05  # 5% bonus per skill level
        final_success_rate = min(0.95, recipe.success_rate + skill_bonus)
        
        import random
        if random.random() > final_success_rate:
            # Crafting failed
            return {
                "success": False,
                "error": "Crafting gagal! Materials hilang.",
                "materials_lost": recipe.materials
            }
        
        # Crafting successful
        crafted_item = self.crafted_items.get(recipe_name)
        if not crafted_item:
            return {"success": False, "error": "Item tidak ditemukan dalam database"}
        
        # Gain experience
        if recipe.skill_required:
            self.player_crafting_skills[recipe.skill_required] += recipe.experience_gain
        
        return {
            "success": True,
            "crafted_item": crafted_item,
            "experience_gained": recipe.experience_gain,
            "skill_improved": recipe.skill_required,
            "crafting_time": recipe.crafting_time
        }
    
    def get_crafting_skills(self) -> Dict[str, int]:
        """Get player's crafting skills"""
        return self.player_crafting_skills.copy()
    
    def improve_skill(self, skill_name: str, experience: int):
        """Improve a crafting skill"""
        if skill_name in self.player_crafting_skills:
            self.player_crafting_skills[skill_name] += experience
    
    def get_materials_info(self) -> List[Dict]:
        """Get information about all materials"""
        return [
            {
                "name": material.name,
                "description": material.description,
                "rarity": material.rarity,
                "value": material.base_value,
                "weight": material.weight
            }
            for material in self.materials.values()
        ]
    
    def get_recipe_info(self, recipe_name: str) -> Optional[Dict]:
        """Get detailed information about a recipe"""
        if recipe_name not in self.recipes:
            return None
        
        recipe = self.recipes[recipe_name]
        crafted_item = self.crafted_items.get(recipe_name)
        
        return {
            "name": recipe.name,
            "description": recipe.description,
            "materials": recipe.materials,
            "difficulty": recipe.difficulty.value,
            "crafting_time": recipe.crafting_time,
            "experience_gain": recipe.experience_gain,
            "success_rate": recipe.success_rate,
            "tools_required": recipe.tools_required,
            "skill_required": recipe.skill_required,
            "skill_level_required": recipe.skill_level_required,
            "crafted_item": crafted_item
        } 
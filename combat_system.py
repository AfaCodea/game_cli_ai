import random
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class CombatState(Enum):
    IDLE = "idle"
    IN_COMBAT = "in_combat"
    VICTORY = "victory"
    DEFEAT = "defeat"
    ESCAPED = "escaped"

@dataclass
class CombatStats:
    health: int
    max_health: int
    attack: int
    defense: int
    speed: int
    critical_chance: float = 0.1
    dodge_chance: float = 0.05

@dataclass
class Monster:
    name: str
    description: str
    stats: CombatStats
    level: int
    experience_reward: int
    gold_reward: int
    item_drops: List[str]
    special_abilities: List[str]
    weakness: Optional[str] = None
    resistance: Optional[str] = None

@dataclass
class CombatAction:
    name: str
    description: str
    damage: int
    accuracy: float
    cooldown: int = 0
    current_cooldown: int = 0
    special_effect: Optional[str] = None

class CombatSystem:
    def __init__(self):
        self.combat_state = CombatState.IDLE
        self.player_stats = None
        self.enemy = None
        self.turn_count = 0
        self.combat_log = []
        
        # Initialize monsters
        self.monsters = self._initialize_monsters()
        self.combat_actions = self._initialize_combat_actions()
    
    def _initialize_monsters(self) -> Dict[str, Monster]:
        """Initialize all monsters in the game"""
        return {
            "goblin": Monster(
                name="Goblin",
                description="Goblin kecil yang licik dengan senjata tajam",
                stats=CombatStats(health=30, max_health=30, attack=8, defense=3, speed=12),
                level=1,
                experience_reward=15,
                gold_reward=10,
                item_drops=["dagger", "leather_armor"],
                special_abilities=["stealth_attack"],
                weakness="fire"
            ),
            "orc": Monster(
                name="Orc",
                description="Orc besar dan kuat dengan kapak perang",
                stats=CombatStats(health=60, max_health=60, attack=15, defense=8, speed=6),
                level=3,
                experience_reward=35,
                gold_reward=25,
                item_drops=["battle_axe", "chain_mail"],
                special_abilities=["berserker_rage"],
                weakness="lightning"
            ),
            "dragon": Monster(
                name="Dragon",
                description="Naga merah yang mengerikan dengan nafas api",
                stats=CombatStats(health=200, max_health=200, attack=25, defense=15, speed=10, critical_chance=0.2),
                level=10,
                experience_reward=200,
                gold_reward=150,
                item_drops=["dragon_scale", "fire_sword"],
                special_abilities=["fire_breath", "wing_buffet"],
                weakness="ice",
                resistance="fire"
            ),
            "skeleton": Monster(
                name="Skeleton Warrior",
                description="Tentara tulang yang bangkit dari kubur",
                stats=CombatStats(health=40, max_health=40, attack=12, defense=5, speed=8),
                level=2,
                experience_reward=25,
                gold_reward=15,
                item_drops=["bone_sword", "skeleton_key"],
                special_abilities=["bone_shield"],
                weakness="holy"
            ),
            "troll": Monster(
                name="Troll",
                description="Troll besar dengan regenerasi yang cepat",
                stats=CombatStats(health=80, max_health=80, attack=18, defense=12, speed=4),
                level=5,
                experience_reward=50,
                gold_reward=40,
                item_drops=["troll_club", "regeneration_potion"],
                special_abilities=["regeneration"],
                weakness="fire"
            )
        }
    
    def _initialize_combat_actions(self) -> Dict[str, CombatAction]:
        """Initialize all combat actions"""
        return {
            "attack": CombatAction(
                name="Attack",
                description="Serangan dasar dengan senjata",
                damage=10,
                accuracy=0.85
            ),
            "strong_attack": CombatAction(
                name="Strong Attack",
                description="Serangan kuat dengan akurasi rendah",
                damage=20,
                accuracy=0.65,
                cooldown=2
            ),
            "defend": CombatAction(
                name="Defend",
                description="Bertahan untuk mengurangi kerusakan",
                damage=0,
                accuracy=1.0,
                special_effect="defense_boost"
            ),
            "fireball": CombatAction(
                name="Fireball",
                description="Melempar bola api",
                damage=25,
                accuracy=0.75,
                cooldown=3
            ),
            "heal": CombatAction(
                name="Heal",
                description="Menyembuhkan diri sendiri",
                damage=-20,
                accuracy=1.0,
                cooldown=4
            ),
            "critical_strike": CombatAction(
                name="Critical Strike",
                description="Serangan dengan peluang critical tinggi",
                damage=15,
                accuracy=0.70,
                cooldown=3,
                special_effect="high_critical"
            )
        }
    
    def start_combat(self, player_stats: CombatStats, enemy_name: str) -> Dict:
        """Start a combat encounter"""
        if enemy_name not in self.monsters:
            return {"success": False, "error": f"Monster '{enemy_name}' tidak ditemukan"}
        
        self.player_stats = player_stats
        self.enemy = self.monsters[enemy_name]
        self.combat_state = CombatState.IN_COMBAT
        self.turn_count = 0
        self.combat_log = []
        
        # Reset cooldowns
        for action in self.combat_actions.values():
            action.current_cooldown = 0
        
        self.combat_log.append(f"🎯 Pertarungan dimulai! Anda melawan {self.enemy.name}!")
        
        return {
            "success": True,
            "enemy": self.enemy,
            "combat_log": self.combat_log,
            "available_actions": self._get_available_actions()
        }
    
    def _get_available_actions(self) -> List[Dict]:
        """Get list of available combat actions"""
        available = []
        for action_name, action in self.combat_actions.items():
            if action.current_cooldown <= 0:
                available.append({
                    "name": action_name,
                    "display_name": action.name,
                    "description": action.description,
                    "damage": action.damage,
                    "accuracy": action.accuracy
                })
        return available
    
    def execute_action(self, action_name: str) -> Dict:
        """Execute a combat action"""
        if self.combat_state != CombatState.IN_COMBAT:
            return {"success": False, "error": "Tidak sedang dalam pertarungan"}
        
        if action_name not in self.combat_actions:
            return {"success": False, "error": f"Aksi '{action_name}' tidak valid"}
        
        action = self.combat_actions[action_name]
        
        if action.current_cooldown > 0:
            return {"success": False, "error": f"{action.name} masih dalam cooldown ({action.current_cooldown} turn)"}
        
        # Execute player action
        result = self._execute_player_action(action)
        
        # Check if combat is over
        if self.enemy.stats.health <= 0:
            return self._end_combat_victory()
        
        # Enemy turn
        enemy_result = self._execute_enemy_turn()
        
        # Check if player is defeated
        if self.player_stats.health <= 0:
            return self._end_combat_defeat()
        
        # Update cooldowns
        self._update_cooldowns()
        
        return {
            "success": True,
            "player_action": result,
            "enemy_action": enemy_result,
            "combat_log": self.combat_log,
            "available_actions": self._get_available_actions(),
            "player_health": self.player_stats.health,
            "enemy_health": self.enemy.stats.health
        }
    
    def _execute_player_action(self, action: CombatAction) -> Dict:
        """Execute player's combat action"""
        # Check accuracy
        if random.random() > action.accuracy:
            self.combat_log.append(f"❌ {action.name} meleset!")
            return {"type": "miss", "message": f"{action.name} meleset!"}
        
        # Calculate damage
        base_damage = action.damage
        
        # Apply special effects
        if action.special_effect == "high_critical":
            if random.random() < 0.4:  # 40% critical chance
                base_damage *= 2
                self.combat_log.append(f"💥 CRITICAL HIT! {action.name}!")
        
        # Apply defense
        final_damage = max(1, base_damage - self.enemy.stats.defense)
        
        # Apply damage
        if action.damage < 0:  # Healing
            heal_amount = abs(action.damage)
            self.player_stats.health = min(self.player_stats.max_health, self.player_stats.health + heal_amount)
            self.combat_log.append(f"💚 Anda menyembuhkan {heal_amount} HP!")
        else:
            self.enemy.stats.health -= final_damage
            self.combat_log.append(f"⚔️ {action.name} menyerang {self.enemy.name} untuk {final_damage} kerusakan!")
        
        # Set cooldown
        action.current_cooldown = action.cooldown
        
        return {
            "type": "attack" if action.damage >= 0 else "heal",
            "damage": final_damage,
            "message": f"{action.name} berhasil!"
        }
    
    def _execute_enemy_turn(self) -> Dict:
        """Execute enemy's turn"""
        # Simple AI: choose random action
        actions = ["attack", "strong_attack"]
        if self.enemy.stats.health < self.enemy.stats.max_health * 0.3:  # Low health
            actions.append("defend")
        
        enemy_action = random.choice(actions)
        
        # Calculate enemy damage
        base_damage = self.enemy.stats.attack
        if enemy_action == "strong_attack":
            base_damage = int(base_damage * 1.5)
        
        # Apply player defense
        final_damage = max(1, base_damage - self.player_stats.defense)
        
        # Check dodge
        if random.random() < self.player_stats.dodge_chance:
            self.combat_log.append(f"🛡️ Anda berhasil menghindari serangan {self.enemy.name}!")
            return {"type": "dodge", "message": "Serangan dihindari!"}
        
        # Apply damage
        self.player_stats.health -= final_damage
        self.combat_log.append(f"💥 {self.enemy.name} menyerang Anda untuk {final_damage} kerusakan!")
        
        return {
            "type": "attack",
            "damage": final_damage,
            "message": f"{self.enemy.name} menyerang!"
        }
    
    def _update_cooldowns(self):
        """Update cooldowns for all actions"""
        for action in self.combat_actions.values():
            if action.current_cooldown > 0:
                action.current_cooldown -= 1
    
    def _end_combat_victory(self) -> Dict:
        """End combat with victory"""
        self.combat_state = CombatState.VICTORY
        self.combat_log.append(f"🎉 Anda mengalahkan {self.enemy.name}!")
        self.combat_log.append(f"💰 Mendapatkan {self.enemy.gold_reward} gold dan {self.enemy.experience_reward} experience!")
        
        # Random item drop
        if self.enemy.item_drops and random.random() < 0.7:  # 70% chance
            dropped_item = random.choice(self.enemy.item_drops)
            self.combat_log.append(f"📦 {self.enemy.name} menjatuhkan {dropped_item}!")
        
        return {
            "success": True,
            "result": "victory",
            "combat_log": self.combat_log,
            "rewards": {
                "gold": self.enemy.gold_reward,
                "experience": self.enemy.experience_reward,
                "items": self.enemy.item_drops if random.random() < 0.7 else []
            }
        }
    
    def _end_combat_defeat(self) -> Dict:
        """End combat with defeat"""
        self.combat_state = CombatState.DEFEAT
        self.combat_log.append(f"💀 Anda dikalahkan oleh {self.enemy.name}!")
        self.combat_log.append("🏥 Anda kehilangan beberapa gold dan experience...")
        
        return {
            "success": True,
            "result": "defeat",
            "combat_log": self.combat_log,
            "penalties": {
                "gold_lost": max(5, self.player_stats.gold // 10),
                "experience_lost": max(5, self.player_stats.experience // 20)
            }
        }
    
    def escape_combat(self) -> Dict:
        """Try to escape from combat"""
        if self.combat_state != CombatState.IN_COMBAT:
            return {"success": False, "error": "Tidak sedang dalam pertarungan"}
        
        # 60% chance to escape
        if random.random() < 0.6:
            self.combat_state = CombatState.ESCAPED
            self.combat_log.append("🏃 Anda berhasil melarikan diri!")
            
            return {
                "success": True,
                "result": "escaped",
                "combat_log": self.combat_log
            }
        else:
            self.combat_log.append("❌ Gagal melarikan diri!")
            
            # Enemy gets a free attack
            enemy_result = self._execute_enemy_turn()
            
            if self.player_stats.health <= 0:
                return self._end_combat_defeat()
            
            return {
                "success": True,
                "result": "escape_failed",
                "combat_log": self.combat_log,
                "enemy_action": enemy_result
            }
    
    def get_combat_status(self) -> Dict:
        """Get current combat status"""
        if self.combat_state == CombatState.IDLE:
            return {"in_combat": False}
        
        return {
            "in_combat": True,
            "state": self.combat_state.value,
            "enemy": self.enemy,
            "player_health": self.player_stats.health,
            "enemy_health": self.enemy.stats.health,
            "turn_count": self.turn_count,
            "available_actions": self._get_available_actions(),
            "combat_log": self.combat_log[-5:]  # Last 5 entries
        } 
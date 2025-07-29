import json
import pickle
import os
import base64
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import zlib

@dataclass
class SaveMetadata:
    save_name: str
    player_name: str
    level: int
    location: str
    play_time: int  # in seconds
    save_date: str
    game_version: str
    checksum: str

class SaveLoadSystem:
    def __init__(self, save_directory: str = "saves"):
        self.save_directory = save_directory
        self.game_version = "1.0.0"
        self.encryption_key = "GameAI_Petualangan_Secret_Key_2024"
        
        # Create save directory if it doesn't exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
    
    def _generate_checksum(self, data: str) -> str:
        """Generate checksum for data integrity"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _encrypt_data(self, data: str) -> str:
        """Simple encryption for save data"""
        # Convert to bytes and compress
        data_bytes = data.encode('utf-8')
        compressed = zlib.compress(data_bytes)
        
        # Simple XOR encryption with key
        key_bytes = self.encryption_key.encode('utf-8')
        encrypted = bytearray()
        
        for i, byte in enumerate(compressed):
            key_byte = key_bytes[i % len(key_bytes)]
            encrypted.append(byte ^ key_byte)
        
        # Encode to base64
        return base64.b64encode(bytes(encrypted)).decode('utf-8')
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt save data"""
        try:
            # Decode from base64
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            
            # XOR decryption
            key_bytes = self.encryption_key.encode('utf-8')
            decrypted = bytearray()
            
            for i, byte in enumerate(encrypted_bytes):
                key_byte = key_bytes[i % len(key_bytes)]
                decrypted.append(byte ^ key_byte)
            
            # Decompress
            decompressed = zlib.decompress(bytes(decrypted))
            return decompressed.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to decrypt save data: {e}")
    
    def save_game(self, game_state, save_name: str = None) -> Dict:
        """Save game state to file"""
        try:
            # Generate save name if not provided
            if not save_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_name = f"save_{timestamp}"
            
            # Prepare save data
            save_data = {
                "game_state": self._serialize_game_state(game_state),
                "save_metadata": {
                    "save_name": save_name,
                    "player_name": game_state.player_name,
                    "level": game_state.level,
                    "location": game_state.current_location,
                    "play_time": getattr(game_state, 'play_time', 0),
                    "save_date": datetime.now().isoformat(),
                    "game_version": self.game_version
                }
            }
            
            # Convert to JSON
            json_data = json.dumps(save_data, indent=2)
            
            # Generate checksum
            checksum = self._generate_checksum(json_data)
            save_data["save_metadata"]["checksum"] = checksum
            
            # Encrypt data
            encrypted_data = self._encrypt_data(json.dumps(save_data, indent=2))
            
            # Save to file
            save_file = os.path.join(self.save_directory, f"{save_name}.save")
            with open(save_file, 'w') as f:
                f.write(encrypted_data)
            
            return {
                "success": True,
                "save_name": save_name,
                "file_path": save_file,
                "message": f"Game berhasil disimpan sebagai '{save_name}'"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Gagal menyimpan game: {str(e)}"
            }
    
    def load_game(self, save_name: str) -> Dict:
        """Load game state from file"""
        try:
            save_file = os.path.join(self.save_directory, f"{save_name}.save")
            
            if not os.path.exists(save_file):
                return {
                    "success": False,
                    "error": f"Save file '{save_name}' tidak ditemukan"
                }
            
            # Read encrypted data
            with open(save_file, 'r') as f:
                encrypted_data = f.read()
            
            # Decrypt data
            json_data = self._decrypt_data(encrypted_data)
            save_data = json.loads(json_data)
            
            # Verify checksum
            metadata = save_data["save_metadata"]
            expected_checksum = metadata["checksum"]
            
            # Recreate data without checksum for verification
            verify_data = save_data.copy()
            verify_data["save_metadata"] = metadata.copy()
            del verify_data["save_metadata"]["checksum"]
            
            actual_checksum = self._generate_checksum(json.dumps(verify_data, indent=2))
            
            if actual_checksum != expected_checksum:
                return {
                    "success": False,
                    "error": "Save file corrupted or tampered with"
                }
            
            # Check game version compatibility
            if metadata["game_version"] != self.game_version:
                return {
                    "success": False,
                    "error": f"Save file version {metadata['game_version']} tidak kompatibel dengan game version {self.game_version}"
                }
            
            # Deserialize game state
            game_state = self._deserialize_game_state(save_data["game_state"])
            
            return {
                "success": True,
                "game_state": game_state,
                "metadata": metadata,
                "message": f"Game berhasil dimuat dari '{save_name}'"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Gagal memuat game: {str(e)}"
            }
    
    def _serialize_game_state(self, game_state) -> Dict:
        """Serialize game state to dictionary"""
        # Basic game state data
        serialized = {
            "player_name": game_state.player_name,
            "current_location": game_state.current_location,
            "health": game_state.health,
            "max_health": game_state.max_health,
            "level": game_state.level,
            "experience": game_state.experience,
            "gold": game_state.gold,
            "game_start_time": game_state.game_start_time.isoformat() if hasattr(game_state, 'game_start_time') else None,
            "game_over": game_state.game_over,
            "conversation_history": game_state.conversation_history,
            "player_actions": game_state.player_actions,
            "completed_quests": list(game_state.completed_quests),
            
            # Inventory
            "inventory": [
                {
                    "name": item.name,
                    "description": item.description,
                    "weight": item.weight,
                    "value": item.value,
                    "usable": item.usable,
                    "consumable": item.consumable
                }
                for item in game_state.inventory
            ],
            
            # Quests
            "quests": [
                {
                    "title": quest.title,
                    "description": quest.description,
                    "requirements": quest.requirements,
                    "rewards": [
                        {
                            "name": reward.name,
                            "description": reward.description,
                            "weight": reward.weight,
                            "value": reward.value
                        }
                        for reward in quest.rewards
                    ],
                    "completed": quest.completed,
                    "started": quest.started,
                    "quest_id": quest.quest_id
                }
                for quest in game_state.quests
            ],
            
            # Locations
            "locations": {}
        }
        
        # Serialize locations
        for loc_name, location in game_state.locations.items():
            serialized["locations"][loc_name] = {
                "name": location.name,
                "description": location.description,
                "connections": location.connections,
                "visited": location.visited,
                "items": [
                    {
                        "name": item.name,
                        "description": item.description,
                        "weight": item.weight,
                        "value": item.value,
                        "usable": item.usable,
                        "consumable": item.consumable
                    }
                    for item in location.items
                ],
                "npcs": location.npcs
            }
        
        return serialized
    
    def _deserialize_game_state(self, serialized_data: Dict):
        """Deserialize dictionary back to game state"""
        from game_state import GameState, Item, Location, Quest
        
        # Create new game state
        game_state = GameState()
        
        # Restore basic properties
        game_state.player_name = serialized_data["player_name"]
        game_state.current_location = serialized_data["current_location"]
        game_state.health = serialized_data["health"]
        game_state.max_health = serialized_data["max_health"]
        game_state.level = serialized_data["level"]
        game_state.experience = serialized_data["experience"]
        game_state.gold = serialized_data["gold"]
        game_state.game_over = serialized_data["game_over"]
        game_state.conversation_history = serialized_data["conversation_history"]
        game_state.player_actions = serialized_data["player_actions"]
        game_state.completed_quests = set(serialized_data["completed_quests"])
        
        # Restore inventory
        game_state.inventory = []
        for item_data in serialized_data["inventory"]:
            item = Item(
                name=item_data["name"],
                description=item_data["description"],
                weight=item_data["weight"],
                value=item_data["value"],
                usable=item_data["usable"],
                consumable=item_data["consumable"]
            )
            game_state.inventory.append(item)
        
        # Restore quests
        game_state.quests = []
        for quest_data in serialized_data["quests"]:
            rewards = []
            for reward_data in quest_data["rewards"]:
                reward = Item(
                    name=reward_data["name"],
                    description=reward_data["description"],
                    weight=reward_data["weight"],
                    value=reward_data["value"]
                )
                rewards.append(reward)
            
            quest = Quest(
                title=quest_data["title"],
                description=quest_data["description"],
                requirements=quest_data["requirements"],
                rewards=rewards,
                completed=quest_data["completed"],
                started=quest_data["started"],
                quest_id=quest_data["quest_id"]
            )
            game_state.quests.append(quest)
        
        # Restore locations
        game_state.locations = {}
        for loc_name, loc_data in serialized_data["locations"].items():
            items = []
            for item_data in loc_data["items"]:
                item = Item(
                    name=item_data["name"],
                    description=item_data["description"],
                    weight=item_data["weight"],
                    value=item_data["value"],
                    usable=item_data["usable"],
                    consumable=item_data["consumable"]
                )
                items.append(item)
            
            location = Location(
                name=loc_data["name"],
                description=loc_data["description"],
                connections=loc_data["connections"],
                items=items,
                npcs=loc_data["npcs"],
                visited=loc_data["visited"]
            )
            game_state.locations[loc_name] = location
        
        return game_state
    
    def get_save_files(self) -> List[Dict]:
        """Get list of all save files"""
        save_files = []
        
        if not os.path.exists(self.save_directory):
            return save_files
        
        for filename in os.listdir(self.save_directory):
            if filename.endswith('.save'):
                save_name = filename[:-5]  # Remove .save extension
                file_path = os.path.join(self.save_directory, filename)
                
                try:
                    # Try to read metadata
                    with open(file_path, 'r') as f:
                        encrypted_data = f.read()
                    
                    json_data = self._decrypt_data(encrypted_data)
                    save_data = json.loads(json_data)
                    metadata = save_data["save_metadata"]
                    
                    save_files.append({
                        "save_name": save_name,
                        "file_path": file_path,
                        "metadata": metadata,
                        "file_size": os.path.getsize(file_path),
                        "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                    })
                    
                except Exception as e:
                    # Corrupted save file
                    save_files.append({
                        "save_name": save_name,
                        "file_path": file_path,
                        "error": f"Corrupted save file: {str(e)}",
                        "file_size": os.path.getsize(file_path),
                        "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                    })
        
        # Sort by last modified date (newest first)
        save_files.sort(key=lambda x: x.get("last_modified", ""), reverse=True)
        
        return save_files
    
    def delete_save(self, save_name: str) -> Dict:
        """Delete a save file"""
        try:
            save_file = os.path.join(self.save_directory, f"{save_name}.save")
            
            if not os.path.exists(save_file):
                return {
                    "success": False,
                    "error": f"Save file '{save_name}' tidak ditemukan"
                }
            
            os.remove(save_file)
            
            return {
                "success": True,
                "message": f"Save file '{save_name}' berhasil dihapus"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Gagal menghapus save file: {str(e)}"
            }
    
    def export_save(self, save_name: str, export_path: str) -> Dict:
        """Export save file to external location"""
        try:
            save_file = os.path.join(self.save_directory, f"{save_name}.save")
            
            if not os.path.exists(save_file):
                return {
                    "success": False,
                    "error": f"Save file '{save_name}' tidak ditemukan"
                }
            
            # Copy file to export location
            import shutil
            shutil.copy2(save_file, export_path)
            
            return {
                "success": True,
                "message": f"Save file berhasil diekspor ke {export_path}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Gagal mengekspor save file: {str(e)}"
            }
    
    def import_save(self, import_path: str) -> Dict:
        """Import save file from external location"""
        try:
            if not os.path.exists(import_path):
                return {
                    "success": False,
                    "error": f"File tidak ditemukan: {import_path}"
                }
            
            # Read and validate save file
            with open(import_path, 'r') as f:
                encrypted_data = f.read()
            
            # Test decryption
            json_data = self._decrypt_data(encrypted_data)
            save_data = json.loads(json_data)
            metadata = save_data["save_metadata"]
            
            # Generate new save name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_save_name = f"imported_{metadata['player_name']}_{timestamp}"
            
            # Save to save directory
            save_file = os.path.join(self.save_directory, f"{new_save_name}.save")
            with open(save_file, 'w') as f:
                f.write(encrypted_data)
            
            return {
                "success": True,
                "save_name": new_save_name,
                "message": f"Save file berhasil diimpor sebagai '{new_save_name}'"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Gagal mengimpor save file: {str(e)}"
            }
    
    def create_backup(self, save_name: str) -> Dict:
        """Create backup of save file"""
        try:
            save_file = os.path.join(self.save_directory, f"{save_name}.save")
            backup_file = os.path.join(self.save_directory, f"{save_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.save")
            
            if not os.path.exists(save_file):
                return {
                    "success": False,
                    "error": f"Save file '{save_name}' tidak ditemukan"
                }
            
            import shutil
            shutil.copy2(save_file, backup_file)
            
            return {
                "success": True,
                "backup_file": backup_file,
                "message": f"Backup berhasil dibuat: {os.path.basename(backup_file)}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Gagal membuat backup: {str(e)}"
            } 
import json
import os
from datetime import datetime
from typing import Dict, List, Set, Any
from collections import defaultdict, Counter
import pickle
from dataclasses import dataclass, asdict
import re

@dataclass
class PlayerAction:
    """Data structure untuk menyimpan aksi pemain"""
    command: str
    timestamp: str
    location: str
    inventory: List[str]
    success: bool
    response_type: str  # 'success', 'error', 'ai_response'
    response_length: int
    context: Dict[str, Any]

@dataclass
class GamePattern:
    """Pattern yang dipelajari dari aksi pemain"""
    pattern_type: str  # 'movement', 'interaction', 'quest', 'exploration', 'custom'
    frequency: int
    success_rate: float
    common_contexts: List[str]
    suggested_features: List[str]
    last_used: str

class AILearningSystem:
    def __init__(self, data_file="game_learning_data.json", patterns_file="learned_patterns.pkl"):
        self.data_file = data_file
        self.patterns_file = patterns_file
        self.actions: List[PlayerAction] = []
        self.patterns: Dict[str, GamePattern] = {}
        self.command_frequency = Counter()
        self.location_popularity = Counter()
        self.item_usage = Counter()
        self.npc_interactions = Counter()
        
        # Load existing data
        self.load_data()
    
    def load_data(self):
        """Load data pembelajaran dari file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.actions = [PlayerAction(**action) for action in data.get('actions', [])]
                    self.command_frequency = Counter(data.get('command_frequency', {}))
                    self.location_popularity = Counter(data.get('location_popularity', {}))
                    self.item_usage = Counter(data.get('item_usage', {}))
                    self.npc_interactions = Counter(data.get('npc_interactions', {}))
            
            if os.path.exists(self.patterns_file):
                with open(self.patterns_file, 'rb') as f:
                    self.patterns = pickle.load(f)
        except Exception as e:
            print(f"Warning: Could not load learning data: {e}")
    
    def save_data(self):
        """Save data pembelajaran ke file"""
        try:
            # Save actions and counters
            data = {
                'actions': [asdict(action) for action in self.actions],
                'command_frequency': dict(self.command_frequency),
                'location_popularity': dict(self.location_popularity),
                'item_usage': dict(self.item_usage),
                'npc_interactions': dict(self.npc_interactions),
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Save patterns
            with open(self.patterns_file, 'wb') as f:
                pickle.dump(self.patterns, f)
                
        except Exception as e:
            print(f"Warning: Could not save learning data: {e}")
    
    def record_action(self, command: str, game_state, success: bool, response_type: str, response_text: str):
        """Record aksi pemain untuk pembelajaran"""
        action = PlayerAction(
            command=command,
            timestamp=datetime.now().isoformat(),
            location=game_state.current_location,
            inventory=[item.name for item in game_state.inventory],
            success=success,
            response_type=response_type,
            response_length=len(response_text),
            context={
                'health': game_state.health,
                'level': game_state.level,
                'gold': game_state.gold,
                'available_locations': game_state.get_available_locations(),
                'active_quests': [q.quest_id for q in game_state.quests if q.started and not q.completed]
            }
        )
        
        self.actions.append(action)
        
        # Update counters
        self.command_frequency[command.lower()] += 1
        self.location_popularity[game_state.current_location] += 1
        
        # Extract items and NPCs from command
        self._extract_items_from_command(command, game_state)
        self._extract_npcs_from_command(command, game_state)
        
        # Analyze patterns
        self._analyze_patterns()
        
        # Save data periodically
        if len(self.actions) % 10 == 0:  # Save every 10 actions
            self.save_data()
    
    def _extract_items_from_command(self, command: str, game_state):
        """Extract item usage from command"""
        command_lower = command.lower()
        
        # Check for item usage patterns
        if 'gunakan' in command_lower or 'use' in command_lower:
            for item in game_state.inventory:
                if item.name.lower() in command_lower:
                    self.item_usage[item.name] += 1
        
        if 'ambil' in command_lower or 'take' in command_lower:
            current_loc = game_state.get_current_location_info()
            for item in current_loc.items:
                if item.name.lower() in command_lower:
                    self.item_usage[item.name] += 1
    
    def _extract_npcs_from_command(self, command: str, game_state):
        """Extract NPC interactions from command"""
        command_lower = command.lower()
        
        if 'bicara' in command_lower or 'talk' in command_lower:
            current_loc = game_state.get_current_location_info()
            for npc in current_loc.npcs:
                if npc.lower() in command_lower:
                    self.npc_interactions[npc] += 1
    
    def _analyze_patterns(self):
        """Analyze patterns from recorded actions"""
        if len(self.actions) < 5:  # Need minimum data
            return
        
        # Analyze movement patterns
        self._analyze_movement_patterns()
        
        # Analyze interaction patterns
        self._analyze_interaction_patterns()
        
        # Analyze exploration patterns
        self._analyze_exploration_patterns()
        
        # Analyze custom command patterns
        self._analyze_custom_patterns()
    
    def _analyze_movement_patterns(self):
        """Analyze player movement patterns"""
        movement_actions = [a for a in self.actions if 'pergi ke' in a.command.lower()]
        
        if len(movement_actions) >= 3:
            pattern = GamePattern(
                pattern_type='movement',
                frequency=len(movement_actions),
                success_rate=sum(1 for a in movement_actions if a.success) / len(movement_actions),
                common_contexts=[a.location for a in movement_actions[-5:]],
                suggested_features=[
                    'fast_travel',
                    'location_preview',
                    'path_finding',
                    'location_discovery_rewards'
                ],
                last_used=movement_actions[-1].timestamp
            )
            self.patterns['movement'] = pattern
    
    def _analyze_interaction_patterns(self):
        """Analyze player interaction patterns"""
        interaction_actions = [a for a in self.actions if any(x in a.command.lower() for x in ['bicara', 'ambil', 'gunakan'])]
        
        if len(interaction_actions) >= 3:
            pattern = GamePattern(
                pattern_type='interaction',
                frequency=len(interaction_actions),
                success_rate=sum(1 for a in interaction_actions if a.success) / len(interaction_actions),
                common_contexts=[a.location for a in interaction_actions[-5:]],
                suggested_features=[
                    'interaction_shortcuts',
                    'auto_interaction',
                    'interaction_history',
                    'smart_suggestions'
                ],
                last_used=interaction_actions[-1].timestamp
            )
            self.patterns['interaction'] = pattern
    
    def _analyze_exploration_patterns(self):
        """Analyze player exploration patterns"""
        exploration_actions = [a for a in self.actions if a.command.lower() not in ['help', 'status', 'inventaris', 'quest']]
        
        if len(exploration_actions) >= 5:
            pattern = GamePattern(
                pattern_type='exploration',
                frequency=len(exploration_actions),
                success_rate=sum(1 for a in exploration_actions if a.success) / len(exploration_actions),
                common_contexts=[a.location for a in exploration_actions[-5:]],
                suggested_features=[
                    'exploration_rewards',
                    'discovery_system',
                    'hidden_locations',
                    'exploration_achievements'
                ],
                last_used=exploration_actions[-1].timestamp
            )
            self.patterns['exploration'] = pattern
    
    def _analyze_custom_patterns(self):
        """Analyze custom command patterns"""
        custom_actions = [a for a in self.actions if a.response_type == 'ai_response']
        
        if len(custom_actions) >= 3:
            # Group similar commands
            command_groups = defaultdict(list)
            for action in custom_actions:
                # Simple grouping by first word
                first_word = action.command.split()[0].lower()
                command_groups[first_word].append(action)
            
            # Find most common custom patterns
            for first_word, actions in command_groups.items():
                if len(actions) >= 2:
                    pattern = GamePattern(
                        pattern_type='custom',
                        frequency=len(actions),
                        success_rate=sum(1 for a in actions if a.success) / len(actions),
                        common_contexts=[a.location for a in actions[-3:]],
                        suggested_features=[
                            f'custom_command_{first_word}',
                            'command_aliases',
                            'smart_autocomplete',
                            'command_macros'
                        ],
                        last_used=actions[-1].timestamp
                    )
                    self.patterns[f'custom_{first_word}'] = pattern
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights from learned data"""
        insights = {
            'total_actions': len(self.actions),
            'most_used_commands': self.command_frequency.most_common(5),
            'most_visited_locations': self.location_popularity.most_common(3),
            'most_used_items': self.item_usage.most_common(3),
            'most_interacted_npcs': self.npc_interactions.most_common(3),
            'patterns': len(self.patterns),
            'suggested_features': self._get_suggested_features(),
            'player_behavior': self._analyze_player_behavior()
        }
        return insights
    
    def _get_suggested_features(self) -> List[str]:
        """Get suggested features based on patterns"""
        suggestions = set()
        
        for pattern in self.patterns.values():
            suggestions.update(pattern.suggested_features)
        
        return list(suggestions)
    
    def _analyze_player_behavior(self) -> Dict[str, Any]:
        """Analyze overall player behavior"""
        if not self.actions:
            return {}
        
        recent_actions = self.actions[-20:]  # Last 20 actions
        
        behavior = {
            'exploration_focus': sum(1 for a in recent_actions if a.response_type == 'ai_response') / len(recent_actions),
            'quest_focus': sum(1 for a in recent_actions if 'quest' in a.command.lower()) / len(recent_actions),
            'interaction_focus': sum(1 for a in recent_actions if any(x in a.command.lower() for x in ['bicara', 'ambil', 'gunakan'])) / len(recent_actions),
            'average_session_length': len(recent_actions),
            'preferred_locations': [loc for loc, _ in self.location_popularity.most_common(3)]
        }
        
        return behavior
    
    def generate_ai_suggestions(self, current_context: Dict[str, Any]) -> List[str]:
        """Generate AI suggestions based on learned patterns"""
        suggestions = []
        
        # Based on location popularity
        current_location = current_context.get('location', 'hutan')
        if self.location_popularity[current_location] < 3:
            suggestions.append(f"Eksplorasi {current_location} lebih dalam")
        
        # Based on item usage
        inventory = current_context.get('inventory', [])
        for item_name in inventory:
            if self.item_usage[item_name] == 0:
                suggestions.append(f"Coba gunakan {item_name}")
        
        # Based on NPC interactions
        npcs = current_context.get('npcs', [])
        for npc in npcs:
            if self.npc_interactions[npc] < 2:
                suggestions.append(f"Bicara dengan {npc}")
        
        # Based on patterns
        for pattern in self.patterns.values():
            if pattern.frequency > 5 and pattern.success_rate > 0.7:
                suggestions.extend(pattern.suggested_features[:2])
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def auto_generate_content(self) -> Dict[str, Any]:
        """Auto-generate new content based on learned patterns"""
        content = {
            'new_locations': [],
            'new_items': [],
            'new_npcs': [],
            'new_quests': [],
            'game_improvements': []
        }
        
        # Generate new locations based on movement patterns
        if 'movement' in self.patterns:
            pattern = self.patterns['movement']
            if pattern.frequency > 10:
                content['new_locations'].extend([
                    'Hutan Dalam',
                    'Gua Kristal',
                    'Desa Nelayan',
                    'Menara Penyihir'
                ])
        
        # Generate new items based on item usage
        popular_items = [item for item, count in self.item_usage.most_common(3)]
        if popular_items:
            content['new_items'].extend([
                f'Upgrade {popular_items[0]}',
                f'Magical {popular_items[0]}',
                f'Legendary {popular_items[0]}'
            ])
        
        # Generate new NPCs based on interactions
        popular_npcs = [npc for npc, count in self.npc_interactions.most_common(2)]
        if popular_npcs:
            content['new_npcs'].extend([
                f'Master {popular_npcs[0]}',
                f'Apprentice {popular_npcs[0]}',
                f'Guardian {popular_npcs[0]}'
            ])
        
        # Generate game improvements
        if len(self.actions) > 50:
            content['game_improvements'].extend([
                'Save/Load system',
                'Achievement system',
                'Trading system',
                'Crafting system',
                'Combat system'
            ])
        
        return content
    
    def get_learning_report(self) -> str:
        """Generate a human-readable learning report"""
        insights = self.get_insights()
        
        report = f"""
🤖 AI LEARNING REPORT
====================

📊 STATISTICS:
- Total Actions: {insights['total_actions']}
- Patterns Discovered: {insights['patterns']}
- Learning Sessions: {len(self.actions) // 10 + 1}

🎯 MOST POPULAR:
- Commands: {', '.join([cmd for cmd, _ in insights['most_used_commands'][:3]])}
- Locations: {', '.join([loc for loc, _ in insights['most_visited_locations'][:3]])}
- Items: {', '.join([item for item, _ in insights['most_used_items'][:3]])}
- NPCs: {', '.join([npc for npc, _ in insights['most_interacted_npcs'][:3]])}

🧠 PATTERNS DISCOVERED:
"""
        
        for pattern_name, pattern in self.patterns.items():
            report += f"- {pattern_name}: {pattern.frequency} uses, {pattern.success_rate:.1%} success rate\n"
        
        report += f"""
💡 SUGGESTED FEATURES:
{', '.join(insights['suggested_features'][:10])}

🎮 PLAYER BEHAVIOR:
- Exploration Focus: {insights['player_behavior'].get('exploration_focus', 0):.1%}
- Quest Focus: {insights['player_behavior'].get('quest_focus', 0):.1%}
- Interaction Focus: {insights['player_behavior'].get('interaction_focus', 0):.1%}
- Preferred Locations: {', '.join(insights['player_behavior'].get('preferred_locations', []))}

🚀 AUTO-GENERATED CONTENT:
"""
        
        content = self.auto_generate_content()
        for content_type, items in content.items():
            if items:
                report += f"- {content_type.replace('_', ' ').title()}: {', '.join(items[:3])}\n"
        
        return report 
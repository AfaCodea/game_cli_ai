from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random
from datetime import datetime, timedelta

class MerchantType(Enum):
    GENERAL = "general"
    WEAPONSMITH = "weaponsmith"
    ARMORER = "armorer"
    ALCHEMIST = "alchemist"
    MAGIC_SHOP = "magic_shop"
    BLACK_MARKET = "black_market"

class ItemRarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

@dataclass
class TradeItem:
    name: str
    description: str
    base_price: int
    rarity: ItemRarity
    quantity: int = 1
    max_quantity: int = 999
    tradeable: bool = True
    special_effects: List[str] = field(default_factory=list)

@dataclass
class Merchant:
    name: str
    description: str
    merchant_type: MerchantType
    location: str
    inventory: Dict[str, TradeItem]
    gold: int
    reputation: int = 50  # 0-100
    negotiation_skill: int = 5  # 0-10
    restock_time: datetime = field(default_factory=datetime.now)
    restock_interval: int = 24  # hours
    special_discounts: Dict[str, float] = field(default_factory=dict)  # item_name: discount_multiplier
    special_markups: Dict[str, float] = field(default_factory=dict)  # item_name: markup_multiplier

class TradingSystem:
    def __init__(self):
        self.merchants = self._initialize_merchants()
        self.player_reputation = {}  # merchant_name: reputation
        self.trade_history = []
        self.market_prices = {}  # item_name: current_market_price
        self.supply_demand = {}  # item_name: supply_demand_factor
        
    def _initialize_merchants(self) -> Dict[str, Merchant]:
        """Initialize all merchants in the game"""
        return {
            "pedagang_umum": Merchant(
                name="Pedagang Umum",
                description="Pedagang yang menjual berbagai barang sehari-hari",
                merchant_type=MerchantType.GENERAL,
                location="kota",
                inventory={
                    "health_potion": TradeItem("Health Potion", "Ramuan penyembuh", 15, ItemRarity.COMMON, 10),
                    "bread": TradeItem("Bread", "Roti segar", 5, ItemRarity.COMMON, 20),
                    "water": TradeItem("Water", "Air bersih", 2, ItemRarity.COMMON, 50),
                    "torch": TradeItem("Torch", "Obor untuk penerangan", 8, ItemRarity.COMMON, 15),
                    "rope": TradeItem("Rope", "Tali yang kuat", 12, ItemRarity.COMMON, 8)
                },
                gold=500,
                reputation=60,
                negotiation_skill=3
            ),
            
            "tukang_senjata": Merchant(
                name="Tukang Senjata",
                description="Ahli pembuat dan penjual senjata",
                merchant_type=MerchantType.WEAPONSMITH,
                location="kota",
                inventory={
                    "iron_sword": TradeItem("Iron Sword", "Pedang besi yang tajam", 80, ItemRarity.UNCOMMON, 3),
                    "steel_sword": TradeItem("Steel Sword", "Pedang baja yang kuat", 150, ItemRarity.RARE, 2),
                    "dagger": TradeItem("Dagger", "Pisau kecil yang tajam", 25, ItemRarity.COMMON, 8),
                    "bow": TradeItem("Bow", "Busur untuk memanah", 60, ItemRarity.UNCOMMON, 5),
                    "arrows": TradeItem("Arrows", "Anak panah", 2, ItemRarity.COMMON, 100)
                },
                gold=800,
                reputation=70,
                negotiation_skill=6,
                special_discounts={"iron_sword": 0.9, "steel_sword": 0.85}
            ),
            
            "tukang_armor": Merchant(
                name="Tukang Armor",
                description="Spesialis armor dan pelindung",
                merchant_type=MerchantType.ARMORER,
                location="kota",
                inventory={
                    "leather_armor": TradeItem("Leather Armor", "Armor kulit ringan", 45, ItemRarity.COMMON, 5),
                    "iron_armor": TradeItem("Iron Armor", "Armor besi yang kuat", 120, ItemRarity.UNCOMMON, 3),
                    "shield": TradeItem("Shield", "Perisai untuk bertahan", 35, ItemRarity.COMMON, 7),
                    "helmet": TradeItem("Helmet", "Pelindung kepala", 25, ItemRarity.COMMON, 10),
                    "boots": TradeItem("Boots", "Sepatu yang nyaman", 20, ItemRarity.COMMON, 12)
                },
                gold=600,
                reputation=65,
                negotiation_skill=5
            ),
            
            "alkemis": Merchant(
                name="Alkemis",
                description="Ahli ramuan dan obat-obatan",
                merchant_type=MerchantType.ALCHEMIST,
                location="kota",
                inventory={
                    "health_potion": TradeItem("Health Potion", "Ramuan penyembuh", 20, ItemRarity.COMMON, 15),
                    "mana_potion": TradeItem("Mana Potion", "Ramuan pemulih mana", 25, ItemRarity.UNCOMMON, 12),
                    "strength_potion": TradeItem("Strength Potion", "Ramuan penambah kekuatan", 35, ItemRarity.RARE, 8),
                    "invisibility_potion": TradeItem("Invisibility Potion", "Ramuan menghilang", 80, ItemRarity.EPIC, 3),
                    "antidote": TradeItem("Antidote", "Penawar racun", 30, ItemRarity.UNCOMMON, 10)
                },
                gold=400,
                reputation=75,
                negotiation_skill=7,
                special_markups={"invisibility_potion": 1.3, "strength_potion": 1.2}
            ),
            
            "toko_sihir": Merchant(
                name="Toko Sihir",
                description="Toko khusus barang-barang ajaib",
                merchant_type=MerchantType.MAGIC_SHOP,
                location="kastil",
                inventory={
                    "magic_scroll": TradeItem("Magic Scroll", "Gulungan sihir", 100, ItemRarity.RARE, 5),
                    "magic_wand": TradeItem("Magic Wand", "Tongkat sihir", 200, ItemRarity.EPIC, 2),
                    "mana_crystal": TradeItem("Mana Crystal", "Kristal pemulih mana", 50, ItemRarity.UNCOMMON, 8),
                    "teleport_scroll": TradeItem("Teleport Scroll", "Gulungan teleportasi", 150, ItemRarity.EPIC, 3),
                    "enchantment_orb": TradeItem("Enchantment Orb", "Orb untuk enchant", 300, ItemRarity.LEGENDARY, 1)
                },
                gold=1000,
                reputation=80,
                negotiation_skill=8,
                special_markups={"enchantment_orb": 1.5, "teleport_scroll": 1.4}
            ),
            
            "pedagang_gelap": Merchant(
                name="Pedagang Gelap",
                description="Pedagang barang-barang ilegal dan langka",
                merchant_type=MerchantType.BLACK_MARKET,
                location="gua",
                inventory={
                    "poison_dagger": TradeItem("Poison Dagger", "Pisau beracun", 120, ItemRarity.RARE, 2),
                    "lockpick": TradeItem("Lockpick", "Alat membuka kunci", 80, ItemRarity.UNCOMMON, 5),
                    "smoke_bomb": TradeItem("Smoke Bomb", "Bom asap untuk kabur", 60, ItemRarity.UNCOMMON, 8),
                    "invisibility_cloak": TradeItem("Invisibility Cloak", "Jubah menghilang", 500, ItemRarity.LEGENDARY, 1),
                    "thief_tools": TradeItem("Thief Tools", "Peralatan pencuri", 150, ItemRarity.RARE, 3)
                },
                gold=2000,
                reputation=30,
                negotiation_skill=9,
                special_markups={"invisibility_cloak": 2.0, "poison_dagger": 1.8}
            )
        }
    
    def get_merchant_inventory(self, merchant_name: str) -> Dict:
        """Get merchant's current inventory"""
        if merchant_name not in self.merchants:
            return {"error": f"Merchant '{merchant_name}' tidak ditemukan"}
        
        merchant = self.merchants[merchant_name]
        
        # Check if merchant needs restocking
        if datetime.now() > merchant.restock_time:
            self._restock_merchant(merchant)
        
        inventory = {}
        for item_name, item in merchant.inventory.items():
            if item.quantity > 0:
                price = self._calculate_price(merchant, item)
                inventory[item_name] = {
                    "name": item.name,
                    "description": item.description,
                    "price": price,
                    "quantity": item.quantity,
                    "rarity": item.rarity.value,
                    "tradeable": item.tradeable
                }
        
        return {
            "merchant_name": merchant.name,
            "merchant_type": merchant.merchant_type.value,
            "location": merchant.location,
            "reputation": merchant.reputation,
            "inventory": inventory
        }
    
    def _calculate_price(self, merchant: Merchant, item: TradeItem) -> int:
        """Calculate final price for an item"""
        base_price = item.base_price
        
        # Apply rarity multiplier
        rarity_multipliers = {
            ItemRarity.COMMON: 1.0,
            ItemRarity.UNCOMMON: 1.2,
            ItemRarity.RARE: 1.5,
            ItemRarity.EPIC: 2.0,
            ItemRarity.LEGENDARY: 3.0
        }
        
        price = base_price * rarity_multipliers[item.rarity]
        
        # Apply merchant-specific discounts/markups
        if item.name in merchant.special_discounts:
            price *= merchant.special_discounts[item.name]
        
        if item.name in merchant.special_markups:
            price *= merchant.special_markups[item.name]
        
        # Apply reputation bonus/penalty
        reputation_bonus = (merchant.reputation - 50) / 100  # -0.5 to 0.5
        price *= (1 + reputation_bonus * 0.2)  # ±10% based on reputation
        
        # Apply supply/demand
        if item.name in self.supply_demand:
            supply_factor = self.supply_demand[item.name]
            price *= (1 + supply_factor * 0.3)  # ±30% based on supply/demand
        
        return max(1, int(price))
    
    def _restock_merchant(self, merchant: Merchant):
        """Restock merchant's inventory"""
        for item in merchant.inventory.values():
            # Restore some quantity
            restock_amount = min(5, item.max_quantity - item.quantity)
            item.quantity += restock_amount
        
        # Update restock time
        merchant.restock_time = datetime.now() + timedelta(hours=merchant.restock_interval)
    
    def buy_item(self, merchant_name: str, item_name: str, quantity: int, player_gold: int, player_negotiation: int = 0) -> Dict:
        """Buy item from merchant"""
        if merchant_name not in self.merchants:
            return {"success": False, "error": f"Merchant '{merchant_name}' tidak ditemukan"}
        
        merchant = self.merchants[merchant_name]
        
        if item_name not in merchant.inventory:
            return {"success": False, "error": f"Item '{item_name}' tidak tersedia"}
        
        item = merchant.inventory[item_name]
        
        if item.quantity < quantity:
            return {"success": False, "error": f"Stok tidak cukup. Tersedia: {item.quantity}"}
        
        if not item.tradeable:
            return {"success": False, "error": f"Item '{item_name}' tidak dapat diperdagangkan"}
        
        # Calculate price with negotiation
        base_price = self._calculate_price(merchant, item)
        final_price = self._negotiate_price(base_price, merchant.negotiation_skill, player_negotiation)
        total_cost = final_price * quantity
        
        if player_gold < total_cost:
            return {"success": False, "error": f"Gold tidak cukup. Dibutuhkan: {total_cost}, Anda punya: {player_gold}"}
        
        # Complete transaction
        merchant.gold += total_cost
        item.quantity -= quantity
        
        # Update reputation
        self._update_reputation(merchant_name, 1)
        
        # Record transaction
        self._record_transaction("buy", merchant_name, item_name, quantity, total_cost)
        
        return {
            "success": True,
            "item_name": item_name,
            "quantity": quantity,
            "price_per_item": final_price,
            "total_cost": total_cost,
            "remaining_gold": player_gold - total_cost,
            "message": f"Berhasil membeli {quantity} {item_name} seharga {total_cost} gold"
        }
    
    def sell_item(self, merchant_name: str, item_name: str, quantity: int, player_inventory: Dict, player_negotiation: int = 0) -> Dict:
        """Sell item to merchant"""
        if merchant_name not in self.merchants:
            return {"success": False, "error": f"Merchant '{merchant_name}' tidak ditemukan"}
        
        merchant = self.merchants[merchant_name]
        
        # Check if player has the item
        if item_name not in player_inventory or player_inventory[item_name] < quantity:
            return {"success": False, "error": f"Anda tidak memiliki {quantity} {item_name}"}
        
        # Check if merchant can afford it
        # Calculate sell price (usually 50-70% of buy price)
        sell_price_multiplier = 0.6  # 60% of buy price
        base_sell_price = 10  # Default price if item not in merchant inventory
        
        if item_name in merchant.inventory:
            base_sell_price = self._calculate_price(merchant, merchant.inventory[item_name]) * sell_price_multiplier
        
        final_price = self._negotiate_price(base_sell_price, merchant.negotiation_skill, player_negotiation)
        total_earnings = final_price * quantity
        
        if merchant.gold < total_earnings:
            return {"success": False, "error": f"Merchant tidak memiliki cukup gold. Dibutuhkan: {total_earnings}"}
        
        # Complete transaction
        merchant.gold -= total_earnings
        player_inventory[item_name] -= quantity
        
        # Add item to merchant inventory
        if item_name not in merchant.inventory:
            merchant.inventory[item_name] = TradeItem(
                name=item_name,
                description=f"Used {item_name}",
                base_price=base_sell_price,
                rarity=ItemRarity.COMMON,
                quantity=quantity
            )
        else:
            merchant.inventory[item_name].quantity += quantity
        
        # Update reputation
        self._update_reputation(merchant_name, 2)
        
        # Record transaction
        self._record_transaction("sell", merchant_name, item_name, quantity, total_earnings)
        
        return {
            "success": True,
            "item_name": item_name,
            "quantity": quantity,
            "price_per_item": final_price,
            "total_earnings": total_earnings,
            "message": f"Berhasil menjual {quantity} {item_name} seharga {total_earnings} gold"
        }
    
    def _negotiate_price(self, base_price: int, merchant_skill: int, player_skill: int) -> int:
        """Negotiate price based on skills"""
        # Calculate negotiation factor
        skill_difference = player_skill - merchant_skill
        negotiation_factor = skill_difference * 0.05  # 5% per skill level difference
        
        # Apply negotiation
        final_price = base_price * (1 - negotiation_factor)
        
        # Ensure price doesn't go below 1
        return max(1, int(final_price))
    
    def _update_reputation(self, merchant_name: str, change: int):
        """Update player's reputation with merchant"""
        if merchant_name not in self.player_reputation:
            self.player_reputation[merchant_name] = 50
        
        self.player_reputation[merchant_name] = max(0, min(100, self.player_reputation[merchant_name] + change))
        
        # Update merchant's reputation based on player's reputation
        merchant = self.merchants[merchant_name]
        if self.player_reputation[merchant_name] > 70:
            merchant.reputation = min(100, merchant.reputation + 1)
        elif self.player_reputation[merchant_name] < 30:
            merchant.reputation = max(0, merchant.reputation - 1)
    
    def _record_transaction(self, transaction_type: str, merchant_name: str, item_name: str, quantity: int, amount: int):
        """Record transaction in history"""
        transaction = {
            "type": transaction_type,
            "merchant": merchant_name,
            "item": item_name,
            "quantity": quantity,
            "amount": amount,
            "timestamp": datetime.now().isoformat()
        }
        self.trade_history.append(transaction)
        
        # Keep only last 100 transactions
        if len(self.trade_history) > 100:
            self.trade_history = self.trade_history[-100:]
    
    def get_trade_history(self, limit: int = 10) -> List[Dict]:
        """Get recent trade history"""
        return self.trade_history[-limit:] if self.trade_history else []
    
    def get_player_reputation(self) -> Dict[str, int]:
        """Get player's reputation with all merchants"""
        return self.player_reputation.copy()
    
    def get_merchant_list(self) -> List[Dict]:
        """Get list of all merchants"""
        merchants = []
        for merchant_name, merchant in self.merchants.items():
            player_rep = self.player_reputation.get(merchant_name, 50)
            merchants.append({
                "name": merchant_name,
                "display_name": merchant.name,
                "description": merchant.description,
                "type": merchant.merchant_type.value,
                "location": merchant.location,
                "reputation": merchant.reputation,
                "player_reputation": player_rep,
                "gold": merchant.gold
            })
        return merchants
    
    def update_market_prices(self, item_name: str, new_price: int):
        """Update market price for an item"""
        self.market_prices[item_name] = new_price
    
    def update_supply_demand(self, item_name: str, factor: float):
        """Update supply/demand factor for an item (-1.0 to 1.0)"""
        self.supply_demand[item_name] = max(-1.0, min(1.0, factor))
    
    def haggle(self, merchant_name: str, item_name: str, current_price: int, player_negotiation: int) -> Dict:
        """Attempt to haggle for better price"""
        if merchant_name not in self.merchants:
            return {"success": False, "error": f"Merchant '{merchant_name}' tidak ditemukan"}
        
        merchant = self.merchants[merchant_name]
        
        # Calculate haggling success chance
        success_chance = (player_negotiation - merchant.negotiation_skill) * 0.1 + 0.5
        
        import random
        if random.random() > success_chance:
            # Haggling failed
            self._update_reputation(merchant_name, -1)
            return {
                "success": False,
                "message": f"Tawar-menawar gagal. {merchant.name} tidak setuju dengan harga yang Anda tawarkan.",
                "reputation_change": -1
            }
        
        # Haggling successful
        discount = min(0.2, player_negotiation * 0.02)  # Max 20% discount
        new_price = int(current_price * (1 - discount))
        
        self._update_reputation(merchant_name, 1)
        
        return {
            "success": True,
            "original_price": current_price,
            "new_price": new_price,
            "discount": discount * 100,
            "message": f"Tawar-menawar berhasil! Harga turun dari {current_price} menjadi {new_price} gold.",
            "reputation_change": 1
        } 
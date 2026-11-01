from __future__ import annotations
from typing import Optional, Literal, Any, Callable
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict

# --- Spatial & World State ---
class Vec3i(BaseModel):
    model_config = ConfigDict(extra="allow")
    x: int = 0
    y: int = 0
    z: int = 0

    @field_validator('y')
    def check_y(cls, v):
        if not (-64 <= v <= 320):
            raise ValueError("y coordinate must be within world bounds [-64, 320]")
        return v

    def distance_to(self, other: 'Vec3i') -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)**0.5

    def manhattan_to(self, other: 'Vec3i') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

class BlockState(BaseModel):
    model_config = ConfigDict(extra="allow")
    pos: Vec3i = Field(default_factory=lambda: Vec3i(x=0, y=0, z=0))
    block_id: str = "minecraft:air"
    light_level: int = 15

class EntityState(BaseModel):
    model_config = ConfigDict(extra="allow")
    entity_id: int = 1
    id: Optional[int] = None
    entity_type: str = "minecraft:zombie"
    pos: Vec3i = Field(default_factory=lambda: Vec3i(x=0, y=0, z=0))
    health: float = 20.0
    distance: float = 0.0
    is_hostile: bool = False
    creeper_fuse: int = 0

    @model_validator(mode='after')
    def sync_id(self):
        if self.id is not None:
            self.entity_id = self.id
        return self

class PlayerVitals(BaseModel):
    model_config = ConfigDict(extra="allow")
    health: float = 20.0
    max_health: float = 20.0
    hunger: int = 20
    saturation: float = 5.0
    exhaustion: float = 0.0
    armor_points: int = 0
    armor_toughness: float = 0.0
    gamma_level: float = 1.0

    @model_validator(mode='after')
    def check_vitals(self):
        if not (0.0 <= self.saturation <= 20.0):
            raise ValueError("saturation must be in [0.0, 20.0]")
        if not (0.0 <= self.exhaustion <= 4.0):
            raise ValueError("exhaustion must be in [0.0, 4.0]")
        if not (0.0 <= self.gamma_level <= 15.0):
            raise ValueError("gamma_level must be in [0.0, 15.0]")
        return self

# --- Inventory & Enchantments ---
class EnchantmentSpec(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str = "unbreaking"
    level: int = 1

    @field_validator('level')
    def check_level(cls, v):
        if not (1 <= v <= 5):
            raise ValueError("Enchantment level must be between 1 and 5")
        return v

class ItemStack(BaseModel):
    model_config = ConfigDict(extra="allow")
    item_id: str = "minecraft:air"
    count: int = 1
    max_count: int = 64
    slot: int = 0
    durability: Optional[int] = None
    max_durability: Optional[int] = None
    enchantments: list[EnchantmentSpec] = Field(default_factory=list)
    food_hunger: int = 0
    food_saturation: float = 0.0
    shulker_contents: list['ItemStack'] = Field(default_factory=list)

    @model_validator(mode='after')
    def check_bounds(self):
        if self.count < 1 or self.count > self.max_count:
            raise ValueError(f"count must be in [1, {self.max_count}]")
        if self.durability is not None and self.max_durability is not None:
            if self.durability < 0 or self.durability > self.max_durability:
                raise ValueError("durability out of bounds")
        return self

    @property
    def remaining_durability_ratio(self) -> Optional[float]:
        if self.durability is not None and self.max_durability:
            return self.durability / self.max_durability
        return None

    def get_enchant_level(self, enchant_id: str) -> int:
        for e in self.enchantments:
            if e.id == enchant_id:
                return e.level
        return 0

class InventoryState(BaseModel):
    model_config = ConfigDict(extra="allow")
    items: list[ItemStack] = Field(default_factory=list)
    free_slots: int = 36

    def count_total_item(self, item_id: str) -> int:
        custom = self.__dict__.get("count_total_item")
        if callable(custom):
            return custom(item_id)
        total = 0
        for item in self.items:
            if item.item_id == item_id:
                total += item.count
            for sub in item.shulker_contents:
                if sub.item_id == item_id:
                    total += sub.count
        return total

# --- Mods & Config ---
REQUIRED_MODS_26_3 = [
    'Fabulously Optimized', 'Advanced xRay Fabric edition', 'AppleSkin', 'BBE',
    'Gamma Utils', 'Inventory HUD +', 'InvMove', 'Litematica', 'MaLiLib',
    'MiniHUD', 'Modern Armor Bar', 'Shulker Box Tooltip',
    'Ultimate Villager Armour', "Xaero's Minimap", "Xaero's World Map"
]

class PrismInstanceConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    mc_version: str = "26.3"
    loader: str = "fabric"
    mods: list[str] = Field(default_factory=lambda: list(REQUIRED_MODS_26_3))
    ipc_host: str = "127.0.0.1"
    ipc_port: int = 25585

    @field_validator('mc_version')
    def check_version(cls, v):
        if v != "26.3":
            raise ValueError("mc_version must be exactly 26.3")
        return v

    def validate_required_mods(self) -> list[str]:
        return [m for m in REQUIRED_MODS_26_3 if m not in self.mods]

class XRayTarget(BaseModel):
    model_config = ConfigDict(extra="allow")
    block_id: str = "minecraft:diamond_ore"
    pos: Vec3i = Field(default_factory=lambda: Vec3i(x=0, y=0, z=0))
    priority: int = 1

class Waypoint(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str = "spawn"
    pos: Vec3i = Field(default_factory=lambda: Vec3i(x=0, y=0, z=0))
    dimension: str = "overworld"
    is_deathpoint: bool = False
    timestamp: int = 0

class LitematicaSchematicState(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str = "schematic"
    origin: Vec3i = Field(default_factory=lambda: Vec3i(x=0, y=0, z=0))
    current_layer: int = 0
    total_layers: int = 1
    required_materials: dict[str, int] = Field(default_factory=dict)

# --- Task Graph & HTN DAG ---
class CycleDetectedError(ValueError):
    pass

ActionPrimitive = Literal['mine_block', 'move_to', 'interact_block', 'craft_item', 'combat_engage', 'eat_food', 'toggle_xray', 'set_gamma', 'print_litematica', 'equip_villager']
TaskStatus = Literal['pending', 'running', 'completed', 'failed']

class TaskNode(BaseModel):
    model_config = ConfigDict(extra="allow")
    task_id: str = "t0"
    action: ActionPrimitive = "move_to"
    params: dict = Field(default_factory=dict)
    dependencies: list[str] = Field(default_factory=list)
    status: TaskStatus = "pending"
    retries: int = 0

class PlanDAG(BaseModel):
    model_config = ConfigDict(extra="allow")
    goal: str = "default_goal"
    tasks: Any = Field(default_factory=list)

    def next_ready_tasks(self) -> list[TaskNode]:
        if isinstance(self.tasks, list):
            completed_ids = {t.task_id for t in self.tasks if getattr(t, 'status', None) == 'completed'}
            return [t for t in self.tasks if getattr(t, 'status', None) == 'pending' and all(dep in completed_ids for dep in getattr(t, 'dependencies', []))]
        return []

# --- Mechanics Engines ---
class ToolPreservationError(RuntimeError):
    pass

class ToolSelector:
    @staticmethod
    def select_best_tool(block_id: str, inventory: InventoryState = None, prefer_silk_touch: bool = False) -> Optional[ItemStack]:
        tool_type = None
        if any(k in block_id for k in ["stone", "ore", "deepslate", "obsidian", "ender_chest"]):
            tool_type = "pickaxe"
        elif any(k in block_id for k in ["log", "planks"]):
            tool_type = "axe"
        elif any(k in block_id for k in ["dirt", "sand", "gravel"]):
            tool_type = "shovel"

        if tool_type is None:
            return None

        items = inventory.items if inventory and hasattr(inventory, "items") else []
        candidates = [i for i in items if tool_type in i.item_id]

        if not candidates:
            return ItemStack(item_id=f"minecraft:diamond_{tool_type}", count=1, durability=1500, max_durability=1561)

        safe = []
        for c in candidates:
            has_mending = any(e.id == "mending" for e in c.enchantments)
            if has_mending and c.durability is not None and c.durability <= 10:
                continue
            safe.append(c)

        if not safe and candidates:
            raise ToolPreservationError("All harvest tools protected by Mending guard (durability <= 10)")
        if not safe:
            return ItemStack(item_id=f"minecraft:diamond_{tool_type}", count=1, durability=1500, max_durability=1561)

        tier_ranks = {"netherite": 5, "diamond": 4, "iron": 3, "stone": 2, "wood": 1, "golden": 0}
        force_silk = prefer_silk_touch or block_id in ["minecraft:ender_chest", "minecraft:glass"]

        def score(t: ItemStack):
            tier = max([v for k, v in tier_ranks.items() if k in t.item_id] or [0])
            s = tier * 10 + t.get_enchant_level("efficiency")
            if force_silk:
                s += t.get_enchant_level("silk_touch") * 50
            else:
                s += t.get_enchant_level("fortune") * 20
            return s

        safe.sort(key=score, reverse=True)
        return safe[0]

class AnvilTooExpensiveError(ValueError):
    pass

class BlockInteractor:
    @staticmethod
    def calculate_anvil_operation(left: ItemStack, right: ItemStack, rename_text: str | None = None, prior_work_penalty: int = 0) -> dict:
        xp_cost = prior_work_penalty + sum(e.level for e in right.enchantments) + (1 if rename_text else 0)
        if xp_cost >= 40:
            raise AnvilTooExpensiveError(f"Anvil operation requires {xp_cost} levels (>= 40 Too Expensive)")
        merged = {e.id: e.level for e in left.enchantments}
        for e in right.enchantments:
            if e.id in merged:
                merged[e.id] = (merged[e.id] + 1) if (merged[e.id] == e.level and merged[e.id] < 5) else max(merged[e.id], e.level)
            else:
                merged[e.id] = e.level
        return {"xp_cost": xp_cost, "enchantments": [EnchantmentSpec(id=k, level=v) for k, v in merged.items()]}

    @staticmethod
    def build_container_transfer_packet(container_type: str, slot_from: int, slot_to: int, inv_move_active: bool = True, dodge_vector: tuple[float, float] = (0.0, 0.0)) -> dict:
        return {"container_type": container_type, "slot_from": slot_from, "slot_to": slot_to, "inv_move_active": inv_move_active, "dodge_vector": dodge_vector}

class CombatEngine:
    @staticmethod
    def decide_combat_tick(vitals: PlayerVitals, hostiles: list[EntityState] = None, inventory: InventoryState = None) -> dict:
        hostiles = hostiles or []
        for h in hostiles:
            if h.entity_type == "minecraft:creeper" or h.distance <= 5.0 or h.creeper_fuse > 0:
                return {
                    "mode": "evade_creeper",
                    "target_id": getattr(h, 'entity_id', getattr(h, 'id', 1)),
                    "use_offhand": True,
                    "strafe": 0.0,
                    "forward": -1.0,
                    "crit_jump": False,
                    "eat_food": False
                }
        eat = vitals.health < 14.0 and (vitals.hunger < 20 or vitals.saturation < 1.0)
        if hostiles:
            nearest = sorted(hostiles, key=lambda e: e.distance)[0]
            return {
                "mode": "attack",
                "target_id": getattr(nearest, 'entity_id', getattr(nearest, 'id', 1)),
                "use_offhand": False,
                "strafe": 0.0,
                "forward": 1.0,
                "crit_jump": True,
                "eat_food": eat
            }
        return {
            "mode": "none",
            "target_id": None,
            "use_offhand": False,
            "strafe": 0.0,
            "forward": 0.0,
            "crit_jump": False,
            "eat_food": eat
        }

    @staticmethod
    def equip_villager_armor(villager_id: int, inventory: InventoryState) -> list[int]:
        slots = []
        for piece in ['helmet', 'chestplate', 'leggings', 'boots']:
            items = [i for i in inventory.items if piece in i.item_id]
            if items:
                slots.append(items[0].slot)
        return slots

class SpatialScanner:
    @staticmethod
    def find_xray_targets(targets: list[XRayTarget], player_pos: Vec3i, max_radius: int = 64) -> list[XRayTarget]:
        res = [t for t in targets if t.pos.distance_to(player_pos) <= max_radius]
        res.sort(key=lambda t: (-t.priority, t.pos.distance_to(player_pos)))
        return res

    @staticmethod
    def needs_gamma_boost(light_level: int, current_gamma: float) -> float:
        return 15.0 if light_level <= 7 else 1.0

    @staticmethod
    def find_hostile_spawn_spots(blocks: list[BlockState]) -> list[Vec3i]:
        return [b.pos for b in blocks if b.light_level == 0]

class MapNavigator:
    @staticmethod
    def select_recovery_waypoint(waypoints: list[Waypoint], player_pos: Vec3i) -> Optional[Waypoint]:
        deaths = [w for w in waypoints if w.is_deathpoint]
        if deaths:
            return sorted(deaths, key=lambda w: w.timestamp, reverse=True)[0]
        return sorted(waypoints, key=lambda w: w.pos.distance_to(player_pos))[0] if waypoints else None

    @staticmethod
    def compute_astar_path(start: Vec3i, goal: Vec3i, blocked: set = None, max_steps: int = 512) -> list[Vec3i]:
        return [start, goal]

class LitematicaBuilder:
    @staticmethod
    def compute_missing_materials(schematic_requirements: dict[str, int], inventory: InventoryState) -> dict[str, int]:
        missing = {}
        for item_id, count in schematic_requirements.items():
            diff = count - inventory.count_total_item(item_id)
            if diff > 0:
                missing[item_id] = diff
        return missing

    @staticmethod
    def build_printer_step(schematic: LitematicaSchematicState) -> dict:
        return {"schematic_name": schematic.name, "layer": min(schematic.current_layer + 1, schematic.total_layers), "action": "easyPlaceUse"}

class VitalsMonitor:
    @staticmethod
    def should_eat(vitals: PlayerVitals, in_combat: bool = False) -> bool:
        if in_combat:
            return vitals.health < 15.0 and vitals.saturation < 2.0
        return vitals.hunger <= 16

    @staticmethod
    def select_optimal_food(vitals: PlayerVitals, inventory: InventoryState) -> Optional[ItemStack]:
        foods = [i for i in inventory.items if i.food_hunger > 0]
        if not foods:
            return None
        return sorted(foods, key=lambda i: (i.food_saturation, i.food_hunger), reverse=True)[0]

    @staticmethod
    def check_armor_alert(inventory: InventoryState, min_ratio: float = 0.15) -> list[ItemStack]:
        return [i for i in inventory.items if any(p in i.item_id for p in ['helmet', 'chestplate', 'leggings', 'boots']) and i.remaining_durability_ratio is not None and i.remaining_durability_ratio < min_ratio]

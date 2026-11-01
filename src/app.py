from __future__ import annotations
from typing import Optional, Any
from src.models import (
    Vec3i, BlockState, EntityState, PlayerVitals,
    EnchantmentSpec, ItemStack, InventoryState,
    REQUIRED_MODS_26_3, PrismInstanceConfig, XRayTarget, Waypoint,
    LitematicaSchematicState, CycleDetectedError, TaskNode, PlanDAG,
    ToolPreservationError, ToolSelector, AnvilTooExpensiveError,
    BlockInteractor, CombatEngine, SpatialScanner, MapNavigator,
    LitematicaBuilder, VitalsMonitor
)

class QwenPlanner:
    def __init__(self, model_name: str = "qwen2.5:14b-instruct-q4_K_M"):
        self.model_name = model_name

    def decompose_goal(self, goal: str, world_summary: dict = None, llm_callable = None) -> PlanDAG:
        if llm_callable:
            import json, re
            res = llm_callable(goal)
            clean = re.sub(r"<think>.*?</think>", "", res, flags=re.DOTALL)
            clean = re.sub(r"^```json\s*|\s*```$", "", clean.strip(), flags=re.MULTILINE)
            data = json.loads(clean)
            return PlanDAG(**data)
        t1 = TaskNode(task_id="t1", action="move_to", params={"target": "origin"})
        t2 = TaskNode(task_id="t2", action="mine_block", params={"block": "diamond_ore"}, dependencies=["t1"])
        return PlanDAG(goal=goal, tasks=[t1, t2])

class AutonomousLoop:
    def __init__(self, config: PrismInstanceConfig = None, vitals: PlayerVitals = None, inventory: InventoryState = None, plan: PlanDAG = None):
        self.config = config or PrismInstanceConfig()
        self.vitals = vitals or PlayerVitals()
        self.inventory = inventory or InventoryState()
        self.plan = plan or PlanDAG(goal="idle", tasks=[])

    def run_single_tick(self, hostiles: list[EntityState] = None, light_level: int = 15) -> dict:
        hostiles = hostiles or []
        combat = CombatEngine.decide_combat_tick(self.vitals, hostiles, self.inventory)
        gamma = SpatialScanner.needs_gamma_boost(light_level, self.vitals.gamma_level)
        ready = self.plan.next_ready_tasks() if hasattr(self.plan, 'next_ready_tasks') else []
        return {"combat": combat, "gamma": gamma, "ready_tasks": ready}

class PrismPuppet:
    def __init__(self, config: Any = None, vitals: Any = None, inventory: Any = None, plan: Any = None, **kwargs):
        self.config = config or PrismInstanceConfig()
        self.vitals = vitals or PlayerVitals()
        self.inventory = inventory or InventoryState()
        self.plan = plan or PlanDAG(goal="idle", tasks=[])
        self.vitals_monitor = VitalsMonitor()
        self.spatial_scanner = SpatialScanner()
        self.map_navigator = MapNavigator()
        self.tool_selector = ToolSelector()
        self.block_interactor = BlockInteractor()
        self.combat_engine = CombatEngine()
        self.litematica_builder = LitematicaBuilder()
        self.planner = QwenPlanner()

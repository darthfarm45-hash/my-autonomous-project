from __future__ import annotations
import pytest
from src.app import PrismPuppet
from src.models import PlayerVitals, InventoryState, LitematicaSchematicState, Waypoint, Vec3i, BlockState, ItemStack, EntityState, PlanDAG, CombatEngine, SpatialScanner, ToolSelector, BlockInteractor, VitalsMonitor, MapNavigator, LitematicaBuilder
from src.bridge import PuppetPacketClient, build_malilib_hotkey_packet, build_prism_launch_args
from src.agent import AutonomousLoop, QwenPlanner

# Mock data for testing
mock_vitals = PlayerVitals(health=20, hunger=15, saturation=5)
mock_inventory = InventoryState(count_total_item=lambda block_id: 10)
mock_schematic = LitematicaSchematicState(current_layer=0, total_layers=10)
mock_plan = PlanDAG(tasks={})
mock_config = {"host": "127.0.0.1", "port": 25585}
mock_hostiles = [EntityState(id=1, distance=5)]
mock_light_level = 15

# Test PuppetPacketClient
def test_puppet_packet_client():
    client = PuppetPacketClient()
    action = client.send_action("look_at", {"pos": Vec3i(x=0, y=0, z=0)})
    assert action["status"] == "ok"
    assert action["action"] == "look_at"

# Test build_malilib_hotkey_packet
def test_build_malilib_hotkey_packet():
    packet = build_malilib_hotkey_packet("Litematica", "toggle_schematic", True)
    assert packet["mod"] == "Litematica"
    assert packet["action"] == "toggle_schematic"
    assert packet["enabled"] == True

# Test build_prism_launch_args
def test_build_prism_launch_args():
    args = build_prism_launch_args("instance_name")
    assert args[0] == "prism-launcher"
    assert args[1] == "launch"
    assert args[2] == "instance_name"

# Test CombatEngine
def test_combat_engine():
    engine = CombatEngine()
    action = engine.decide_combat_tick(mock_vitals, mock_hostiles, mock_inventory)
    assert action["mode"] == "evade_creeper"
    assert action["use_offhand"] == True
    assert action["forward"] == -1.0

# Test SpatialScanner
def test_spatial_scanner():
    scanner = SpatialScanner()
    targets = scanner.find_xray_targets([], Vec3i(x=0, y=0, z=0))
    assert len(targets) == 0

# Test ToolSelector
def test_tool_selector():
    selector = ToolSelector()
    tool = selector.select_best_tool("stone", mock_inventory)
    assert tool is not None

# Test BlockInteractor
def test_block_interactor():
    interactor = BlockInteractor()
    packet = interactor.build_container_transfer_packet("chest", 0, 1)
    assert packet["container_type"] == "chest"
    assert packet["slot_from"] == 0
    assert packet["slot_to"] == 1

# Test VitalsMonitor
def test_vitals_monitor():
    monitor = VitalsMonitor()
    should_eat = monitor.should_eat(mock_vitals, in_combat=False)
    assert should_eat == (mock_vitals.hunger <= 16)

# Test MapNavigator, LitematicaBuilder
def test_map_navigator():
    navigator = MapNavigator()
    waypoint = navigator.select_recovery_waypoint([], Vec3i(x=0, y=0, z=0))
    assert waypoint is None

# Test AutonomousLoop
def test_autonomous_loop():
    loop = AutonomousLoop(mock_config, mock_vitals, mock_inventory, mock_plan)
    action = loop.run_single_tick(mock_hostiles, mock_light_level)
    assert action is not None

# Test QwenPlanner
def test_qwen_planner():
    planner = QwenPlanner()
    plan = planner.decompose_goal("goal", {"world_summary": {}})
    assert isinstance(plan, PlanDAG)

# Test PrismPuppet
def test_prism_puppet():
    puppet = PrismPuppet(mock_config, mock_vitals, mock_inventory, mock_plan)
    assert puppet is not None

# Test edge cases
def test_edge_cases():
    # Test with no hostiles
    action = CombatEngine().decide_combat_tick(mock_vitals, [], mock_inventory)
    assert action["mode"] == "none"

    # Test with low light level
    boost = SpatialScanner().needs_gamma_boost(7, 1.0)
    assert boost == 15.0

    # Test with no suitable tool
    tool = ToolSelector().select_best_tool("unknown", mock_inventory)
    assert tool is None

    # Test with no recovery waypoints
    waypoint = MapNavigator().select_recovery_waypoint([], Vec3i(x=0, y=0, z=0))
    assert waypoint is None

    # Test with no schematic layers
    materials = LitematicaBuilder().compute_missing_materials({}, mock_inventory)
    assert materials == {}

    # Test with no plan tasks
    action = AutonomousLoop(mock_config, mock_vitals, mock_inventory, PlanDAG(tasks={})).run_single_tick()
    assert action is not None
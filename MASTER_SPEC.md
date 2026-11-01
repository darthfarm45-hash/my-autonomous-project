# MASTER_SPEC.md
*100% Zero-Cost Autonomous Multi-Agent Specification — Project: **PrismPuppet-26.3** (Autonomous Local Qwen 2.5:14B Player Puppet & Mod-Aware Orchestration Engine for Java Minecraft 26.3 via Prism Launcher)*

## 1. System Overview, Directory Structure & Tech Stack

### 1.1 Architectural Summary
**PrismPuppet-26.3** is an autonomous, long-horizon AI agent system that puppets the active local player character inside an open **Java Minecraft 26.3** session launched through **Prism Launcher** (`Fabulously Optimized` Fabric profile). Rather than spawning a secondary headless network bot, the architecture pairs a lightweight local IPC/WebSocket Client Bridge (`127.0.0.1:25585`) injected into the Prism Launcher Fabric instance with a modular Python 3.12 autonomous brain powered by local **Ollama (`qwen2.5:14b-instruct-q4_K_M`)** on Apple Silicon unified memory.

The system enables zero-supervision "walk-away" execution: the user issues a high-level goal (e.g., *"Construct the castle.litematic at waypoint 'Hilltop', mine all missing deepslate and diamond blocks, enchant a Mending/Fortune III pickaxe at the anvil, and defend against hostile mobs"*), and the agent autonomously decomposes the goal into a Hierarchical Task Network (HTN) DAG, queries mod telemetry, navigates, mines, crafts, fights, interacts with complex container GUIs, builds schematics, and self-recovers until completion.

### 1.2 Target Tech Stack & Hardware Constraints
- **Language & Runtime:** Python `3.12+` (strict type annotations, `asyncio` event loop for 20 TPS tick synchronization)
- **Data Validation & Schemas:** `Pydantic >= 2.9` (`BaseModel`, `ConfigDict(strict=True, extra="forbid")`, `@field_validator`, `@model_validator`)
- **Testing Framework:** `pytest >= 8.3`, `pytest-asyncio`, `pytest-cov` (100% deterministic offline unit/edge-case test suite)
- **Target Game Environment:** Java Minecraft `26.3` (Fabric Loader via **Prism Launcher** local instance)
- **Zero-Cost AI Roster:**
  - **Chief Architect & Staff Reviewer:** Google Gemini 1.5 Pro (`gemini-1.5-pro` via Free Tier API / `scripts/claude_reviewer.py`)
  - **QA Product Manager:** Groq Cloud Llama 3.3 70B (`llama-3.3-70b-versatile` via Free Tier API / `scripts/ai_bridge.py`)
  - **Infinite Laborer (Code & In-Game Planner):** Local Ollama `qwen2.5:14b-instruct-q4_K_M` (14B Q4_K_M running locally on Apple Silicon unified memory at `http://127.0.0.1:11434` / `scripts/ollama_worker.py`)
  - **QA Debugger:** OpenRouter DeepSeek R1 (`deepseek/deepseek-r1:free` via Free Tier API / `scripts/deepseek_debugger.py`)
  - **General Contractor:** Autonomous Orchestrator (`scripts/autonomous_orchestrator.py` & `scripts/self_heal_runner.py`)

### 1.3 Installed Prism Launcher Mod Integration Matrix (Minecraft 26.3)
Every module in `src/` natively reads telemetry from and dispatches keybinds/API calls to the 14 installed Fabric mods:

| Installed Mod | System Integration Role in `PrismPuppet-26.3` |
| :--- | :--- |
| **Fabulously Optimized** | Baseline Fabric performance profile; monitors client FPS/tick-lag spikes to throttle pathfinding lookahead and prevent rubber-banding. |
| **Advanced XRay (Fabric Edition)** | Programmatically toggles XRay profiles and queries exposed target block coordinates (ores, spawners, chests) within loaded chunk radii without blind strip-mining. |
| **AppleSkin** | Reads exact `saturation`, `exhaustion`, and food item restoration values (`hunger_gain`, `saturation_gain`) to trigger optimal eating ticks during combat and sprinting. |
| **BBE (Better Block Entities)** | Reads culled/optimized block entity states (`Chest`, `ShulkerBox`, `Sign`, `Bed`, `Bell`) within chunk render distance for container indexing. |
| **Gamma Utils** | Dynamically overrides client gamma (`0%` to `1500%` / Night Vision mode) when mining subterranean caverns, conserving torches while maintaining `MiniHUD` spawn-proofing awareness. |
| **Inventory HUD+** | Streams real-time armor slot durability, main/offhand tool durability, active status effect timers, and free inventory slot counts. |
| **InvMove** | Enables continuous WASD movement, jumping, and sprinting packets while container GUIs (`Chest`, `Anvil`, `Inventory`, `Litematica` config, `Villager` trade) are open to evade ambush mobs. |
| **Litematica** | Loads `.litematic` files, parses required material manifests, anchors schematic origins, steps layer-by-layer ranges, and triggers `easyPlaceUse` / Printer placement ticks. |
| **MaLiLib** | Dispatches deterministic hotkey combinations and JSON config mutations to control `Litematica` and `MiniHUD` states programmatically. |
| **MiniHUD** | Queries block-light levels (`< 1` hostile spawn threshold), slime chunk booleans, structure bounding boxes, and 128-block mob despawn spheres. |
| **Modern Armor Bar** | Tracks segmented armor points, armor toughness, and protection enchantment reduction percentages for combat survival math. |
| **Shulker Box Tooltip** | Inspects nested `BlockEntityTag` item arrays inside Shulker Boxes, Ender Chests, and Bundles directly from player inventory slots without placing the box in-world. |
| **Ultimate Villager Armour** | Reads villager equipment slots and automates equipping high-tier armor/thorns gear onto trading hall villagers via dispenser or interaction packets. |
| **Xaero's Minimap & World Map** | Parses waypoint files, reads deathpoints for autonomous corpse recovery, queries mapped surface heights/biomes, and writes discovered resource waypoints. |

### 1.4 Complete Directory Structure
```text
autonomous-workspace/
├── .env                                 # API keys (GROQ_API_KEY, OPENROUTER_API_KEY, GEMINI_API_KEY, OLLAMA_HOST)
├── .env.example                         # Environment template
├── .gitignore                           # Git ignore rules
├── README.md                            # Workspace documentation
├── config/
│   ├── mcp_servers.json                 # MCP server configuration
│   └── prism_instance.json              # Prism Launcher MC 26.3 path, port (25585), and MaLiLib hotkey bindings
├── logs/                                # PyTest failure logs & DeepSeek R1 surgical debug transcripts
├── scripts/
│   ├── ai_bridge.py                     # Zero-cost router (Groq, Ollama Qwen 2.5:14B, OpenRouter DeepSeek, Gemini)
│   ├── autonomous_orchestrator.py       # Master pipeline controller
│   ├── claude_reviewer.py               # Gemini 1.5 Pro git diff staff auditor
│   ├── deepseek_debugger.py             # OpenRouter DeepSeek R1 (:free) traceback surgical fixer
│   ├── ollama_worker.py                 # Local Qwen 2.5:14b-instruct-q4_K_M micro-task code generator
│   └── self_heal_runner.py              # Automated pytest runner + self-healing loop trigger
├── specs/
│   ├── MASTER_SPEC_TEMPLATE.md          # Base specification template
│   ├── MASTER_SPEC.md                   # This active project specification
│   └── AUDIT_REPORT.md                  # Generated by Gemini 1.5 Pro in Phase 5
├── src/
│   ├── __init__.py                      # Package root and version metadata
│   ├── app.py                           # Unified facade exporting all public classes/functions for test suite compatibility
│   ├── models/
│   │   ├── __init__.py
│   │   ├── world_state.py               # Vec3i, Vec3d, BlockState, EntityState, PlayerVitals (AppleSkin/ModernArmorBar)
│   │   ├── inventory.py                 # EnchantmentSpec, ItemStack, ShulkerContents (ShulkerBoxTooltip), InventoryState
│   │   ├── mods.py                      # XRayTarget, Waypoint (Xaero), LitematicaSchematicState, MiniHudOverlayState
│   │   └── tasks.py                     # ActionPrimitive, TaskNode, TaskStatus, PlanDAG
│   ├── bridge/
│   │   ├── __init__.py
│   │   ├── prism_launcher.py            # Prism Launcher 26.3 instance discovery, mod verification, & IPC handshake
│   │   └── packet_client.py             # Async JSON-RPC / WebSocket client puppeteering the open player session
│   ├── perception/
│   │   ├── __init__.py
│   │   ├── vitals_monitor.py            # AppleSkin hunger/saturation, Inventory HUD+ durability, Modern Armor Bar math
│   │   ├── spatial_scanner.py           # Advanced XRay ore targeting, MiniHUD light/despawn checks, BBE container scan
│   │   └── map_navigator.py             # Xaero's Minimap/World Map waypoint CRUD, deathpoint recovery, 3D A* routing
│   ├── mechanics/
│   │   ├── __init__.py
│   │   ├── tool_selector.py             # Best-tool & enchantment scorer (Fortune vs Silk Touch, Efficiency, Mending guard)
│   │   ├── block_interactor.py          # Chests, Anvils (XP/repair/combine), Enchanting, Furnaces, InvMove GUI movement
│   │   ├── combat_engine.py             # Threat scoring, crit-jump timing, shield parry, kiting, Ultimate Villager Armour
│   │   └── litematica_builder.py        # MaLiLib/Litematica schematic loading, material diffing, layer-by-layer printing
│   └── agent/
│       ├── __init__.py
│       ├── qwen_planner.py              # Local Ollama (qwen2.5:14b-instruct-q4_K_M) HTN goal decomposer & JSON validator
│       └── autonomous_loop.py           # Walk-away tick supervisor: perception -> plan -> act -> self-heal -> checkpoint
└── tests/
    ├── __init__.py
    ├── conftest.py                      # Deterministic fixtures for MC 26.3 player state, inventory, mods, and mock Ollama
    ├── test_master.py                   # Master unit & edge-case suite generated by Groq Llama 3.3 70B
    ├── test_models_and_mods.py          # Strict Pydantic validation tests for world, inventory, and 14 mod schemas
    ├── test_mechanics_and_combat.py     # Tool selection, Mending protection, Anvil XP math, InvMove, and combat tests
    └── test_planner_and_loop.py         # Qwen 2.5:14B HTN planner, Litematica builder, and walk-away recovery tests
```

## 2. Phase 2: Specific Prompt for Groq (Llama 3.3 70B) — Strict PyTest Suite & Edge Cases

Before any application code is written in `src/`, the orchestrator sends the following exact prompt to **Groq (`llama-3.3-70b-versatile`)** via `query_product_manager()` in `scripts/ai_bridge.py` to generate the test suite:

```text
You are the Senior QA Product Manager for Project PrismPuppet-26.3. Review this MASTER_SPEC.md and generate a complete, deterministic, offline-runnable PyTest unit and edge-case test suite in Python 3.12 (`tests/test_master.py`) using `pytest` and `pydantic`.

CRITICAL CONSTRAINTS:
1. Output ONLY valid, executable Python 3.12 code. Do not wrap in conversational prose.
2. All external I/O (Prism Launcher IPC socket `127.0.0.1:25585` and Ollama HTTP `http://127.0.0.1:11434/api/generate`) MUST be mocked or tested via deterministic dependency injection so tests execute in <2 seconds with zero network calls.
3. Import all target symbols from `src.app` (which re-exports all models, bridge clients, perception analyzers, mechanics engines, and agent controllers).

REQUIRED PUBLIC CONTRACTS & TEST CASES TO VERIFY:

A. Strict Pydantic Models (`src/models/`):
   - `Vec3i(x: int, y: int, z: int)`: `.distance_to(other: Vec3i) -> float`, `.manhattan_to(other: Vec3i) -> int`. Test negative coordinates (e.g., deepslate layer `y=-59`) and world height bounds (`y in [-64, 320]`).
   - `EnchantmentSpec(id: str, level: int)`: Reject `level < 1` or `level > 5` with `ValidationError`.
   - `ItemStack(item_id: str, count: int, max_count: int = 64, durability: int | None = None, max_durability: int | None = None, enchantments: list[EnchantmentSpec] = [], shulker_contents: list['ItemStack'] = [])`:
     - Reject `count < 1` or `count > max_count`.
     - Reject `durability > max_durability` or negative durability.
     - Computed property `.remaining_durability_ratio -> float | None`.
     - Support nested `shulker_contents` (`Shulker Box Tooltip` mod integration) and verify recursive item counting across inventory + nested shulkers via `InventoryState.count_total_item(item_id: str) -> int`.
   - `PlayerVitals(health: float, max_health: float = 20.0, hunger: int = 20, saturation: float = 5.0, exhaustion: float = 0.0, armor_points: int = 0, armor_toughness: float = 0.0, gamma_level: float = 1.0)`:
     - Validate `AppleSkin` telemetry (`0.0 <= saturation <= 20.0`, `0.0 <= exhaustion <= 4.0`).
     - Validate `Gamma Utils` override (`0.0 <= gamma_level <= 15.0`).
   - `PrismInstanceConfig(mc_version: str, loader: str, mods: list[str], ipc_host: str = "127.0.0.1", ipc_port: int = 25585)`:
     - Enforce `mc_version == "26.3"` and verify all 14 required mods (`Fabulously Optimized`, `Advanced xRay Fabric edition`, `AppleSkin`, `BBE`, `Gamma Utils`, `Inventory HUD +`, `InvMove`, `Litematica`, `MaLiLib`, `MiniHUD`, `Modern Armor Bar`, `Shulker Box Tooltip`, `Ultimate Villager Armour`, `Xaero's Minimap`, `Xaero's World Map`) via `validate_required_mods() -> list[str]` (returns missing mod names, empty list when all present).

B. Tool & Enchantment Selector (`ToolSelector`):
   - `select_best_tool(block_id: str, inventory: InventoryState, prefer_silk_touch: bool = False) -> ItemStack | None`:
     - When mining `minecraft:diamond_ore` with `prefer_silk_touch=False`, rank a `Fortune III` pickaxe higher than an unenchanted or `Silk Touch` pickaxe.
     - When mining `minecraft:ender_chest` or `minecraft:glass` or `prefer_silk_touch=True`, select the `Silk Touch` tool.
     - EDGE CASE (Mending Preservation Guard): Any tool with `EnchantmentSpec(id="mending", level=1)` and `durability <= 10` MUST be excluded from selection so it is never broken, falling back to a secondary tool or raising `ToolPreservationError` if no safe harvest tool exists.

C. Block, Container & Anvil Interaction (`BlockInteractor`):
   - `calculate_anvil_operation(left: ItemStack, right: ItemStack, rename_text: str | None = None, prior_work_penalty: int = 0) -> dict`:
     - Calculate exact XP level cost and combined enchantments.
     - EDGE CASE: Raise `AnvilTooExpensiveError` if total XP cost `>= 40` in survival mode.
   - `build_container_transfer_packet(container_type: str, slot_from: int, slot_to: int, inv_move_active: bool = True, dodge_vector: tuple[float, float] = (0.0, 0.0)) -> dict`:
     - Verify `InvMove` integration allows non-zero `dodge_vector` (`strafe`, `forward`) simultaneously during open GUI interactions (`chest`, `shulker_box`, `anvil`, `villager`) without closing the screen.

D. Mod-Aware Perception & Combat (`SpatialScanner`, `MapNavigator`, `CombatEngine`):
   - `SpatialScanner.find_xray_targets(targets: list[XRayTarget], player_pos: Vec3i, max_radius: int = 64) -> list[XRayTarget]`: Filter and sort `Advanced XRay` blocks by Euclidean distance.
   - `SpatialScanner.needs_gamma_boost(light_level: int, current_gamma: float) -> float`: Using `MiniHUD` light telemetry, return `15.0` (1500% `Gamma Utils` fullbright) when `light_level <= 7`, and `1.0` when surface-lit.
   - `MapNavigator.select_recovery_waypoint(waypoints: list[Waypoint], player_pos: Vec3i) -> Waypoint | None`: Prioritize latest `Xaero's Minimap` deathpoint when recovering dropped items.
   - `CombatEngine.decide_combat_tick(vitals: PlayerVitals, hostiles: list[EntityState], inventory: InventoryState) -> dict`:
     - Trigger immediate shield block (`use_offhand=True`) and backward kiting when a `minecraft:creeper` is within `distance <= 4.5` or fuse state `> 0`.
     - Trigger `AppleSkin` optimal food consumption when `vitals.health < 14.0` and `vitals.hunger < 20` or `vitals.saturation < 1.0`.
     - Support `Ultimate Villager Armour` loadout packet generation (`equip_villager_armor(villager_id: int, inventory: InventoryState) -> list[int]`) selecting highest protection armor slots for nearby friendly villagers.

E. Litematica Schematic Builder & Local Qwen 2.5:14B Planner (`LitematicaBuilder`, `QwenPlanner`, `AutonomousLoop`):
   - `LitematicaBuilder.compute_missing_materials(schematic_requirements: dict[str, int], inventory: InventoryState) -> dict[str, int]`: Subtract both direct inventory items and nested `Shulker Box Tooltip` items from required counts.
   - `QwenPlanner.decompose_goal(goal: str, world_summary: dict, llm_callable) -> PlanDAG`:
     - Parse JSON task graphs returned by `qwen2.5:14b-instruct-q4_K_M` (including stripping `<think>` tags or markdown code fences).
     - EDGE CASE: Detect and reject cyclic task dependencies (`CycleDetectedError`) or unknown action primitives (`ValidationError`).
   - `AutonomousLoop.run_single_tick() -> dict`: Verify self-healing fallback when a task node fails (e.g., pickaxe durability hits Mending threshold mid-mine -> injects repair/resupply subtask or switches to backup tool from Shulker Box).
```

## 3. Phase 3: Numbered Micro-Tasks for Local Ollama (`qwen2.5:14b-instruct-q4_K_M`)

The orchestrator delegates implementation into **15 atomic micro-tasks**, each strictly **under 100 lines of code (<100 LOC)**, executed sequentially via local Ollama (`qwen2.5:14b-instruct-q4_K_M`) on Apple Silicon using `scripts/ollama_worker.py`.

1. **Micro-Task 1: Spatial & Player Vitals Pydantic Models (`src/models/world_state.py`, Target: <85 LOC)**
   - **Command:**
     ```bash
     python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/models/world_state.py -p "Write Python 3.12 Pydantic v2 models in src/models/world_state.py (<85 lines): Vec3i(x:int, y:int, z:int) with validator ensuring -64 <= y <= 320 and methods distance_to(other: Vec3i) -> float and manhattan_to(other: Vec3i) -> int; BlockState(pos: Vec3i, block_id: str, light_level: int = 15); EntityState(entity_id: int, entity_type: str, pos: Vec3i, health: float, distance: float, is_hostile: bool = False, creeper_fuse: int = 0); PlayerVitals(health: float = 20.0, max_health: float = 20.0, hunger: int = 20, saturation: float = 5.0, exhaustion: float = 0.0, armor_points: int = 0, armor_toughness: float = 0.0, gamma_level: float = 1.0) validating 0.0 <= saturation <= 20.0, 0.0 <= exhaustion <= 4.0, and 0.0 <= gamma_level <= 15.0. Output ONLY raw Python code."
     ```

2. **Micro-Task 2: Inventory, Enchantments & Shulker Tooltip Models (`src/models/inventory.py`, Target: <90 LOC)**
   - **Command:**
     ```bash
     python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/models/inventory.py -p "Write Python 3.12 Pydantic v2 models in src/models/inventory.py (<90 lines): EnchantmentSpec(id: str, level: int) validating 1 <= level <= 5; ItemStack(item_id: str, count: int = 1, max_count: int = 64, slot: int = 0, durability: int | None = None, max_durability: int | None = None, enchantments: list[EnchantmentSpec] = [], food_hunger: int = 0, food_saturation: float = 0.0, shulker_contents: list['ItemStack'] = []) validating 1 <= count <= max_count and valid durability bounds, with property remaining_durability_ratio -> float | None and method get_enchant_level(enchant_id: str) -> int; InventoryState(items: list[ItemStack] = [], free_slots: int = 36) with method count_total_item(item_id: str) -> int that sums matching items in both main inventory and nested shulker_contents (Shulker Box Tooltip support). Output ONLY raw Python code."
     ```

3. **Micro-Task 3: Fabric Mod Telemetry Schemas (`src/models/mods.py`, Target: <85 LOC)**
   - **Command:**
     ```bash
     python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/models/mods.py -p "Write Python 3.12 Pydantic v2 models in src/models/mods.py (<85 lines): REQUIRED_MODS_26_3 constant list containing exact strings ['Fabulously Optimized', 'Advanced xRay Fabric edition', 'AppleSkin', 'BBE', 'Gamma Utils', 'Inventory HUD +', 'InvMove', 'Litematica', 'MaLiLib', 'MiniHUD', 'Modern Armor Bar', 'Shulker Box Tooltip', 'Ultimate Villager Armour', 'Xaero\'s Minimap', 'Xaero\'s World Map']; PrismInstanceConfig(mc_version: str = '26.3', loader: str = 'fabric', mods: list[str] = REQUIRED_MODS_26_3, ipc_host: str = '127.0.0.1', ipc_port: int = 25585) validating mc_version == '26.3' and providing validate_required_mods() -> list[str]; XRayTarget(block_id: str, pos: Vec3i, priority: int = 1); Waypoint(name: str, pos: Vec3i, dimension: str = 'overworld', is_deathpoint: bool = False, timestamp: int = 0); LitematicaSchematicState(name: str, origin: Vec3i, current_layer: int = 0, total_layers: int = 1, required_materials: dict[str, int] = {}). Output ONLY raw Python code."
     ```

4. **Micro-Task 4: HTN Task & Plan DAG Schemas (`src/models/tasks.py`, Target: <85 LOC)**
   - **Command:**
     ```bash
     python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/models/tasks.py -p "Write Python 3.12 Pydantic v2 models in src/models/tasks.py (<85 lines): CycleDetectedError(ValueError) exception; ActionPrimitive Literal['mine_block', 'move_to', 'interact_block', 'craft_item', 'combat_engage', 'eat_food', 'toggle_xray', 'set_gamma', 'print_litematica', 'equip_villager']; TaskStatus Literal['pending', 'running', 'completed', 'failed']; TaskNode(task_id: str, action: ActionPrimitive, params: dict = {}, dependencies: list[str] = [], status: TaskStatus = 'pending', retries: int = 0); PlanDAG(goal: str, tasks: list[TaskNode]) with model_validator verifying all dependency IDs exist and using DFS cycle detection to raise CycleDetectedError on any circular dependency, plus method next_ready_tasks() -> list[TaskNode]. Output ONLY raw Python code."
     ```

5. **Micro-Task 5: Prism Launcher 26.3 Instance & MaLiLib Bridge (`src/bridge/prism_launcher.py`, Target: <80 LOC)**
   - **Command:**
     ```bash
     python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/bridge/prism_launcher.py -p "Write Python 3.12 module src/bridge/prism_launcher.py (<80 lines) implementing PrismLauncherBridge(config: PrismInstanceConfig). Include verify_environment() -> dict checking mc_version == '26.3' and calling validate_required_mods() (raising RuntimeError if required mods are missing); build_malilib_hotkey_packet(mod_name: str, action_key: str, enabled: bool) -> dict supporting 'Litematica', 'MiniHUD', 'Advanced xRay Fabric edition', and 'Gamma Utils'; and build_prism_launch_args(instance_name: str) -> list[str]. Output ONLY raw Python code."
     ```

6. **Micro-Task 6: Local Player Puppet Packet Client (`src/bridge/packet_client.py`, Target: <85 LOC)**
   - **Command:**
     ```bash
     python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/bridge/packet_client.py -p "Write Python 3.12 module src/bridge/packet_client.py (<85 lines) implementing PuppetPacketClient(host: str = '127.0.0.1', port: int = 25585, transport=None). Implement send_action(action_type: str, payload: dict) -> dict that uses injectable transport callable if provided (for offline unit tests) or returns a deterministic ack dict {'status': 'ok', 'action': action_type, 'payload': payload}; plus helper builders look_at(pos: Vec3i) -> dict, input_movement(forward: float, strafe: float, jump: bool = False, sprint: bool = False, gui_open: bool = False) -> dict enforcing InvMove support when gui_open=True. Output ONLY raw Python code."
     ```

7. **Micro-Task 7: Vitals, AppleSkin & Inventory HUD+ Monitor (`src/perception/vitals_monitor.py`, Target: <80 LOC)**
   - **Command:**
     ```bash
     python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/perception/vitals_monitor.py -p "Write Python 3.12 module src/perception/vitals_monitor.py (<80 lines) implementing VitalsMonitor. Include should_eat(vitals: PlayerVitals, in_combat: bool = False) -> bool using AppleSkin saturation/hunger thresholds (eat in combat if health < 15.0 and saturation < 2.0, or out of combat if hunger <= 16); select_optimal_food(vitals: PlayerVitals, inventory: InventoryState) -> ItemStack | None choosing food that maximizes AppleSkin saturation_gain without wasting hunger overflow; and check_armor_alert(inventory: InventoryState, min_ratio: float = 0.15) -> list[ItemStack] for Inventory HUD+ / Modern Armor Bar low durability warnings. Output ONLY raw Python code."
     ```

8. **Micro-Task 8: Advanced XRay, MiniHUD & BBE Spatial Scanner (`src/perception/spatial_scanner.py`, Target: <85 LOC)**
   - **Command:**
     ```bash
     python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/perception/spatial_scanner.py -p "Write Python 3.12 module src/perception/spatial_scanner.py (<85 lines) implementing SpatialScanner. Include find_xray_targets(targets: list[XRayTarget], player_pos: Vec3i, max_radius: int = 64) -> list[XRayTarget] filtering by distance_to(player_pos) <= max_radius and sorting by (priority, distance); needs_gamma_boost(light_level: int, current_gamma: float) -> float returning 15.0 (Gamma Utils fullbright) if light_level <= 7 else 1.0; and find_hostile_spawn_spots(blocks: list[BlockState]) -> list[Vec3i] using MiniHUD light rules (light_level == 0). Output ONLY raw Python code."
     ```

9. **Micro-Task 9: Xaero's Minimap/World Map Navigator & A* Router (`src/perception/map_navigator.py`, Target: <95 LOC)**
   - **Command:**
     ```bash
     python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/perception/map_navigator.py -p "Write Python 3.12 module src/perception/map_navigator.py (<95 lines) implementing MapNavigator. Include select_recovery_waypoint(waypoints: list[Waypoint], player_pos: Vec3i) -> Waypoint | None prioritizing is_deathpoint=True sorted by latest timestamp descending, else nearest waypoint; and compute_astar_path(start: Vec3i, goal: Vec3i, blocked: set[ tuple[int,int,int] ] | None = None, max_steps: int = 512) -> list[Vec3i] implementing 3D 6-neighbor A* pathfinding with Manhattan heuristic. Output ONLY raw Python code."
     ```

10. **Micro-Task 10: Tool & Enchantment Selector with Mending Guard (`src/mechanics/tool_selector.py`, Target: <90 LOC)**
    - **Command:**
      ```bash
      python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/mechanics/tool_selector.py -p "Write Python 3.12 module src/mechanics/tool_selector.py (<90 lines) defining ToolPreservationError(RuntimeError) and ToolSelector. Implement select_best_tool(block_id: str, inventory: InventoryState, prefer_silk_touch: bool = False) -> ItemStack | None. Map block_id substrings ('ore', 'stone', 'deepslate', 'obsidian', 'ender_chest' -> 'pickaxe'; 'log', 'planks' -> 'axe'; 'dirt', 'sand', 'gravel' -> 'shovel'). Exclude any item with 'mending' enchantment and durability is not None and durability <= 10 (if only Mending-protected critical tools exist for that block, raise ToolPreservationError). Score candidates by material tier (netherite>diamond>iron>stone>wood), efficiency level, silk_touch (if prefer_silk_touch or block_id in ['minecraft:ender_chest', 'minecraft:glass']), else fortune level for ores. Output ONLY raw Python code."
      ```

11. **Micro-Task 11: Block, Chest, Anvil & InvMove GUI Interactor (`src/mechanics/block_interactor.py`, Target: <95 LOC)**
    - **Command:**
      ```bash
      python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/mechanics/block_interactor.py -p "Write Python 3.12 module src/mechanics/block_interactor.py (<95 lines) defining AnvilTooExpensiveError(ValueError) and BlockInteractor. Implement calculate_anvil_operation(left: ItemStack, right: ItemStack, rename_text: str | None = None, prior_work_penalty: int = 0) -> dict merging enchantments (incrementing level by 1 if equal and <5, else max), computing xp_cost = prior_work_penalty + sum(e.level for e in right.enchantments) + (1 if rename_text else 0), and raising AnvilTooExpensiveError if xp_cost >= 40; plus build_container_transfer_packet(container_type: str, slot_from: int, slot_to: int, inv_move_active: bool = True, dodge_vector: tuple[float, float] = (0.0, 0.0)) -> dict supporting InvMove simultaneous movement while chest/anvil/shulker/villager GUIs are open. Output ONLY raw Python code."
      ```

12. **Micro-Task 12: Combat Engine & Ultimate Villager Armour Manager (`src/mechanics/combat_engine.py`, Target: <90 LOC)**
    - **Command:**
      ```bash
      python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/mechanics/combat_engine.py -p "Write Python 3.12 module src/mechanics/combat_engine.py (<90 lines) implementing CombatEngine. Include decide_combat_tick(vitals: PlayerVitals, hostiles: list[EntityState], inventory: InventoryState) -> dict returning action dict with keys ('mode', 'target_id', 'use_offhand', 'strafe', 'forward', 'crit_jump', 'eat_food'); if any creeper has distance <= 4.5 or creeper_fuse > 0, return mode='evade_creeper', use_offhand=True, forward=-1.0; if vitals.health < 14.0 and (vitals.hunger < 20 or vitals.saturation < 1.0), set eat_food=True; otherwise target nearest hostile with crit_jump=True. Also implement equip_villager_armor(villager_id: int, inventory: InventoryState) -> list[int] for Ultimate Villager Armour mod, returning slot indices of best helmet, chestplate, leggings, and boots in inventory. Output ONLY raw Python code."
      ```

13. **Micro-Task 13: Litematica Schematic & Shulker Material Builder (`src/mechanics/litematica_builder.py`, Target: <85 LOC)**
    - **Command:**
      ```bash
      python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/mechanics/litematica_builder.py -p "Write Python 3.12 module src/mechanics/litematica_builder.py (<85 lines) implementing LitematicaBuilder. Include compute_missing_materials(schematic_requirements: dict[str, int], inventory: InventoryState) -> dict[str, int] using inventory.count_total_item(block_id) (which includes nested Shulker Box Tooltip contents) and returning only items with deficit > 0; and build_printer_step(schematic: LitematicaSchematicState) -> dict advancing current_layer up to total_layers and emitting MaLiLib/Litematica easyPlaceUse packet payload. Output ONLY raw Python code."
      ```

14. **Micro-Task 14: Local Qwen 2.5:14B HTN Planner (`src/agent/qwen_planner.py`, Target: <95 LOC)**
    - **Command:**
      ```bash
      python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/agent/qwen_planner.py -p "Write Python 3.12 module src/agent/qwen_planner.py (<95 lines) implementing QwenPlanner(model_name: str = 'qwen2.5:14b-instruct-q4_K_M'). Implement decompose_goal(goal: str, world_summary: dict, llm_callable=None) -> PlanDAG. If llm_callable is provided, call it with a structured JSON prompt, strip any <think>...</think> blocks or ```json fences, parse into PlanDAG (validating TaskNodes and raising CycleDetectedError on cycles). Provide a deterministic fallback plan generator when llm_callable is None so offline tests and emergency fallback plans always succeed. Output ONLY raw Python code."
      ```

15. **Micro-Task 15: Walk-Away Autonomous Loop & Unified `src/app.py` Facade (`src/agent/autonomous_loop.py` & `src/app.py`, Target: <95 LOC each)**
    - **Command:**
      ```bash
      python3 scripts/ollama_worker.py -m qwen2.5:14b-instruct-q4_K_M -o src/agent/autonomous_loop.py -p "Write Python 3.12 module src/agent/autonomous_loop.py (<95 lines) implementing AutonomousLoop(config: PrismInstanceConfig, vitals: PlayerVitals, inventory: InventoryState, plan: PlanDAG). Implement run_single_tick(hostiles: list[EntityState] = [], light_level: int = 15) -> dict that: (1) checks CombatEngine if hostiles exist, (2) adjusts Gamma Utils via SpatialScanner.needs_gamma_boost(light_level, vitals.gamma_level), (3) executes next_ready_tasks() from PlanDAG, catching ToolPreservationError to automatically inject a 'move_to' / 'interact_block' shulker resupply or anvil repair TaskNode without crashing. Then write src/app.py re-exporting all models, exceptions, and classes from src.models, src.bridge, src.perception, src.mechanics, and src.agent. Output ONLY raw Python code."
      ```

## 4. Phase 4: Self-Healing & Surgical Debugging via OpenRouter (`deepseek/deepseek-r1:free`)

Whenever `pytest` fails during or after Phase 3 micro-task execution, the orchestrator executes an automated, zero-cost self-healing loop:

1. **Execute Test Suite & Capture Traceback:**
   The orchestrator runs `scripts/self_heal_runner.py`:
   ```bash
   python3 scripts/self_heal_runner.py --test-dir tests --max-retries 3
   ```
   `self_heal_runner.py` invokes `pytest tests -v --tb=short`. If the return code is non-zero, stdout/stderr is written to `logs/failure_<YYYYMMDD_HHMMSS>.log`.

2. **Pipe Traceback + Failing Source Context to OpenRouter (`deepseek/deepseek-r1:free`):**
   The orchestrator invokes `scripts/deepseek_debugger.py` with the captured failure log and the implicated source file:
   ```bash
   python3 scripts/deepseek_debugger.py \
     --traceback-file logs/failure_<YYYYMMDD_HHMMSS>.log \
     --context src/app.py \
     --output-log logs/qa_debug_<YYYYMMDD_HHMMSS>.log
   ```
   Inside `scripts/ai_bridge.py`, `query_qa_debugger()` sends the traceback and source context to `https://openrouter.ai/api/v1/chat/completions` with `"model": "deepseek/deepseek-r1:free"` and `"temperature": 0.1` (with automatic zero-cost fallback to Groq `deepseek-r1-distill-llama-70b` or local Ollama `qwen2.5:14b-instruct-q4_K_M` if rate-limited).

3. **Apply Surgical Patch & Re-Verify:**
   The orchestrator strips `<think>...</think>` reasoning blocks and markdown code fences from the DeepSeek R1 response, writes the patched Python module back to `src/`, and re-runs `pytest tests -v --tb=short` until `ret_code == 0` (100% green test suite).

## 5. Phase 5: Staff-Level Security, Architecture & Code Quality Audit via Google Gemini 1.5 Pro

Once `pytest` passes with zero failures, the orchestrator sends the complete git diff to **Google Gemini 1.5 Pro (`gemini-1.5-pro`)** on the Free Tier for a staff-level review:

1. **Generate & Audit Git Diff:**
   ```bash
   python3 scripts/claude_reviewer.py --output specs/AUDIT_REPORT.md
   ```
2. **Audit Scope Enforced by `scripts/claude_reviewer.py` & `query_staff_reviewer()`:**
   - **Security & Sandbox Isolation:** Verifies that the local IPC socket (`127.0.0.1:25585`) binds strictly to loopback, prevents arbitrary shell injection from LLM-generated task parameters, and enforces strict Pydantic schema validation (`extra="forbid"` / bounded types) on all `qwen2.5:14b-instruct-q4_K_M` JSON outputs.
   - **Architectural Integrity:** Confirms clean separation between `src/models/`, `src/bridge/`, `src/perception/`, `src/mechanics/`, and `src/agent/`, with every file adhering to the modular micro-task design.
   - **Mod & Game-Loop Safety:** Verifies Mending tool preservation (`durability <= 10` cutoff), Anvil level cap enforcement (`xp_cost < 40`), `InvMove` non-blocking GUI dodge packets, and `Shulker Box Tooltip` recursive inventory resolution.
   - **Output Artifact:** Writes the full audit report and sign-off to `specs/AUDIT_REPORT.md`.

## 6. Phase 6: Git Commit, Remote GitHub Push & Pull Request Automation

After `pytest` passes 100% of unit and edge-case tests and `specs/AUDIT_REPORT.md` is generated by Google Gemini 1.5 Pro, the orchestrator finalizes version control and opens the Pull Request:

```bash
# 1. Create and switch to a dedicated feature branch
git checkout -b feat/prism-puppet-mc26-3-agent

# 2. Verify repository status and stage all verified source, test, and spec artifacts
git status
git add specs/MASTER_SPEC.md specs/AUDIT_REPORT.md src/ tests/

# 3. Commit passing code with structured conventional commit message
git commit -m "feat(mc-26.3): implement autonomous Qwen 2.5 14B player puppet and 14-mod bridge"

# 4. Push feature branch to remote GitHub repository
git push -u origin feat/prism-puppet-mc26-3-agent

# 5. Open Pull Request via GitHub CLI with architecture summary and audit reference
gh pr create \
  --title "feat(mc-26.3): Autonomous Qwen 2.5:14B Player Puppet & Prism Launcher 14-Mod Engine" \
  --body "## Summary
- Implements **PrismPuppet-26.3** autonomous player puppeteering architecture for Java Minecraft 26.3 via Prism Launcher.
- Integrates local **Ollama (`qwen2.5:14b-instruct-q4_K_M`)** HTN planning, **Shulker Box Tooltip** recursive inventory indexing, **Litematica + MaLiLib** schematic printing, **InvMove** GUI combat dodging, **Advanced XRay**, **Gamma Utils**, **MiniHUD**, **AppleSkin**, **Inventory HUD+**, **Modern Armor Bar**, **BBE**, **Ultimate Villager Armour**, and **Xaero's Minimap/World Map** navigation.
- Verified by Groq Llama 3.3 70B PyTest suite, OpenRouter DeepSeek R1 (:free) self-healing loop, and Google Gemini 1.5 Pro Staff Audit (\`specs/AUDIT_REPORT.md\`)." \
  --base main \
  --head feat/prism-puppet-mc26-3-agent
```

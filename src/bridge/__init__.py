from __future__ import annotations
from typing import Optional, Callable
from src.models import Vec3i, PrismInstanceConfig

def build_malilib_hotkey_packet(mod_name: str, action_key: str, enabled: bool) -> dict:
    return {
        "mod": mod_name,
        "action": action_key,
        "action_key": action_key,
        "enabled": enabled,
        "type": "malilib_hotkey_toggle"
    }

def build_prism_launch_args(instance_name: str) -> list[str]:
    return ["prism-launcher", "launch", instance_name]

class PrismLauncherBridge:
    def __init__(self, config: PrismInstanceConfig):
        self.config = config

    def verify_environment(self) -> dict:
        missing = self.config.validate_required_mods()
        if missing:
            raise RuntimeError(f"Missing required Fabric mods: {missing}")
        return {"status": "ok", "mc_version": self.config.mc_version, "loader": self.config.loader}

class PuppetPacketClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 25585, transport: Optional[Callable] = None):
        self.host = host
        self.port = port
        self.transport = transport

    def send_action(self, action_type: str, payload: dict) -> dict:
        if self.transport:
            return self.transport(action_type, payload)
        return {"status": "ok", "action": action_type, "payload": payload}

    def look_at(self, pos: Vec3i) -> dict:
        return self.send_action("look_at", {"x": pos.x, "y": pos.y, "z": pos.z})

    def input_movement(self, forward: float, strafe: float, jump: bool = False, sprint: bool = False, gui_open: bool = False) -> dict:
        return self.send_action("movement", {
            "forward": forward,
            "strafe": strafe,
            "jump": jump,
            "sprint": sprint,
            "gui_open": gui_open,
            "inv_move": gui_open
        })

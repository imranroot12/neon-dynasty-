"""Generate a 100k candidate book for one Neon Dynasty mode.

This is intentionally pre-optimizer validation only. It never rewrites weights.
Usage: python run_candidate_mode.py base|basic|super|mystery
"""
import sys
from game_config import GameConfig
from gamestate import GameState
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if len(sys.argv) != 2 or sys.argv[1] not in {"base", "basic", "super", "mystery"}:
    raise SystemExit("usage: python run_candidate_mode.py <base|basic|super|mystery>")
mode = sys.argv[1]
config = GameConfig()
gs = GameState(config)
create_books(gs, config, {mode: 100000}, 50000, 10, True, False)
generate_configs(gs)
print(f"CANDIDATE_100K_MODE_COMPLETE {mode}")

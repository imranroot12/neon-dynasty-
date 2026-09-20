"""Official Engine Math SDK entrypoint for Neon Dynasty.

This follows the same orchestration pattern as the current Engine examples.
It intentionally requires Cargo for optimization and never substitutes a
client-side weighting pass for the official optimizer.
"""
import shutil
from game_config import GameConfig
from gamestate import GameState
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from utils.game_analytics.run_analysis import create_stat_sheet
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

NUM_THREADS = 10
RUST_THREADS = 20
BATCHING_SIZE = 50000
NUM_SIM_ARGS = {"base": int(1e5), "basic": int(1e5), "super": int(1e5), "mystery": int(1e5)}
TARGET_MODES = list(NUM_SIM_ARGS)

if __name__ == "__main__":
    if not shutil.which("cargo"):
        raise SystemExit("OFFICIAL_OPTIMIZER_BLOCKED: install Rust/Cargo before running production optimization")
    config = GameConfig()
    gamestate = GameState(config)
    OptimizationSetup(config)
    create_books(gamestate, config, NUM_SIM_ARGS, BATCHING_SIZE, NUM_THREADS, True, False)
    generate_configs(gamestate)
    OptimizationExecution().run_all_modes(config, TARGET_MODES, RUST_THREADS)
    generate_configs(gamestate)
    create_stat_sheet(gamestate)
    execute_all_tests(config)
    print("OFFICIAL_PIPELINE_COMPLETE")

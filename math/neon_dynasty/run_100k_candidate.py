"""Generate 100k-per-mode books without optimization for diversity validation.

This is a pre-optimizer candidate run. It must not be labeled as the final
publication math because the official optimizer is deliberately not invoked.
"""
from game_config import GameConfig
from gamestate import GameState
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":
    config = GameConfig(); gs = GameState(config)
    create_books(gs, config, {"base":100000,"basic":100000,"super":100000,"mystery":100000}, 50000, 10, True, False)
    generate_configs(gs)
    print("CANDIDATE_100K_PER_MODE_COMPLETE")

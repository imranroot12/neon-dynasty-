"""Neon Dynasty optimization parameters for the official Engine Math SDK."""
from optimization_program.optimization_config import (
    ConstructScaling, ConstructParameters, ConstructConditions,
    ConstructFenceBias, verify_optimization_input,
)
from game_config import GameConfig

class OptimizationSetup:
    def __init__(self, game_config: GameConfig):
        self.game_config = game_config
        caps = {m.get_name(): m.get_wincap() for m in game_config.bet_modes}
        modes = {}
        # Base is optimized against basegame contribution; buy modes are
        # optimized against the freegame contribution because their entry
        # cost is the mode's buy multiplier.
        for name in ("base", "basic", "super", "mystery"):
            is_base = name == "base"
            modes[name] = {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.001, av_win=caps[name], search_conditions=caps[name]
                    ).return_dict(),
                    "basegame": ConstructConditions(
                        rtp=0.959 if is_base else 0.0,
                        hr=3.5 if is_base else "x",
                    ).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.0 if is_base else 0.959,
                        hr=200 if not is_base else "x",
                    ).return_dict(),
                },
                "scaling": ConstructScaling([
                    {"criteria": "basegame" if is_base else "freegame", "scale_factor": 0.8, "win_range": (20, 50), "probability": 1.0},
                    {"criteria": "basegame" if is_base else "freegame", "scale_factor": 0.8, "win_range": (1000, 2000), "probability": 1.0},
                    {"criteria": "basegame" if is_base else "freegame", "scale_factor": 1.2, "win_range": (3000, 4000), "probability": 1.0},
                ]).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50] if not is_base else [50, 100, 200],
                    test_weights=[0.6, 0.2, 0.2] if not is_base else [0.3, 0.4, 0.3],
                    score_type="rtp",
                ).return_dict(),
            }
        self.game_config.opt_params = modes
        verify_optimization_input(self.game_config, self.game_config.opt_params)

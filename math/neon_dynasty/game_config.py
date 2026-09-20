"""Neon Dynasty — Stake Engine Math SDK configuration.

Build 43 uses the official cluster SDK structure as its math foundation.
This is an implementation scaffold; RTP must be certified with the production
optimizer/simulation pipeline before submission.
"""
import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "0_0_neon"
        self.provider_number = 0
        self.provider_name = "Voltix Games"
        self.game_name = "Neon Dynasty"
        self.working_name = "Neon Dynasty"
        self.wincap = 20000.0
        self.win_type = "cluster"
        self.rtp = 0.96
        self.construct_paths(self.game_id)

        self.num_reels = 6
        self.num_rows = [5] * 6

        # 5+ connected symbols pay. Values are the math scaffold and are not
        # represented as a certified 96.0% RTP claim.
        groups = {
            "H1": [6.45, 12.9, 22.575, 32.25, 51.6, 77.4, 116.1, 154.8, 206.4, 283.8, 387.0, 516.0, 709.5, 967.5, 1290.0, 1806.0, 2322.0, 2838.0, 3870.0, 5160.0, 6450.0, 8385.0, 10320.0, 12900.0, 16125.0, 19350.0],
            "H2": [5.16, 10.32, 18.06, 25.8, 41.28, 61.92, 92.88, 123.84, 165.12, 227.04, 309.6, 412.8, 567.6, 774.0, 1032.0, 1444.8, 1857.6, 2270.4, 3096.0, 4128.0, 5160.0, 6708.0, 8256.0, 10320.0, 12900.0, 15480.0],
            "H3": [3.87, 7.74, 13.545, 19.35, 30.96, 46.44, 69.66, 92.88, 123.84, 170.28, 232.2, 309.6, 425.7, 580.5, 774.0, 1083.6, 1393.2, 1702.8, 2322.0, 3096.0, 3870.0, 5031.0, 6192.0, 7740.0, 9675.0, 11610.0],
            "H4": [3.225, 6.45, 11.61, 16.125, 25.8, 38.7, 58.05, 77.4, 103.2, 141.9, 193.5, 258.0, 354.75, 483.75, 645.0, 903.0, 1161.0, 1419.0, 1935.0, 2580.0, 3225.0, 4192.5, 5160.0, 6450.0, 8062.5, 9675.0],
            "L1": [1.935, 3.87, 6.45, 9.675, 15.48, 23.22, 34.83, 46.44, 61.92, 85.14, 116.1, 154.8, 212.85, 290.25, 387.0, 541.8, 696.6, 851.4, 1161.0, 1548.0, 1935.0, 2515.5, 3096.0, 3870.0, 4837.5, 5805.0],
            "L2": [1.548, 3.096, 5.16, 7.74, 12.384, 18.576, 27.864, 37.152, 49.536, 68.112, 92.88, 123.84, 170.28, 232.2, 309.6, 433.44, 557.28, 681.12, 928.8, 1238.4, 1548.0, 2012.4, 2476.8, 3096.0, 3870.0, 4644.0],
            "L3": [1.29, 2.58, 4.386, 6.45, 10.32, 15.48, 23.22, 30.96, 41.28, 56.76, 77.4, 103.2, 141.9, 193.5, 258.0, 361.2, 464.4, 567.6, 774.0, 1032.0, 1290.0, 1677.0, 2064.0, 2580.0, 3225.0, 3870.0],
            "L4": [1.032, 2.064, 3.612, 5.16, 8.256, 12.384, 18.576, 24.768, 33.024, 45.408, 61.92, 82.56, 113.52, 154.8, 206.4, 288.96, 371.52, 454.08, 619.2, 825.6, 1032.0, 1341.6, 1651.2, 2064.0, 2580.0, 3096.0],
        }
        pay_group = {}
        for sym, values in groups.items():
            for size, payout in enumerate(values, start=5):
                pay_group[((size, size), sym)] = payout
        self.paytable = self.convert_range_table(pay_group)

        self.include_padding = True
        self.special_symbols = {"wild": ["W"], "scatter": []}
        self.freespin_triggers = {self.basegame_type: {}, self.freegame_type: {}}
        self.anticipation_triggers = {self.basegame_type: 999, self.freegame_type: 999}
        self.maximum_board_mult = 50
        self.maximum_tumbles = 5

        self.reels = {}
        for name in ("BR0", "FR0", "WCAP"):
            self.reels[name] = self.read_reels_csv(os.path.join(self.reels_path, f"{name}.csv"))

        # RGS mode costs. Hidden Bonus is not a direct buy mode; it is an
        # outcome of Mystery Buy in GameState.
        self.bet_modes = [
            self._mode("base", 1.0),
            self._mode("basic", 100.0),
            self._mode("super", 200.0),
            self._mode("mystery", 500.0),
        ]

    def _mode(self, name, cost):
        return BetMode(
            name=name,
            cost=cost,
            rtp=self.rtp,
            max_win=self.wincap,
            auto_close_disabled=False,
            is_feature=(name != "base"),
            is_buybonus=(name != "base"),
            distributions=[
                Distribution(
                    criteria="basegame",
                    quota=1.0,
                    conditions={
                        "reel_weights": {
                            self.basegame_type: {"BR0": 1},
                            self.freegame_type: {"FR0": 1},
                        },
                        "force_wincap": False,
                        "force_freegame": False,
                    },
                )
            ],
        )

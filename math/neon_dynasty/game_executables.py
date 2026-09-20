from game_calculations import GameCalculations
from src.calculations.cluster import Cluster
from src.events.events import update_freespin_event


class GameExecutables(GameCalculations):
    def reset_grid_mults(self):
        self.position_multipliers = [[0 for _ in range(self.config.num_rows[r])] for r in range(self.config.num_reels)]

    def update_grid_mults(self):
        if self.win_data["totalWin"] > 0:
            for win in self.win_data["wins"]:
                for pos in win["positions"]:
                    r, row = pos["reel"], pos["row"]
                    self.position_multipliers[r][row] = min(max(self.position_multipliers[r][row] + 1, 1), self.config.maximum_board_mult)

    def get_clusters_update_wins(self):
        clusters = Cluster.get_clusters(self.board, "wild")
        data = {"totalWin": 0, "wins": []}
        self.board, self.win_data = self.evaluate_clusters_with_grid(
            self.config, self.board, clusters, self.position_multipliers,
            self.global_multiplier, data
        )
        Cluster.record_cluster_wins(self)
        self.win_manager.update_spinwin(self.win_data["totalWin"])
        self.win_manager.tumble_win = self.win_data["totalWin"]

    def update_freespin(self):
        self.fs += 1
        update_freespin_event(self)
        self.win_manager.reset_spin_win()
        self.win_data = {"totalWin": 0, "wins": []}

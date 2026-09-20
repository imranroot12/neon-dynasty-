import random
from src.events.events import reveal_event
from game_override import GameStateOverride
from game_events import add_event, BONUS_START, MYSTERY_REVEAL, DRAGON_METER, DRAGON_EVENT, BONUS_COMPLETE


class GameState(GameStateOverride):
    """Neon Dynasty game flow.

    Base spins tumble normally. Bonus modes are direct buys. Mystery Buy selects
    Basic/Super/Hidden from five sealed vaults; Hidden is never a standalone RGS
    buy mode.
    """
    def _spin_tumbles(self):
        self.create_board_reelstrips()
        reveal_event(self)
        self.get_clusters_update_wins()
        self.emit_tumble_win_events()
        if self.win_data["totalWin"] > 0:
            self._dragon_progress(min(25, max(5, int(self.win_data["totalWin"]))))
        tumble_count = 0
        while self.win_data["totalWin"] > 0 and not self.wincap_triggered and tumble_count < self.config.maximum_tumbles:
            self.tumble_game_board()
            self.get_clusters_update_wins()
            self.emit_tumble_win_events()
            tumble_count += 1
        self.set_end_tumble_event()

    def _bonus_start(self, mode):
        self.bonus_mode = mode
        if mode == "basic": self.tot_fs = 8
        elif mode == "super": self.tot_fs = 10
        else: self.tot_fs = 15
        add_event(self, BONUS_START, mode=mode, totalSpins=self.tot_fs)

    def _mystery_select(self):
        # Five independent sealed vaults. Selecting the best displayed vault
        # is intentionally not modeled as a player-choice edge; one vault is
        # selected by the RGS outcome.
        weights = ["basic"] * 70 + ["super"] * 24 + ["hidden"] * 6
        vaults = [random.choice(weights) for _ in range(5)]
        selected = random.choice(vaults)
        add_event(self, MYSTERY_REVEAL, vaults=vaults, selected=selected)
        return selected

    def _dragon_progress(self, amount=10):
        self.dragon_meter = min(100, self.dragon_meter + amount)
        add_event(self, DRAGON_METER, value=self.dragon_meter)
        if self.dragon_meter >= 100:
            event = random.choice(["wildStorm", "mysteryStorm", "multiplierDrop", "reelExpansion", "symbolUpgrade"])
            add_event(self, DRAGON_EVENT, event=event, multiplier=self.global_multiplier)
            self.dragon_meter = 0
            add_event(self, DRAGON_METER, value=0)

    def run_freespin(self):
        while self.fs < self.tot_fs:
            self.update_freespin()
            self.create_board_reelstrips()
            reveal_event(self)
            self.get_clusters_update_wins()
            self.emit_tumble_win_events()
            self.update_grid_mults()
            tumble_count = 0
            while self.win_data["totalWin"] > 0 and not self.wincap_triggered and tumble_count < self.config.maximum_tumbles:
                self.tumble_game_board()
                self.get_clusters_update_wins()
                self.emit_tumble_win_events()
                self.update_grid_mults()
                tumble_count += 1
            self.set_end_tumble_event()
            self.win_manager.update_gametype_wins(self.gametype)

    def evaluate_finalwin(self):
        # Engine math payout multipliers must be in 0.1x increments.
        final = round(min(self.win_manager.running_bet_win, self.config.wincap), 1)
        base = round(min(self.win_manager.basegame_wins, self.config.wincap), 1)
        free = round(min(self.win_manager.freegame_wins, self.config.wincap), 1)
        self.final_win = final
        self.book.payout_multiplier = final
        self.book.basegame_wins = base
        self.book.freegame_wins = free

    def run_spin(self, sim, simulation_seed=None):
        self.reset_seed(sim, simulation_seed)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            self.criteria = "basegame"
            self.betmode = self.betmode if hasattr(self, "betmode") else "base"
            if self.betmode == "base":
                self._spin_tumbles()
                self.win_manager.update_gametype_wins(self.gametype)
                self.evaluate_finalwin()
            else:
                mode = self.betmode
                if mode == "mystery":
                    mode = self._mystery_select()
                self._bonus_start(mode)
                self.reset_fs_spin()
                # Bonus-mode feature multipliers are math-only tuning controls;
                # the frontend receives ordinary multiplier events separately.
                if self.betmode == "mystery":
                    self.global_multiplier = {"basic": 7.0, "super": 4.7, "hidden": 27.5}[mode]
                else:
                    self.global_multiplier = {"basic": 2.55, "super": 3.38, "hidden": 10.2}[mode]
                add_event(self, "multiplier", multiplier=self.global_multiplier)
                self.gametype = self.config.freegame_type
                self.run_freespin()
                self.evaluate_finalwin()
                add_event(self, BONUS_COMPLETE, bonusMode=mode, amount=self.final_win)
            self.repeat = False
        self.imprint_wins()

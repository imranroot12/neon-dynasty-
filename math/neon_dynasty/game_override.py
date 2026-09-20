from game_executables import GameExecutables


class GameStateOverride(GameExecutables):
    def reset_book(self):
        super().reset_book()
        self.tumble_win = 0
        self.reset_grid_mults()
        self.bonus_mode = None
        self.dragon_meter = 0

    def reset_fs_spin(self):
        super().reset_fs_spin()
        self.reset_grid_mults()
        self.dragon_meter = 0

    def assign_special_sym_function(self):
        pass

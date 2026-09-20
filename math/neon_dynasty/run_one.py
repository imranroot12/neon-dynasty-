import sys, shutil, os
from game_config import GameConfig
from gamestate import GameState
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs
mode=sys.argv[1]; num=int(sys.argv[2]) if len(sys.argv)>2 else 10000
config=GameConfig(); gs=GameState(config)
# clean mode temp/final outputs only
create_books(gs, config, {mode:num}, 1000, 2, True, False)
generate_configs(gs)
print('DONE', mode, num)

import sys
from game_config import GameConfig
from gamestate import GameState
from src.state.run_sims import create_books
mode=sys.argv[1]; num=int(sys.argv[2])
config=GameConfig(); gs=GameState(config)
create_books(gs, config, {mode:num}, 5000, 4, True, False)
print('DONE', mode, num)

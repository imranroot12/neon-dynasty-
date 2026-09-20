from game_config import GameConfig
from gamestate import GameState
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs
from utils.rgs_verification import execute_all_tests

if __name__ == '__main__':
    config=GameConfig(); gs=GameState(config)
    num=10000
    create_books(gs, config, {'base':num,'basic':num,'super':num,'mystery':num}, 1000, 2, True, False)
    generate_configs(gs)
    execute_all_tests(config)
    print('BUILD48 SDK SIMULATION COMPLETE')

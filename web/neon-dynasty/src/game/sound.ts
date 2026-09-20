import { createSound } from 'utils-sound';

export type MusicName =
	| 'nd_bgm_main'
	| 'nd_bgm_freespin'
	| 'nd_bgm_winlevel_big'
	| 'nd_bgm_winlevel_epic'
	| 'nd_bgm_winlevel_max'
	| 'nd_bgm_winlevel_mega'
	| 'nd_bgm_winlevel_superwin';

export type SoundEffectName =
	| 'nd_jng_intro_fs'
	| 'nd_sfx_anticipation'
	| 'nd_sfx_anticipation_start'
	| 'nd_sfx_bigwin_coinloop'
	| 'nd_sfx_btn_general'
	| 'nd_sfx_btn_spin'
	| 'nd_sfx_fs_respins'
	| 'nd_sfx_multiplier_combine_a'
	| 'nd_sfx_multiplier_combine_b'
	| 'nd_sfx_multiplier_explosion_a'
	| 'nd_sfx_multiplier_explosion_b'
	| 'nd_sfx_multiplier_explosion_c'
	| 'nd_sfx_multiplier_landing'
	| 'nd_sfx_multiplier_reset'
	| 'nd_sfx_multiplier_up'
	| 'nd_sfx_multiplier_update'
	| 'nd_sfx_multiplier_win'
	| 'nd_sfx_reel_stop_1'
	| 'nd_sfx_reel_stop_2'
	| 'nd_sfx_reel_stop_3'
	| 'nd_sfx_reel_stop_4'
	| 'nd_sfx_reel_stop_5'
	| 'nd_sfx_royals_landing'
	| 'nd_sfx_scatter_reveal'
	| 'nd_sfx_scatter_stop_1'
	| 'nd_sfx_scatter_stop_2'
	| 'nd_sfx_scatter_stop_3'
	| 'nd_sfx_scatter_stop_4'
	| 'nd_sfx_scatter_stop_5'
	| 'nd_sfx_scatter_win'
	| 'nd_sfx_scatter_win_v2'
	| 'nd_sfx_superfreespin'
	| 'nd_sfx_symbols_landing'
	| 'nd_sfx_wild_explode'
	| 'nd_sfx_winlevel_end'
	| 'nd_sfx_winlevel_nice'
	| 'nd_sfx_winlevel_small'
	| 'nd_sfx_winlevel_standard'
	| 'nd_sfx_winlevel_substantial'
	| 'nd_sfx_youwon_panel'
	| 'nd_tumble_win_1'
	| 'nd_tumble_win_2'
	| 'nd_tumble_win_3'
	| 'nd_tumble_win_4';

export type SoundName = MusicName | SoundEffectName;

const sound = createSound<SoundName>();

export { sound };

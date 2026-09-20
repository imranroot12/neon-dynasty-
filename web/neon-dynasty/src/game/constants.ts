import _ from 'lodash';

import type { RawSymbol, SymbolState } from './types';

export const SYMBOL_SIZE = 80;

export const REEL_PADDING = 0.53;

// initial board (padded top and bottom)
export const INITIAL_BOARD: RawSymbol[][] = [
	[
		{ name: 'L1' }, { name: 'L2' }, { name: 'L3' }, { name: 'H1' }, { name: 'H2' }, { name: 'H3' }, { name: 'H4' },
	],
	[
		{ name: 'L2' }, { name: 'L3' }, { name: 'L4' }, { name: 'H2' }, { name: 'H3' }, { name: 'H4' }, { name: 'L1' },
	],
	[
		{ name: 'L3' }, { name: 'L4' }, { name: 'H1' }, { name: 'H2' }, { name: 'H4' }, { name: 'L1' }, { name: 'L2' },
	],
	[
		{ name: 'L4' }, { name: 'H1' }, { name: 'H2' }, { name: 'H3' }, { name: 'L1' }, { name: 'L2' }, { name: 'L3' },
	],
	[
		{ name: 'H1' }, { name: 'H2' }, { name: 'H3' }, { name: 'H4' }, { name: 'L2' }, { name: 'L3' }, { name: 'L4' },
	],
	[
		{ name: 'H2' }, { name: 'H3' }, { name: 'H4' }, { name: 'L1' }, { name: 'L3' }, { name: 'L4' }, { name: 'L2' },
	],
];

export const BOARD_DIMENSIONS = { x: INITIAL_BOARD.length, y: INITIAL_BOARD[0].length - 2 };

export const BOARD_SIZES = {
	width: SYMBOL_SIZE * BOARD_DIMENSIONS.x,
	height: SYMBOL_SIZE * BOARD_DIMENSIONS.y,
};

export const BACKGROUND_RATIO = 2039 / 1000;
export const PORTRAIT_BACKGROUND_RATIO = 1242 / 2208;
const PORTRAIT_RATIO = 800 / 1422;
const LANDSCAPE_RATIO = 1600 / 900;
const DESKTOP_RATIO = 1422 / 800;

const DESKTOP_HEIGHT = 800;
const LANDSCAPE_HEIGHT = 900;
const PORTRAIT_HEIGHT = 1422;
export const DESKTOP_MAIN_SIZES = { width: DESKTOP_HEIGHT * DESKTOP_RATIO, height: DESKTOP_HEIGHT };
export const LANDSCAPE_MAIN_SIZES = {
	width: LANDSCAPE_HEIGHT * LANDSCAPE_RATIO,
	height: LANDSCAPE_HEIGHT,
};
export const PORTRAIT_MAIN_SIZES = {
	width: PORTRAIT_HEIGHT * PORTRAIT_RATIO,
	height: PORTRAIT_HEIGHT,
};

export const HIGH_SYMBOLS = ['H1', 'H2', 'H3', 'H4', 'H5'];

export const INITIAL_SYMBOL_STATE: SymbolState = 'static';

const M_SIZE = 0.3;
const HIGH_SYMBOL_SIZE = 0.9;
const LOW_SYMBOL_SIZE = 0.9;
const SPECIAL_SYMBOL_SIZE = 1;

const SPIN_OPTIONS_SHARED = {
	reelFallInDelay: 80,
	reelPaddingMultiplierNormal: 1.25,
	reelPaddingMultiplierAnticipated: 18,
	reelFallOutDelay: 145,
};

export const SPIN_OPTIONS_DEFAULT = {
	...SPIN_OPTIONS_SHARED,
	symbolFallInSpeed: 3.5,
	symbolFallInInterval: 30,
	symbolFallInBounceSpeed: 0.15,
	symbolFallInBounceSizeMulti: 0.5,
	symbolFallOutSpeed: 3.5,
	symbolFallOutInterval: 20,
};

export const SPIN_OPTIONS_FAST = {
	...SPIN_OPTIONS_SHARED,
	symbolFallInSpeed: 7,
	symbolFallInInterval: 0,
	symbolFallInBounceSpeed: 0.3,
	symbolFallInBounceSizeMulti: 0.25,
	symbolFallOutSpeed: 7,
	symbolFallOutInterval: 0,
};

export const MOTION_BLUR_VELOCITY = 31;

export const zIndexes = {
	background: {
		backdrop: -3,
		normal: -2,
		feature: -1,
	},
};

const spriteInfo = (assetKey: string, scale = 1) => ({ type: 'sprite', assetKey, sizeRatios: { width: scale, height: scale } });
const winInfo = (assetKey: string, scale = 1) => spriteInfo(assetKey, scale);

const symbol = (assetKey: string) => ({
	explosion: spriteInfo('explosion', 1),
	win: winInfo(assetKey, 0.92),
	postWinStatic: spriteInfo(assetKey, 0.92),
	static: spriteInfo(assetKey, 0.92),
	spin: spriteInfo(assetKey, 0.92),
	land: spriteInfo(assetKey, 0.92),
});

export const SYMBOL_INFO_MAP = {
	H1: symbol('H1'),
	H2: symbol('H2'),
	H3: symbol('H3'),
	H4: symbol('H4'),
	H5: symbol('H5'),
	L1: symbol('L1'),
	L2: symbol('L2'),
	L3: symbol('L3'),
	L4: symbol('L4'),
	W: {
		explosion: spriteInfo('explosion'),
		postWinStatic: spriteInfo('W', 1),
		static: spriteInfo('W', 1),
		spin: spriteInfo('W', 1),
		win: spriteInfo('W', 1),
		land: spriteInfo('W', 1),
	},
	S: {
		explosion: spriteInfo('explosion'),
		postWinStatic: spriteInfo('S', 1),
		static: spriteInfo('S', 1),
		spin: spriteInfo('S', 1),
		win: spriteInfo('S', 1),
		land: spriteInfo('S', 1),
	},
} as const;

export const SCATTER_LAND_SOUND_MAP = {
	1: 'nd_sfx_scatter_stop_1',
	2: 'nd_sfx_scatter_stop_2',
	3: 'nd_sfx_scatter_stop_3',
	4: 'nd_sfx_scatter_stop_4',
	5: 'nd_sfx_scatter_stop_5',
} as const;

import type { NeonBookEvent } from './neonDynastyBookEvents';

/**
 * Presentation adapter only. Payouts, outcomes and bonus selection remain
 * authoritative in the RGS book returned by the server.
 */
export function adaptNeonEvent(event: NeonBookEvent): Record<string, unknown> {
	switch (event.type) {
		case 'clusterWin':
			return {
				index: event.index,
				type: 'winInfo',
				totalWin: event.amount * event.multiplier,
				wins: [{
					symbol: event.symbol,
					win: event.amount,
					positions: event.positions,
					meta: { globalMult: event.multiplier, clusterMult: 1, winWithoutMult: event.amount, overlay: event.positions[0] ?? { reel: 0, row: 0 }, },
				}],
			};
		case 'tumble':
			return { index: event.index, type: 'tumbleBoard', explodingSymbols: event.explodingPositions, newSymbols: event.board };
		case 'bonusStart':
			return { index: event.index, type: 'bonusStart', mode: event.mode, totalSpins: event.totalSpins };
		case 'mysteryReveal':
			return { index: event.index, type: 'mysteryReveal', vaults: event.vaults, selected: event.selected };
		case 'dragonMeter':
			return { index: event.index, type: 'dragonMeter', value: event.value };
		case 'dragonEvent':
			return { index: event.index, type: 'dragonEvent', event: event.event };
		case 'bonusComplete':
			return { index: event.index, type: 'bonusComplete', bonusMode: 'hidden', amount: event.amount };
		case 'multiplier':
			return { index: event.index, type: 'updateGlobalMult', globalMult: event.value };
		case 'freeSpinCounter':
			return { index: event.index, type: 'updateFreeSpin', amount: event.current, total: event.total };
		case 'retrigger':
			return { index: event.index, type: 'freeSpinRetrigger', totalFs: event.total, positions: [] };
		default:
			return event;
	}
}

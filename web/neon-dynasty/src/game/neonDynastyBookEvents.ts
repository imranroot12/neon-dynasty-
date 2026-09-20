export type NeonPosition = { reel: number; row: number };
export type NeonBoard = { name: string; multiplier?: number }[][];

export type NeonBookEvent =
  | { index: number; type: "reveal"; board: NeonBoard }
  | { index: number; type: "clusterWin"; symbol: string; positions: NeonPosition[]; amount: number; multiplier: number }
  | { index: number; type: "tumble"; explodingPositions: NeonPosition[]; board: NeonBoard }
  | { index: number; type: "mysteryReveal"; vaults: ("basic" | "super" | "hidden")[]; selected: "basic" | "super" | "hidden" }
  | { index: number; type: "multiplier"; value: number }
  | { index: number; type: "dragonMeter"; value: number }
  | { index: number; type: "dragonEvent"; event: "wildStorm" | "mysteryStorm" | "multiplierDrop" | "reelExpansion" | "symbolUpgrade" }
  | { index: number; type: "bonusStart"; mode: "basic" | "super" | "hidden"; totalSpins: number }
  | { index: number; type: "freeSpinCounter"; current: number; total: number }
  | { index: number; type: "retrigger"; addedSpins: number; total: number }
  | { index: number; type: "bonusComplete"; amount: number }
  | { index: number; type: "setTotalWin"; amount: number }
  | { index: number; type: "finalWin"; amount: number };

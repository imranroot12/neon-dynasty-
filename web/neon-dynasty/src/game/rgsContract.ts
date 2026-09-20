/** RGS-facing contracts for Neon Dynasty.
 * No client-side RNG or payout calculation belongs here.
 */
export type RgsBetLevel = { amount: number; currency?: string };
export type RgsBetConfig = {
  min: number;
  max: number;
  step: number;
  levels?: RgsBetLevel[];
};

export type NeonRgsConfig = RgsBetConfig & {
  rgsUrl: string;
  game: string;
  version?: string;
};

export type ReplayConfig = {
  replay: boolean;
  game?: string;
  version?: string;
  mode?: string;
  event?: string;
  rgsUrl?: string;
  currency?: string;
  amount?: number;
  lang?: string;
  device?: string;
  social?: boolean;
};

export function readQuery(search = typeof window === 'undefined' ? '' : window.location.search): ReplayConfig {
  const q = new URLSearchParams(search);
  const bool = (v: string | null) => v === 'true' || v === '1';
  const amount = q.get('amount');
  return {
    replay: bool(q.get('replay')),
    game: q.get('game') ?? undefined,
    version: q.get('version') ?? undefined,
    mode: q.get('mode') ?? undefined,
    event: q.get('event') ?? undefined,
    rgsUrl: q.get('rgs_url') ?? undefined,
    currency: q.get('currency') ?? undefined,
    amount: amount == null ? undefined : Number(amount),
    lang: q.get('lang') ?? undefined,
    device: q.get('device') ?? undefined,
    social: q.get('social') == null ? undefined : bool(q.get('social')),
  };
}

export function clampToRgsBet(amount: number, config: RgsBetConfig): number {
  const step = config.step > 0 ? config.step : 1;
  const clamped = Math.min(config.max, Math.max(config.min, amount));
  const stepped = config.min + Math.round((clamped - config.min) / step) * step;
  return Number(Math.min(config.max, Math.max(config.min, stepped)).toFixed(8));
}

export function isRgsBetAllowed(amount: number, config: RgsBetConfig): boolean {
  if (!Number.isFinite(amount) || amount < config.min || amount > config.max) return false;
  const step = config.step > 0 ? config.step : 1;
  const n = (amount - config.min) / step;
  return Math.abs(n - Math.round(n)) < 1e-8;
}

export function getReplayEndpoint(config: ReplayConfig): string | null {
  if (!config.replay || !config.rgsUrl || !config.game || !config.version || !config.mode || !config.event) return null;
  const base = config.rgsUrl.replace(/\/$/, '');
  return `${base}/bet/replay/${encodeURIComponent(config.game)}/${encodeURIComponent(config.version)}/${encodeURIComponent(config.mode)}/${encodeURIComponent(config.event)}`;
}

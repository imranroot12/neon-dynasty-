<script lang="ts">
  import { onMount } from 'svelte';
  import { clampToRgsBet, isRgsBetAllowed, type RgsBetConfig } from '../game/rgsContract';

  export let config: RgsBetConfig = { min: 0.1, max: 100, step: 0.1 };
  export let value = 1;
  export let disabled = false;
  export let onSpin: (() => void) | undefined;

  let levels: number[] = [];
  $: current = clampToRgsBet(value, config);
  $: canSpin = !disabled && isRgsBetAllowed(current, config);

  onMount(() => {
    levels = config.levels?.map((x) => x.amount).filter(Number.isFinite) ?? [];
  });

  function change(delta: number) {
    const ordered = levels.length ? levels : undefined;
    if (ordered) {
      const i = ordered.reduce((best, x, idx) => Math.abs(x - current) < Math.abs(ordered[best] - current) ? idx : best, 0);
      value = ordered[Math.max(0, Math.min(ordered.length - 1, i + delta))];
      return;
    }
    value = clampToRgsBet(current + delta * config.step, config);
  }
</script>

<div class="bet-controls" aria-label="Bet controls">
  <button aria-label="Decrease bet" disabled={disabled} onclick={() => change(-1)}>−</button>
  <span aria-live="polite">{current.toFixed(2)}×</span>
  <button aria-label="Increase bet" disabled={disabled} onclick={() => change(1)}>+</button>
  <button class="spin" disabled={!canSpin} onclick={() => onSpin?.()}>SPIN</button>
</div>

<style>
.bet-controls{display:flex;align-items:center;gap:8px;font-family:sans-serif;color:#fff}.bet-controls button{min-width:42px;height:42px;border:1px solid rgba(255,255,255,.18);border-radius:10px;background:rgba(7,10,27,.94);color:#fff;font-size:20px;font-weight:800}.bet-controls span{min-width:72px;text-align:center;font-weight:800}.bet-controls .spin{min-width:86px;border-color:rgba(39,231,255,.55);font-size:14px}.bet-controls button:disabled{opacity:.4}
</style>

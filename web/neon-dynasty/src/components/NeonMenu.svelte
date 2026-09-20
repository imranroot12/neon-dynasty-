<script lang="ts">
	import { stateBet } from 'state-shared';
	import { getContext } from '../game/context';

	const context = getContext();
	let open = false;
	let music = true;
	let sound = true;
	let turbo = false;
	const paytable = [
		['H1', [6.45,12.9,22.575,32.25,51.6,77.4,116.1,154.8,206.4,283.8,387,516,709.5,967.5,1290,1806,2322,2838,3870,5160,6450,8385,10320,12900,16125,19350]],
		['H2', [5.16,10.32,18.06,25.8,41.28,61.92,92.88,123.84,165.12,227.04,309.6,412.8,567.6,774,1032,1444.8,1857.6,2270.4,3096,4128,5160,6708,8256,10320,12900,15480]],
		['H3', [3.87,7.74,13.545,19.35,30.96,46.44,69.66,92.88,123.84,170.28,232.2,309.6,425.7,580.5,774,1083.6,1393.2,1702.8,2322,3096,3870,5031,6192,7740,9675,11610]],
		['H4', [3.225,6.45,11.61,16.125,25.8,38.7,58.05,77.4,103.2,141.9,193.5,258,354.75,483.75,645,903,1161,1419,1935,2580,3225,4192.5,5160,6450,8062.5,9675]],
		['L1', [1.935,3.87,6.45,9.675,15.48,23.22,34.83,46.44,61.92,85.14,116.1,154.8,212.85,290.25,387,541.8,696.6,851.4,1161,1548,1935,2515.5,3096,3870,4837.5,5805]],
		['L2', [1.548,3.096,5.16,7.74,12.384,18.576,27.864,37.152,49.536,68.112,92.88,123.84,170.28,232.2,309.6,433.44,557.28,681.12,928.8,1238.4,1548,2012.4,2476.8,3096,3870,4644]],
		['L3', [1.29,2.58,4.386,6.45,10.32,15.48,23.22,30.96,41.28,56.76,77.4,103.2,141.9,193.5,258,361.2,464.4,567.6,774,1032,1290,1677,2064,2580,3225,3870]],
		['L4', [1.032,2.064,3.612,5.16,8.256,12.384,18.576,24.768,33.024,45.408,61.92,82.56,113.52,154.8,206.4,288.96,371.52,454.08,619.2,825.6,1032,1341.6,1651.2,2064,2580,3096]],
	] as const;
</script>

<div class="menu-root">
	<button class="menu-button" aria-label="Open Neon Dynasty menu" onclick={() => (open = !open)}>☰</button>
	{#if open}
		<div class="panel" role="dialog" aria-label="Neon Dynasty menu">
			<div class="title">NEON DYNASTY</div>
			<button onclick={() => { music = !music; context.eventEmitter.broadcast({ type: 'musicMute', muted: !music }); }}>Music: {music ? 'ON' : 'OFF'}</button>
			<button onclick={() => { sound = !sound; context.eventEmitter.broadcast({ type: 'soundMute', muted: !sound }); }}>Sound Effects: {sound ? 'ON' : 'OFF'}</button>
			<button onclick={() => { turbo = !turbo; stateBet.isTurbo = turbo; }}>Turbo Spins: {turbo ? 'ON' : 'OFF'}</button>
			<div class="info">
				<strong>Rules & Features</strong>
				<span>6×5 cluster wins · 5+ connected symbols</span>
				<span>Target RTP: 96.0% · Max win: 20,000×</span>
				<span>Basic: 8 FS · 100× buy</span>
				<span>Super: 10 FS · 200× buy</span>
				<span>Hidden: 15 FS · Mystery Buy only</span>
				<span>ANTE: 3× bet · 5× trigger setting</span>
			</div>
			<details><summary>Rules & Paytable</summary>
				<div class="paytable"><div class="pay-head">Cluster size 5 → 30 · payout × bet</div>
					{#each paytable as row}<div class="pay-row"><b>{row[0]}</b><span>{row[1].map((v, i) => `${i + 5}: ${v}×`).join(' · ')}</span></div>{/each}
				</div>
			</details>
			<div class="about">WILD substitutes for regular symbols. Multipliers: 2×, 3×, 5×, 10×, 25×, 50×. Mystery can reveal feature outcomes, high-value symbols, multipliers or Dragon Events. Dragon Meter triggers one of five Dragon Events at 100%.</div>
			<div class="about">Voltix Games · Neon Dynasty</div>
		</div>
	{/if}
</div>

<style>
	.menu-root { position: fixed; top: 1rem; right: 1rem; z-index: 1000; font-family: sans-serif; }
	.menu-button { width: 42px; height: 42px; border: 1px solid rgba(255,255,255,.35); border-radius: 10px; background: rgba(10,10,25,.88); color: white; font-size: 22px; cursor: pointer; }
	.panel { margin-top: .5rem; width: min(310px, calc(100vw - 2rem)); padding: 14px; display: grid; gap: 8px; border: 1px solid rgba(255,255,255,.22); border-radius: 14px; background: rgba(7,8,20,.96); color: white; box-shadow: 0 12px 36px rgba(0,0,0,.45); }
	.panel button { padding: 9px 10px; border: 0; border-radius: 8px; background: rgba(255,255,255,.08); color: white; text-align: left; cursor: pointer; }
	.title { font-weight: 800; letter-spacing: .08em; }
	.info { display: grid; gap: 4px; padding: 8px 0; font-size: 12px; line-height: 1.35; }
	.about { opacity: .65; font-size: 11px; padding-top: 4px; }
	details { border-top: 1px solid rgba(255,255,255,.12); padding-top: 8px; }
	summary { cursor: pointer; font-weight: 700; font-size: 12px; }
	.paytable { margin-top: 8px; max-height: 260px; overflow: auto; font-size: 9px; }
	.pay-head { opacity: .65; margin-bottom: 6px; }
	.pay-row { display: grid; grid-template-columns: 28px 1fr; gap: 5px; padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,.06); }
	.pay-row span { opacity: .82; line-height: 1.35; }
	@media (max-width: 600px) { .menu-root { top: .5rem; right: .5rem; } }
</style>

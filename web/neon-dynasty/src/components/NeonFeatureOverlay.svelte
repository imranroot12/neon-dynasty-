<script lang="ts">
	import { getContext } from '../game/context';
	const context = getContext();
	let meter = $state(0);
	let bonus = $state('');
	let spins = $state<number | null>(null);
	let vaults = $state<string[]>([]);
	let selected = $state('');
	let dragonEvent = $state('');
	context.eventEmitter.subscribeOnMount({
		neonDragonMeter: ({ value }) => (meter = value),
		neonBonusStart: ({ mode, totalSpins }) => { bonus = mode.toUpperCase(); spins = totalSpins; },
		neonMysteryReveal: ({ vaults: v, selected: s }) => { vaults = v; selected = s; },
		neonDragonEvent: ({ event }) => (dragonEvent = event),
		neonBonusComplete: () => { spins = null; setTimeout(() => { bonus = ''; vaults = []; selected = ''; dragonEvent = ''; }, 900); },
	});
</script>

<div class="feature-layer" aria-live="polite">
	<div class="dragon">
		<div class="dragon-title">DRAGON METER</div>
		<div class="track"><div class="fill" style={`width:${meter}%`}></div></div>
		<div class="meter-value">{meter}%</div>
	</div>
	{#if bonus}
		<div class="bonus">{bonus} BONUS · {spins} FREE SPINS</div>
	{/if}
	{#if vaults.length}
		<div class="vaults"><div>MYSTERY VAULTS</div><div class="vault-row">{#each vaults as v, i}<span class:selected={v === selected}>{i + 1} · {v.toUpperCase()}</span>{/each}</div></div>
	{/if}
	{#if dragonEvent}<div class="dragon-event">DRAGON EVENT · {dragonEvent}</div>{/if}
</div>

<style>
.feature-layer{position:fixed;left:50%;top:3.5rem;transform:translateX(-50%);z-index:900;display:grid;gap:6px;text-align:center;color:#fff;font:600 11px/1.2 sans-serif;pointer-events:none;text-shadow:0 1px 4px #000}.dragon{min-width:190px;padding:7px 10px;border:1px solid rgba(0,230,255,.45);border-radius:10px;background:rgba(4,10,26,.82)}.dragon-title{letter-spacing:.12em;font-size:9px}.track{height:6px;margin-top:5px;border-radius:9px;background:rgba(255,255,255,.12);overflow:hidden}.fill{height:100%;background:linear-gradient(90deg,#00d9ff,#ff32c8);transition:width .25s}.meter-value{font-size:9px;margin-top:3px;opacity:.8}.bonus,.dragon-event{padding:7px 10px;border-radius:9px;background:rgba(7,8,20,.9);border:1px solid rgba(255,255,255,.18);letter-spacing:.06em}.vaults{padding:7px 9px;border-radius:9px;background:rgba(7,8,20,.94);border:1px solid rgba(255,255,255,.18)}.vault-row{display:flex;gap:5px;justify-content:center;margin-top:5px}.vault-row span{padding:4px 5px;border-radius:5px;background:rgba(255,255,255,.07);font-size:8px}.vault-row span.selected{background:rgba(255,50,200,.35);border:1px solid rgba(255,50,200,.65)}
@media(max-width:600px){.feature-layer{top:3rem;transform:translateX(-50%) scale(.88);transform-origin:top center}}
</style>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Text, REM } from 'pixi-svelte';
	import type { SymbolState, RawSymbol } from '../game/types';
	import { SYMBOL_SIZE } from '../game/constants';

	type Props = { x?: number; y?: number; state: SymbolState; rawSymbol: RawSymbol; oncomplete?: () => void; loop?: boolean };
	const props: Props = $props();
	const labels: Record<string, string> = { H1: 'EM', H2: 'DR', H3: 'TF', H4: 'BF', L1: 'FOX', L2: 'TIGER', L3: 'BUTTERFLY', L4: 'LOTUS', W: 'WILD' };
	const glyph = $derived(labels[props.rawSymbol.name] ?? props.rawSymbol.name);
	const size = $derived(Math.max(12, SYMBOL_SIZE * 0.18));
	onMount(() => props.oncomplete?.());
</script>

<Container x={props.x} y={props.y}>
	<Text
		text={glyph}
		anchor={0.5}
		style={{ fontFamily: 'proxima-nova', fontSize: size, fontWeight: '800', fill: props.rawSymbol.name === 'W' ? 0xff3bdc : 0x8eeeff, stroke: 0x061225, strokeThickness: 4, letterSpacing: 1 }}
	/>
	<Text
		text={props.rawSymbol.name === 'W' ? 'DRAGON WILD' : 'NEON DYNASTY'}
		anchor={{ x: 0.5, y: 0 }}
		y={size * 0.62}
		style={{ fontFamily: 'proxima-nova', fontSize: REM * 0.38, fontWeight: '600', fill: 0xffffff, alpha: 0.58 }}
	/>
</Container>


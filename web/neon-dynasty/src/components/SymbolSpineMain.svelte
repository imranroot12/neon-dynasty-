<script lang="ts">
	import { Sprite } from 'pixi-svelte';
	import { onMount } from 'svelte';
	import { getSymbolInfo } from '../game/utils';
	import { SYMBOL_SIZE } from '../game/constants';

	type Props = {
		symbolInfo: ReturnType<typeof getSymbolInfo>;
		x?: number;
		y?: number;
		listener?: unknown;
		loop?: boolean;
	};
	const props: Props = $props();
	onMount(() => {
		const listener = props.listener as { complete?: () => void } | undefined;
		listener?.complete?.();
	});
</script>

<Sprite
	x={props.x}
	y={props.y}
	anchor={0.5}
	key={props.symbolInfo.assetKey}
	width={SYMBOL_SIZE * props.symbolInfo.sizeRatios.width}
	height={SYMBOL_SIZE * props.symbolInfo.sizeRatios.height}
/>

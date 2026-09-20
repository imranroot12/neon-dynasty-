<script lang="ts">
 import {Sprite} from 'pixi-svelte'; import {getContext} from '../game/context'; import type {Reel} from '../game/stateGame.svelte'; import {REEL_PADDING,SYMBOL_SIZE} from '../game/constants'; type Props={reel:Reel;oncomplete:()=>void}; const props:Props=$props(); const context=getContext(); $effect(()=>{if(props.reel.reelState.motion==='stopped') props.oncomplete();});
 const x=$derived(context.stateGameDerived.boardLayout().x-context.stateGameDerived.boardLayout().width*.5+(props.reel.reelIndex+REEL_PADDING)*SYMBOL_SIZE); const y=$derived(context.stateGameDerived.boardLayout().y-SYMBOL_SIZE*.06);
</script>
<Sprite key="anticipation" x={x} y={y} width={SYMBOL_SIZE*.56} height={SYMBOL_SIZE*3.7} alpha={.85}/>

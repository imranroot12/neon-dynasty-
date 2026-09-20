<script lang="ts" module>
export type EmitterEventMultiplierGrid={type:'multiplierGridShow'}|{type:'multiplierGridHide'}|{type:'multiplierGridUpdate';grid:number[][]}|{type:'multiplierGridClear'};
</script>
<script lang="ts">
 import { BitmapText, Container, Sprite } from 'pixi-svelte'; import BoardContainer from './BoardContainer.svelte'; import {getContext} from '../game/context'; import {SYMBOL_SIZE} from '../game/constants';
 const context=getContext(); const DEFAULT_GRID=Array.from({length:6},()=>Array(5).fill(0)); let show=$state(false); let grid=$state(DEFAULT_GRID);
 context.eventEmitter.subscribeOnMount({multiplierGridShow:()=>show=true,multiplierGridHide:()=>show=false,multiplierGridUpdate:e=>grid=e.grid,multiplierGridClear:()=>grid=DEFAULT_GRID});
</script>
<BoardContainer>{#if show}{#each grid as reel,reelIndex}{#each reel as multiplier,rowIndex}{#if multiplier>0}<Container x={(reelIndex+.5)*SYMBOL_SIZE} y={(rowIndex+.5)*SYMBOL_SIZE}><Sprite key="payFrame" width={SYMBOL_SIZE*.95} height={SYMBOL_SIZE*.95} alpha={.8}/><BitmapText x={0} y={0} anchor={.5} text={`${multiplier}×`} style={{fontSize:SYMBOL_SIZE*.32,fill:0xffffff,fontWeight:'700'}}/></Container>{/if}{/each}{/each}{/if}</BoardContainer>

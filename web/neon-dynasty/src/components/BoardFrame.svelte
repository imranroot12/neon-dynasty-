<script lang="ts" module>
export type EmitterEventBoardFrame = { type: 'boardFrameGlowShow' } | { type: 'boardFrameGlowHide' };
</script>
<script lang="ts">
 import { Sprite } from 'pixi-svelte';
 import { getContext } from '../game/context';
 const context=getContext();
 let glow=$state(false);
 context.eventEmitter.subscribeOnMount({boardFrameGlowShow:()=>glow=true,boardFrameGlowHide:()=>glow=false});
</script>
<Sprite key="reelsFrame" anchor={0.5} x={context.stateGameDerived.boardLayout().x} y={context.stateGameDerived.boardLayout().y} width={context.stateGameDerived.boardLayout().width*1.12} height={context.stateGameDerived.boardLayout().height*1.12} alpha={glow?1:0.92}/>

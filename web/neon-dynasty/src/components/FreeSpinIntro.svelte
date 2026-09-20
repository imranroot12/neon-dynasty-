<script lang="ts" module>
export type EmitterEventFreeSpinIntro={type:'freeSpinIntroShow'}|{type:'freeSpinIntroHide'}|{type:'freeSpinIntroUpdate';totalFreeSpins:number};
</script>
<script lang="ts">
 import {CanvasSizeRectangle} from 'components-layout'; import {FadeContainer} from 'components-pixi'; import {waitForResolve} from 'utils-shared/wait'; import {Text,Sprite} from 'pixi-svelte'; import {getContext} from '../game/context'; import PressToContinue from './PressToContinue.svelte'; import FreeSpinAnimation from './FreeSpinAnimation.svelte';
 const context=getContext(); let show=$state(false); let freeSpinsFromEvent=$state(0); let oncomplete=$state(()=>{});
 context.eventEmitter.subscribeOnMount({freeSpinIntroShow:()=>show=true,freeSpinIntroHide:()=>show=false,freeSpinIntroUpdate:async e=>{freeSpinsFromEvent=e.totalFreeSpins; await waitForResolve(r=>oncomplete=r);}});
</script>
<FadeContainer {show}><CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={.55}/><FreeSpinAnimation>{#snippet children({sizes})}<Sprite key="fsIntro" anchor={.5} width={sizes.width*.8} height={sizes.height*.55}/><Text anchor={.5} y={-20} text={`FREE SPINS  ${freeSpinsFromEvent}`} style={{fontFamily:'Arial',fontSize:42,fill:0xffffff,fontWeight:'800'}}/>{/snippet}</FreeSpinAnimation><PressToContinue onpress={()=>oncomplete()}/></FadeContainer>

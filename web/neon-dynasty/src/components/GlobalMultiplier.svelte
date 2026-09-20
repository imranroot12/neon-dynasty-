<script lang="ts" module>
export type EmitterEventGlobalMultiplier={type:'globalMultiplierShow'}|{type:'globalMultiplierHide'}|{type:'globalMultiplierUpdate';multiplier:number};
</script>
<script lang="ts">
 import {BitmapText,Container,Sprite} from 'pixi-svelte'; import {FadeContainer} from 'components-pixi'; import BoardContainer from './BoardContainer.svelte'; import {getContext} from '../game/context'; import {SYMBOL_SIZE} from '../game/constants';
 const context=getContext(); const PANEL_WIDTH=SYMBOL_SIZE*.9; let show=$state(false); let multiplier=$state(1);
 context.eventEmitter.subscribeOnMount({globalMultiplierShow:()=>show=true,globalMultiplierHide:()=>show=false,globalMultiplierUpdate:e=>multiplier=e.multiplier});
 const position=$derived({x:context.stateGameDerived.boardLayout().width-PANEL_WIDTH*1.3,y:-SYMBOL_SIZE*.47});
</script>
<FadeContainer {show}><BoardContainer><Container {...position}><Sprite key="globalMultiplier" width={PANEL_WIDTH*2.2} height={PANEL_WIDTH*1.5}/><BitmapText anchor={.5} text={`${multiplier}×`} style={{fontSize:SYMBOL_SIZE*.55,fill:0xffffff,fontWeight:'700'}}/></Container></BoardContainer></FadeContainer>

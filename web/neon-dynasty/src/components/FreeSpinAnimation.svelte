<script lang="ts">
 import type {Snippet} from 'svelte'; import {Container,Sprite,type Sizes} from 'pixi-svelte'; import {MainContainer} from 'components-layout'; import {getContext} from '../game/context'; import {SYMBOL_SIZE,BOARD_DIMENSIONS} from '../game/constants'; type Props={children:Snippet<[{sizes:Sizes}]>}; const props:Props=$props(); const context=getContext(); const BACKGROUND_SIZES={width:SYMBOL_SIZE*BOARD_DIMENSIONS.y,height:SYMBOL_SIZE*BOARD_DIMENSIONS.y};
</script>
<MainContainer><Container x={context.stateGameDerived.boardLayout().x} y={context.stateGameDerived.boardLayout().y}><Sprite key="fsIntro" width={BACKGROUND_SIZES.width} height={BACKGROUND_SIZES.height}/>{@render props.children({sizes:BACKGROUND_SIZES})}</Container></MainContainer>

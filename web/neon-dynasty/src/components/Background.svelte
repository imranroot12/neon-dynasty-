<script lang="ts">
 import { Rectangle, Sprite } from 'pixi-svelte';
 import { FadeContainer } from 'components-pixi';
 import { SECOND } from 'constants-shared/time';
 import { getContext } from '../game/context';
 const context=getContext();
 const backgroundProps=$derived(context.stateLayoutDerived.normalBackgroundLayout({scale:0.5}));
 const showBaseBackground=$derived(context.stateGame.gameType==='basegame');
 const showFeatureBackground=$derived(context.stateGame.gameType==='freegame');
</script>
<Rectangle {...context.stateLayoutDerived.canvasSizes()} backgroundColor={0x050816} zIndex={-3}/>
<FadeContainer show={showBaseBackground} duration={SECOND} zIndex={-2}><Sprite key="foregroundAnimation" {...backgroundProps}/></FadeContainer>
<FadeContainer show={showFeatureBackground} duration={SECOND} zIndex={-1}><Sprite key="foregroundFeatureAnimation" {...backgroundProps}/></FadeContainer>

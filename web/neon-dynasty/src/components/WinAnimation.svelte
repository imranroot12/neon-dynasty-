<script lang="ts">
 import type {Snippet} from 'svelte'; import {Sprite,Text} from 'pixi-svelte'; import {getContext} from '../game/context'; import {onMount} from 'svelte';
 type Props={animationMap:{intro:string;idle:string;outro:string};children:Snippet}; const props:Props=$props(); const context=getContext(); let oncomplete=$state(()=>{}); let state=$state<'intro'|'idle'|'outro'>('intro'); onMount(()=>{const t=setTimeout(()=>state='idle',450); return()=>clearTimeout(t);});
</script>
<Sprite key="bigwin" width={context.stateGameDerived.boardLayout().width} height={220} alpha={.92}/><Text anchor={.5} y={-30} text={state==='idle'?'BIG WIN':'WIN'} style={{fontFamily:'Arial',fontSize:42,fill:0xffffff,fontWeight:'800'}}/>{@render props.children()}

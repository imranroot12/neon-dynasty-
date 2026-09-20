<script lang="ts">
 import { Sprite } from 'pixi-svelte';
 import { getContext } from '../game/context';
 import { onMount } from 'svelte';
 type Props={oncomplete:()=>void}; const props:Props=$props(); const context=getContext();
 onMount(()=>{const t=setTimeout(props.oncomplete,350); return()=>clearTimeout(t);});
</script>
<Sprite key="transition" x={context.stateLayoutDerived.canvasSizes().width*0.5} y={context.stateLayoutDerived.canvasSizes().height*0.5} width={context.stateLayoutDerived.canvasSizes().width} height={context.stateLayoutDerived.canvasSizes().height*0.9} alpha={0.8}/>

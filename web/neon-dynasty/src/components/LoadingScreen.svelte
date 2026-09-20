<script lang="ts">
 import { Sprite, Container, Text } from 'pixi-svelte';
 import { FadeContainer, LoadingProgress } from 'components-pixi';
 import { MainContainer } from 'components-layout';
 import { getContext } from '../game/context';
 import TransitionAnimation from './TransitionAnimation.svelte';
 import PressToContinue from './PressToContinue.svelte';
 type Props={onloaded:()=>void}; const props:Props=$props(); const context=getContext(); let loadingType=$state<'start'|'transition'>('start');
</script>
<FadeContainer show={loadingType==='start'}><MainContainer><Container x={context.stateLayoutDerived.mainLayout().width*0.5} y={context.stateLayoutDerived.mainLayout().height*0.42}><Sprite key="loader" width={420} height={260}/><Text y={170} anchor={0.5} text="VOLTIX GAMES" style={{fontFamily:'Arial',fontSize:30,fill:0x22d3ee,fontWeight:'700'}}/>
{#if !context.stateApp.loaded}<LoadingProgress y={250} width={320} height={54}>{#snippet background(sizes)}<Sprite key="progressBarBackground" {...sizes}/>{/snippet}{#snippet progress(sizes)}<Sprite key="progressBar" {...sizes}/>{/snippet}{#snippet frame(sizes)}<Sprite key="progressBarFrame" {...sizes}/>{/snippet}</LoadingProgress>{/if}</Container></MainContainer></FadeContainer>
<FadeContainer show={loadingType==='start' && context.stateApp.loaded}><PressToContinue onpress={()=>loadingType='transition'}/></FadeContainer>
<FadeContainer show={loadingType==='transition'}><TransitionAnimation oncomplete={props.onloaded}/></FadeContainer>

<script lang="ts">
 import {Tween} from 'svelte/motion'; import {Sprite,Text} from 'pixi-svelte'; import {bookEventAmountToCurrencyString} from 'utils-shared/amount'; import {SYMBOL_SIZE} from '../game/constants';
 type Props={width:number;amount:number;animate:boolean;oncomplete:()=>void}; const props:Props=$props(); const amount=new Tween(0);
 $effect(()=>{amount.set(props.amount); props.oncomplete();});
</script>
<Sprite key="tumble_win" width={props.width} height={props.width*.55}/><Text anchor={.5} text={bookEventAmountToCurrencyString(amount.current)} style={{fontFamily:'Arial',fontSize:.65*SYMBOL_SIZE,fill:0xffffff,fontWeight:'700'}}/>

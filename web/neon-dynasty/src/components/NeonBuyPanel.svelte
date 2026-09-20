<script lang="ts">
 import { stateBet, stateBetDerived, stateUrlDerived } from 'state-shared';
 import { requestBet } from 'rgs-requests';
 import { getContext } from '../game/context';

 let open = $state(false);
 let ante = $state(false);
 let busy = $state<string | null>(null);
 let error = $state('');
 const context = getContext();

 const modes = [
  { id: 'basic', name: 'BASIC BONUS', spins: 8, cost: 100, note: '' },
  { id: 'super', name: 'SUPER BONUS', spins: 10, cost: 200, note: '' },
  { id: 'mystery', name: 'MYSTERY BUY', spins: 15, cost: 500, note: 'Vault decides mode' },
 ] as const;

 const buy = async (mode: typeof modes[number]) => {
  if (busy) return;
  error = '';
  const baseBet = stateBet.betAmount;
  const totalCost = baseBet * mode.cost * (ante ? 3 : 1);
  if (!Number.isFinite(baseBet) || baseBet <= 0 || totalCost > stateBet.balanceAmount) {
   error = 'Insufficient balance for this purchase.';
   return;
  }

  // The deployed RGS is authoritative for mode pricing and outcome selection.
  // ANTE is intentionally not sent as an invented request field; it will only
  // be enabled when the deployed RGS exposes the corresponding parameter.
  if (ante) {
   error = 'ANTE is displayed but requires the deployed RGS ANTE parameter before it can be charged.';
   return;
  }

  busy = mode.id;
  try {
   const result = await requestBet({
    rgsUrl: stateUrlDerived.rgsUrl(),
    sessionID: stateUrlDerived.sessionID(),
    currency: stateBet.currency,
    amount: baseBet,
    mode: mode.id,
   });
   if (result?.error) throw result;
   if (result?.round) {
    // Resume through the same book-event pipeline used by normal RGS rounds.
    stateBet.activeBetModeKey = mode.id;
    // @ts-ignore RGS round shape is extended by the game book event type.
    stateBet.betToResume = { ...result.round, active: true };
    open = false;
    context.eventEmitter.broadcast({ type: 'resumeBet' });
   }
  } catch (e) {
   console.error(e);
   error = 'The RGS rejected or could not complete the purchase.';
  } finally {
   busy = null;
  }
 };
</script>
<div class="buy-root">
 <button class="buy-button" onclick={() => (open = !open)}>BONUS BUY</button>
 {#if open}
 <section class="panel" aria-label="Bonus Buy">
  <header><strong>BONUS BUY</strong><button class="close" onclick={() => (open = false)}>×</button></header>
  <div class="ante-row"><span>ANTE</span><button class:active={ante} onclick={() => (ante = !ante)}>{ante ? 'ON · 3× BET' : 'OFF · 1× BET'}</button></div>
  {#each modes as mode}
   <button class="mode" disabled={busy !== null || !stateBetDerived.isBetCostAvailable()} onclick={() => buy(mode)}>
    <span><b>{mode.name}</b><small>{mode.spins} starting free spins{mode.note ? ` · ${mode.note}` : ''}</small></span>
    <strong>{busy === mode.id ? '...' : `${mode.cost}×`}</strong>
   </button>
  {/each}
  {#if error}<small class="error">{error}</small>{/if}
  <small class="note">The RGS decides the purchased mode outcome and supplies the book used for playback.</small>
 </section>
 {/if}
</div>
<style>
.buy-root{position:fixed;right:1rem;bottom:5.2rem;z-index:950;font-family:sans-serif;color:#fff}.buy-button{border:1px solid rgba(39,231,255,.5);border-radius:10px;background:rgba(7,10,27,.92);color:#fff;padding:10px 13px;font-weight:800;letter-spacing:.05em}.panel{width:min(340px,calc(100vw - 2rem));margin-bottom:7px;padding:12px;border:1px solid rgba(255,255,255,.2);border-radius:14px;background:rgba(6,8,22,.97);box-shadow:0 14px 45px rgba(0,0,0,.5)}header{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}.close{background:none;border:0;color:#fff;font-size:22px}.ante-row{display:flex;justify-content:space-between;align-items:center;padding:8px;border-radius:9px;background:rgba(255,255,255,.06);margin-bottom:8px}.ante-row button{border:1px solid rgba(255,255,255,.15);border-radius:7px;padding:7px 9px;background:rgba(255,255,255,.08);color:#fff}.ante-row button.active{border-color:#ff3dcc;background:rgba(255,60,204,.15)}.mode{width:100%;display:flex;justify-content:space-between;align-items:center;text-align:left;margin:5px 0;padding:10px;border:1px solid rgba(255,255,255,.12);border-radius:9px;background:rgba(255,255,255,.05);color:#fff}.mode:disabled{opacity:.55}.mode span{display:grid;gap:3px}.mode small,.note,.error{opacity:.72;font-size:10px}.note,.error{display:block;line-height:1.35;margin-top:9px}.error{color:#ff9cba}@media(max-width:600px){.buy-root{right:.5rem;bottom:4.5rem}.panel{width:min(320px,calc(100vw - 1rem))}}
</style>

# Neon Dynasty — RGS / Replay contract

The browser never determines outcomes, payout, RTP, or bonus selection. Those values must come from the RGS book.

## Bet controls

`NeonBetControls.svelte` accepts the authoritative RGS `{min,max,step,levels}` configuration and clamps/validates UI values against it. Production wiring should pass the values returned by the SDK's RGS/auth layer rather than the development defaults.

## Replay

`rgsContract.ts` reads the documented replay query parameters and constructs:

`GET {rgs_url}/bet/replay/{game}/{version}/{mode}/{event}`

Replay mode must disable normal betting/session calls and play the returned book from start to finish. The replay response is authoritative.

## Buy / ANTE

Bonus-buy requests must be sent to the RGS using the exact action supported by the deployed RGS integration. The frontend must not synthesize a purchase or resolve Mystery Vault odds. ANTE is a request parameter/modifier, not client-side RNG.

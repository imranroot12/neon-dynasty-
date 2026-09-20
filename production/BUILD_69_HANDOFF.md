# Build 69 — official execution handoff

Build 69 is the next execution candidate after Build 68.

## Corrected path
The Web SDK application is explicitly copied to:
`<official-web-sdk>/apps/neon-dynasty/`

Then the official documented workspace build is run with:
`pnpm run build --filter=neon-dynasty`

The Math SDK game is copied to:
`<official-math-sdk>/games/neon_dynasty/`

and executed using its real `run.py`.

## Gates
The finalizer requires publication artifacts, all four required modes, 100k+
rows for readable book files, a production Web SDK output, and SDK commit
provenance. It deliberately does not certify Stake Engine deployment.

## Staging
After CI succeeds, perform a real Stake Engine staging session and preserve the
session/build identifier and logs. Verify authentication, balance, normal spin,
cluster/tumble events, Mystery Buy, all bonus modes, free-spin retriggers,
Wild/multiplier events, replay and end-round behavior.

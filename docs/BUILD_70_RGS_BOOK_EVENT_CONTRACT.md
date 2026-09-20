# Neon Dynasty — Build 70 RGS / Book-Event Contract

## Purpose

This document defines the runtime contract the Neon Dynasty frontend must satisfy before
a real Stake Engine staging session is considered valid.

## Authentication / startup

The frontend must consume the RGS URL, session ID, language, replay state, game, mode,
version, and event values from the Web SDK runtime URL/configuration. It must not embed
credentials, session IDs, or environment-specific RGS URLs in source code.

Authentication must correctly propagate:

- balance currency and amount
- bet levels / min / max / step configuration
- jurisdiction flags
- an active round that needs to be resumed
- active game mode

Replay mode must use the RGS replay request and reconstruct the stored round without
creating a new wager.

## Book contract

Every received book is treated as ordered, authoritative data.

Required invariants:

1. `events` is an ordered array.
2. Event indexes are deterministic and processed in sequence.
3. `payoutMultiplier` is the round-level payout.
4. Every event type has an explicit TypeScript type.
5. Every event type has exactly one registered handler.
6. Unknown event types fail visibly instead of being silently ignored.
7. A handler may await animation completion before the next event is processed.
8. No handler may reorder events or execute independent book events concurrently.

## Neon Dynasty event families

The implementation must support the project's game-specific event vocabulary, including:

- initial/reveal board
- cluster wins
- tumble / refill
- wild placement
- sticky wild updates
- multiplier updates
- mystery reveal
- dragon meter updates
- dragon-triggered events
- free-spin start/update/end
- retrigger
- total win
- final win
- bonus / feature transitions

The exact serialized event names remain controlled by the Math publication output.
Frontend types and handlers must be regenerated/updated from the actual publication books
when the official Math SDK is run.

## Error handling

- Authentication errors must reach the standard error UI.
- Malformed books must fail closed.
- Unknown event types must fail closed.
- Replay failures must not place the UI into a fake active-round state.
- RGS/network errors must not fabricate balance or payout values.
- Session credentials must never be written to persistent logs.

## Production acceptance

A Build 70 package is NOT production-certified merely because static checks pass.

Production acceptance requires a network-enabled Engine environment to run:

1. official Math SDK simulation/analysis
2. official optimizer where configured
3. publication book + lookup-table generation
4. book/LUT integrity verification
5. official Web SDK production build
6. Stake Engine staging upload
7. real RGS authentication
8. at least one real play in each supported mode
9. replay/resume verification
10. final artifact hash capture

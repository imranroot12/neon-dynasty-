# Neon Dynasty — Build 67 Staging Handoff

## Verified locally
Build 67 adds a static RGS contract audit for:
- authentication/session ID/RGS URL
- play request path
- end-round path
- balance handling
- book-event delivery

## Real staging test still required
The official Web SDK documentation describes a staging flow where a game session
is started from the Stake Engine Developer page and the game is launched in a
new tab. The frontend uses the RGS URL and session ID from the launch/session
parameters.

Required real test sequence:
1. Start a Stake Engine staging game session.
2. Launch Neon Dynasty.
3. Confirm authentication and starting balance.
4. Place a minimum bet and play.
5. Verify every returned book event renders in order.
6. Verify win/balance update.
7. Verify end-round completes.
8. Repeat for normal spin, Mystery Buy, Free Spins and each supported bonus mode.
9. Record session/build identifiers and screenshots/logs.
10. Only then mark RGS integration PASS.

No fake session IDs or synthetic RGS responses are included.

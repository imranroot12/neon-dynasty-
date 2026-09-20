# Build 77 — Packaging and Upstream SDK Gate

Build 77 fixes two concrete delivery issues identified in Build 76:

1. The ZIP is now packaged with the project files at the archive root rather
   than under an extra `build75/` directory. This makes the archive directly
   usable as a repository/workspace checkout.
2. CI now performs an explicit upstream SDK interface preflight after checking
   out the exact Math and Web SDK revisions and before executing the game.

The Math SDK gate verifies the interfaces Neon Dynasty imports for simulation,
configuration generation, optimization, and RGS verification. The Web SDK gate
verifies the workspace files required for the frontend handoff.

This remains an execution gate, not a certification claim. The official SDKs,
optimizer, and RGS must still execute successfully in a network-enabled
GitHub Actions/Stake Engine environment.

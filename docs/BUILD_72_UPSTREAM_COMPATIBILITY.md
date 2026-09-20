# Build 72 — Upstream Compatibility Note

The official Web SDK currently describes cluster games as a bookEvent-driven integration:
create a game-specific bookEvent, register it in the `bookEventHandlerMap`, emit frontend
events, and let Svelte/Pixi components consume those events.

The upstream repository also has active work around cluster event handling and mapping
book-event game types. Therefore Build 72 deliberately does **not** hard-code an assumed
upstream commit as "certified". CI must pin and record the exact Web SDK revision it
actually builds.

Likewise, the Math SDK publication files must come from the same official execution run
that is subsequently verified. Existing local/static books are never treated as proof of
a fresh official run.

## Required evidence

- exact Math SDK revision
- exact Web SDK revision
- Python version
- Rust/Cargo version when optimizer is used
- fresh publication directory hash
- book/LUT verification output
- Web SDK production-build output hash
- real staging/RGS session evidence
- replay/resume evidence

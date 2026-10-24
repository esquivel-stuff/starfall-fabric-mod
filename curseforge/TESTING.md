# Test report, Starfall 1.0.0 (October 23, 2026)

Setup: Fabric dedicated server 1.21.1 (loader 0.19.5, Fabric API 0.116.17+1.21.1) on localhost, two production
Fabric clients ("Alice" and "Bob", offline mode) with the release jar in `mods/`, software rendering under Xvfb.
Audio was captured with OpenAL's wave-file writer because the box has no sound card.

Passed:
- Server boots clean with the mod; no client-only classes are loaded on the server.
- Both clients load the mod and join the same server.
- Blink: exactly 8 blocks forward on flat ground, 1 durability used, client position matches the server (F3).
- Fizzle against a wall up close: no movement, no durability used, "Wand fizzles" subtitle on both clients.
- 2-high wall at 4.5 blocks: stops in front of it. 1-high ledge: steps up onto it.
- Under a low ceiling looking up, and looking straight down: fizzles, player stays safe.
- Never ends inside a block in any test.
- Cooldown: a second click within 0.4 s does nothing, works again after 1.5 s.
- Second player 8 blocks away sees the depart and arrive particles and gets the sound subtitles.
- Audio: the recorded stream on the second client has a burst at the blink, panning from the depart point to the
  arrive point, that correlates best with the mod's own arrive sound.
- Star Block: places in survival, iron pickaxe drops it, bare hand drops nothing.
- Star Cookie at full hunger: eaten, 30 s of Night Vision.
- All 5 recipes give the right item and count (tested with a Crafter); a wrong layout gives nothing.
- 2 Star Shards crafted by hand in the inventory grid.
- Rebuilt jar (this release file) boots on the server, both clients join, a blink moves 8 blocks, and the new wand
  tooltip shows.

Bugs fixed:
- No gameplay bugs found. Text fixes only: the wand tooltip and the fabric.mod.json description said the wand
  "always lands you on your feet", which is not true if you blink in mid-air (you still fall). Both now say it
  never leaves you inside a wall. fabric.mod.json author set to esquivel_stuff and a homepage link added.

Not verified:
- Sound heard through real speakers (only a recorded audio stream was checked).
- Real GPU rendering, frame rate and shaders (Sodium/Iris etc.).
- Online-mode (Microsoft accounts) servers, more than two players, other mods.
- Particle setting levels (All / Decreased / Minimal).

Evidence pictures: `test-evidence/`.

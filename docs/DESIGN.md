# Starfall design notes

These notes cover how the art, effects and sounds were designed and checked. Each section says which of Ian's mod skills it follows: `minecraft-mod-design`, `minecraft-block-design` and `minecraft-spell-vfx`.

## Scope

A small mod: three items, one block, five recipes and one mechanic. It adds no dimensions, mobs, bosses, structures or story. The improvements made the existing content feel finished instead of adding more of it.

## Theme

A falling star. Everything uses the same three ideas: **starlight gold** for anything hot or magic, **dusk violet** for the night the stars come from, and **night navy** for metal and the block rim. The flavour lines in the tooltips follow that story ("Still warm from the fall.", "Leaves the stars a little out of place.").

## Palette

There are five named ramps in `scripts/starfall_art.py` (swatches in `art/palettes/`). They were built with the block-design `palette.py` and then tuned by hand. Each ramp shifts hue as it brightens: gold goes from orange-brown toward warm white, and violet keeps a hue of about 270 to 285. This gives the textures depth without noise.

| Ramp | Used for |
| --- | --- |
| gold (7 steps) | star cores, wand head, sparks |
| violet (7 steps) | shard crystal, block glow, the wand while it recharges |
| navy (6 steps) | wand shaft, Star Block background and rim |
| dough (6 steps) | cookie |
| grip (3 steps) | wand handle |

## Textures

- Item icons have 10 to 13 colours, a selective outline (dark on the shadow side and lighter where the light hits) and one bright highlight cluster. The spent wand was cut from 16 colours to 13 to meet the 14-colour limit.
- The Star Shard, the Blink Wand and the Star Block animate with `.mcmeta`. They hold still most of the time with a short twinkle, so a full inventory does not flicker.
- The Star Block is a framed panel: the rim is lit on the top and left and shaded on the bottom and right, and the stars stay off the rim, so each block reads clearly in a wall (`docs/renders/star_block_tiled.png`, `star_block_cube.png`).
- Particle sprites are grayscale and get their colour in code, so one sprite set serves the whole colour ramp.

Lint results (`tex_lint.py` from minecraft-block-design): items 0 FAIL / 0 WARN, Star Block 0 FAIL / 0 WARN.

`block_check.py` reports a false FAIL for the loot table and the mineable tag. It looks for the 1.20 folder names (`loot_tables/`, `tags/blocks/`), but 1.21 renamed them to `loot_table/` and `tags/block/`. A copy of the data with the old folder names passes 0 FAIL / 0 WARN. The tool itself was not changed.

## Blink VFX (minecraft-spell-vfx, blink archetype)

- **One packet per blink.** The server sends `BlinkFxPayload(from, to, fizzled)` to players within 64 blocks. The client builds all the particles, so the server spawns no particle loop.
- **Beats:**
  - Depart: an implosion (sparks moving inward over 5 to 8 ticks).
  - Path: sparks that burn out toward the end, about 2 per block and 16 at most.
  - Arrive: brighter than the departure, with a flash, an eased ground ring, a burst at two speeds and bouncing embers.
  - Linger: rising motes.
  - A separate fizzle.
- **Colour over life.** Sparks cool from white to pale gold, then gold, then violet. Each one has a random heat offset, so a burst is never a single flat colour.
- **Varied lifetimes.** Every type rolls its own lifetime, so nothing disappears all at once.
- **Full-bright.** The effects stay visible at night.
- **Budget.** Counts scale with the player's Particles setting: 1, 0.5 or 0.2.
- **Lint.** `vfx_lint.py` gives 0 FAIL / 0 WARN.

## Sound (minecraft-mod-design)

Events are named for what happens (`item.blink_wand.depart`, `arrive`, `fizzle`). Each has two variants, a random pitch from 0.9 to 1.1 and a subtitle. The sounds are original and synthesized in `scripts/gen_sounds.py` (seeded, so they rebuild identically):

- Depart: a whoosh with a falling glide.
- Arrive: a soft bell made of inharmonic partials plus a low thump.
- Fizzle: a falling tone with crackle.

## Evidence and honesty

- `docs/screenshots/`: **real** captures from the Minecraft 1.21.1 Fabric dev client, software rendered under Xvfb. The frame rate is low and there was no audio device.
- `docs/renders/`: **texture renders**, meaning flat or isometric images of the texture files. These are not in-game.

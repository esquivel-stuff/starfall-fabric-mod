# Starfall

A small mod about fallen stars. You get one new material, a block that glows, a cookie, and a wand that blinks you forward. That's it. It's small on purpose, and the time went into making those few things feel good.

![Blink Wand in action](https://raw.githubusercontent.com/esquivel-stuff/starfall-fabric-mod/main/docs/screenshots/blink.gif)

## What it adds

**Star Shard.** The crafting material for everything else. It twinkles in your inventory.

**Star Block.** Light level 15 and it stays bright at night. It twinkles slowly and sheds a few motes of starlight. Uses amethyst sounds. You need a pickaxe to get it back, breaking it by hand drops nothing.

**Star Cookie.** Restores 4 hunger (2 drumsticks), can be eaten even when you're full, and gives 30 seconds of Night Vision.

**Blink Wand.** Right-click to blink up to 8 blocks toward where you're looking.
- It never puts you inside a block. If something is in the way, you stop in front of it. If there's a low ledge (up to 2 blocks), it steps you up onto it.
- If there's no room at all (say, you're facing a wall up close), it fizzles: you don't move, no durability is used, and the cooldown is short.
- 64 uses, 1.5 second recharge. The star on the wand dims while it recharges.
- Heads up: blinking in mid-air still leaves you in mid-air. Fall damage is on you.
- Every blink has its own particles and sounds (depart, arrive, fizzle, all with subtitles), and other players nearby see and hear it too.

![Blink sequence](https://raw.githubusercontent.com/esquivel-stuff/starfall-fabric-mod/main/docs/screenshots/blink_sequence.jpg)

![Star Blocks at night](https://raw.githubusercontent.com/esquivel-stuff/starfall-fabric-mod/main/docs/screenshots/star_blocks_night.png)

## Recipes

| Item | Recipe | You get |
| --- | --- | --- |
| Star Shard | Amethyst Shard + Glowstone Dust (shapeless) | 2 |
| Star Block | 9 Star Shards (fill the grid) | 1 |
| Star Shards from a block | 1 Star Block | 9 |
| Star Cookie | Wheat, Star Shard, Wheat in a row | 4 |
| Blink Wand | Ender Pearl, Star Shard and Stick on a diagonal (pearl in a top corner, shard in the middle, stick in the opposite bottom corner) | 1 |

![Blink Wand tooltip](https://raw.githubusercontent.com/esquivel-stuff/starfall-fabric-mod/main/docs/screenshots/tooltip_blink_wand.png)

![Star Block tooltip](https://raw.githubusercontent.com/esquivel-stuff/starfall-fabric-mod/main/docs/screenshots/tooltip_star_block.png)

## Requirements

- Minecraft **1.21.1**
- **Fabric Loader** 0.16.0 or newer
- **Fabric API** for 1.21.1
- Java 21 or newer (the normal Minecraft 1.21.1 launcher already uses it)

## Server and client

- **Singleplayer:** just drop it in your mods folder with Fabric API.
- **Multiplayer:** install it on the server **and** on every player's game. The items, the block and the blink effects need both sides.
- Tested on a 1.21.1 dedicated server with two players connected: blinking, fizzling, the cooldown, the shared particles and sounds, placing and mining the Star Block, the cookie and all five recipes.

## Languages

English and Brazilian Portuguese.

## License and source

MIT licensed. Source code: https://github.com/esquivel-stuff/starfall-fabric-mod

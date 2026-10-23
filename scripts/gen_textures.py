"""Generates every Starfall texture: item icons (+ shine animations), the Star Block (+ twinkle animation),
grayscale particle sprites (tinted in code) and the 128 px mod icon. Run from the project root.
Art rules: minecraft-mod-design (icons) and minecraft-block-design (blocks). All pixels are original."""
import json, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from starfall_art import P, T, RAMPS
import icons, blocks

R = "src/main/resources/assets/starfall/textures"

def save(im, rel, meta=None):
    path = os.path.join(R, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)
    mp = path + ".mcmeta"
    if meta:
        with open(mp, "w") as f: json.dump(meta, f, indent=2); f.write("\n")
    elif os.path.exists(mp):
        os.remove(mp)

def strip(frames):
    s = Image.new('RGBA', (16, 16 * len(frames)), T)
    for i, f in enumerate(frames): s.paste(f, (0, 16 * i))
    return s

# ---- items. Shine sweep: frame 0 held 200 ticks (10 s), then a 2-tick glint along the shard.
shard_frames = [icons.shard()] + [icons.shard(glint=g) for g in (-8, -5, -2, 1, 4, 7)]
save(strip(shard_frames), "item/star_shard.png",
     {"animation": {"frames": [{"index": 0, "time": 200}, 1, 2, 3, 4, 5, 6], "frametime": 2}})
save(icons.cookie(), "item/star_cookie.png")
# Wand: rare twinkle of the star head; a dimmed violet variant is shown by the cooldown model override.
save(strip([icons.wand(), icons.wand(twinkle=1), icons.wand(twinkle=2)]), "item/blink_wand.png",
     {"animation": {"frames": [{"index": 0, "time": 120}, 1, 2, 2, 1], "frametime": 2}})
save(icons.wand('spent'), "item/blink_wand_spent.png")

# ---- block
s, meta = blocks.star_block_anim()
save(s, "block/star_block.png", meta)

# ---- particles: grayscale, the colour comes from code (white -> gold -> violet as they cool)
def gray(v, a=255): return (v, v, v, a)

def p_star(r):
    im = Image.new('RGBA', (8, 8), T); c = 3
    im.putpixel((c, c), gray(255))
    for k in range(1, r + 1):
        v = 240 if k == 1 else 205 if k == 2 else 170
        for dx, dy in ((k, 0), (-k, 0), (0, k), (0, -k)): im.putpixel((c + dx, c + dy), gray(v))
    if r >= 2:
        for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)): im.putpixel((c + dx, c + dy), gray(150))
    return im
for i, r in enumerate((3, 2, 1, 0)):
    save(p_star(r), f"particle/star_spark_{i}.png")

def p_ember(n):
    im = Image.new('RGBA', (8, 8), T)
    for (x, y) in ([(3, 3), (4, 3), (3, 4), (4, 4)] if n == 2 else [(3, 3)]): im.putpixel((x, y), gray(255))
    return im
save(p_ember(2), "particle/star_ember_0.png"); save(p_ember(1), "particle/star_ember_1.png")

def p_flash():
    """Stepped-alpha starburst (pixel steps, no blur): reads as a flash for 2 ticks."""
    im = Image.new('RGBA', (16, 16), T); c = 7.5
    for y in range(16):
        for x in range(16):
            dx, dy = abs(x - c), abs(y - c)
            d = (dx * dx + dy * dy) ** 0.5
            cross = min(dx, dy)
            a = 0
            if d < 2.2: a = 255
            elif d < 3.4: a = 170
            elif d < 4.6: a = 80
            if cross < 1 and d < 7.6: a = max(a, 255 if d < 5 else 170)
            if a: im.putpixel((x, y), gray(255, a))
    return im
save(p_flash(), "particle/star_flash.png")

def p_ring():
    """Ground blastwave: a 2 px pixel ring with a dim inner step, drawn flat on the ground in code."""
    im = Image.new('RGBA', (32, 32), T); c = 15.5
    for y in range(32):
        for x in range(32):
            d = ((x - c) ** 2 + (y - c) ** 2) ** 0.5
            if 13.6 <= d < 15.6: im.putpixel((x, y), gray(255, 255))
            elif 11.6 <= d < 13.6: im.putpixel((x, y), gray(230, 120))
            elif 9.6 <= d < 11.6: im.putpixel((x, y), gray(210, 40))
    return im
save(p_ring(), "particle/blink_ring.png")

# ---- mod icon (128 px): the shard on a night tile, nearest-neighbour upscale
ic = Image.new('RGBA', (16, 16), P['navy'][1])
for y in range(16):
    for x in range(16):
        if (x + y) % 7 == 0 and (x * 3 + y) % 5 == 0: ic.putpixel((x, y), P['navy'][2])
ic.alpha_composite(icons.shard())
ic.resize((128, 128), Image.NEAREST).save("src/main/resources/assets/starfall/icon.png")

# ---- palette strips (authoring tool, like Iron's textures/palettes/; not read by code)
os.makedirs("art/palettes", exist_ok=True)
for name, ramp in P.items():
    pal = Image.new('RGBA', (len(ramp), 1))
    for i, c in enumerate(ramp): pal.putpixel((i, 0), c)
    pal.save(f"art/palettes/{name}.png")
print("textures written")

"""CurseForge project logo (400x400). A 50x50 pixel-art scene drawn on the mod's own palette and textures,
then nearest-neighbour upscaled x8: a Star Shard falling on a glowing Star Block at night.
Run from the project root: python3 scripts/curseforge_logo.py
Needs /tmp/_cube.png first: the Star Block (frame 0 of textures/block/star_block.png) rendered as a 31x36 isometric
cube with the minecraft-block-design skill tool: preview.py cube --top <frame0.png> --scale 1 /tmp/_cube.png"""
import os, sys, math
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from starfall_art import P
import icons

N = 50
im = Image.new('RGBA', (N, N))
navy, violet, gold = P['navy'], P['violet'], P['gold']

# sky: three stepped bands with a checker dither row between them (no airbrush)
for y in range(N):
    for x in range(N):
        band = 0 if y < 14 else (1 if y < 30 else 2)
        if y in (14, 30) and (x + y) % 2 == 0: band -= 1
        im.putpixel((x, y), navy[band])

# distant stars: fixed, hand-picked positions (1 px, two brightness levels)
for x, y, c in [(4, 3, navy[5]), (12, 8, navy[4]), (20, 2, navy[4]), (9, 17, navy[4]), (2, 26, navy[4]),
                (44, 24, navy[4]), (47, 33, navy[5]), (38, 30, navy[4]), (17, 12, violet[5]), (23, 20, navy[4])]:
    im.putpixel((x, y), c)

def cross(cx, cy, core, arm):
    im.putpixel((cx, cy), core)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): im.putpixel((cx + dx, cy + dy), arm)
cross(7, 10, gold[5], gold[3])
cross(43, 40, gold[5], gold[3])

# ground: night grass strip
for y in range(44, N):
    for x in range(N):
        g = [(30, 52, 34, 255), (24, 42, 30, 255), (19, 33, 26, 255)][min(2, (y - 44) // 2)]
        if y == 44 and (x * 7) % 5 == 0: g = (40, 66, 40, 255)
        im.putpixel((x, y), g)

# glow under/around the block: two stepped violet rings on the grass and sky
cube = Image.open('/tmp/_cube.png')
cx0, cy0 = 4, 11
mx, my = cx0 + cube.width / 2, cy0 + cube.height / 2 + 2
for y in range(N):
    for x in range(N):
        d = math.hypot((x - mx) / 1.1, y - my)
        if y < 44 and 15 < d < 20 and (x + y) % 2 == 0: im.putpixel((x, y), navy[2])
        elif y < 44 and d <= 15: im.putpixel((x, y), navy[2] if (x + y) % 2 else navy[3])
        if y >= 44 and abs(x - mx) < 16 - (y - 44) * 3 and (x + y) % 2 == 0: im.putpixel((x, y), violet[1])
im.alpha_composite(cube, (cx0, cy0))

# falling shard + gold trail behind it (up and to the right)
sx, sy = 28, 4
for i in range(18):
    tx, ty = sx + 12 + i, sy + 3 - i
    if 0 <= tx < N and 0 <= ty < N:
        c = gold[5] if i < 3 else gold[3] if i < 7 else gold[2] if i < 12 else gold[1]
        im.putpixel((tx, ty), c)
        if i < 8 and ty + 1 < N: im.putpixel((tx, ty + 1), gold[2] if i < 4 else gold[1])
im.alpha_composite(icons.shard(), (sx, sy))

out = 'curseforge/logo.png'
os.makedirs('curseforge', exist_ok=True)
im.resize((400, 400), Image.NEAREST).convert('RGB').save(out)
im.save('curseforge/logo_50px_source.png')
print('wrote', out)

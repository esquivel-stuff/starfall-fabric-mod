"""Star Block texture, per minecraft-block-design: ramps first, light from the top-left, clusters not noise,
no #000/#fff, bevelled rim (crafted storage block), glow = bright core pixels + same-hue halo + emissive render.
A framed window of night sky: violet crystal rim, navy field with violet nebula wisps, gold stars."""
from PIL import Image
from starfall_art import P, T

G, V, N = P['gold'], P['violet'], P['navy']

FIELD = [  # inner 12x12; o=N1 p=N2 q=N3 1=V1 2=V2 3=V3
    'opp1112pooop',
    'p112221poopp',
    'p1221ppooopq',
    'p121poooopqp',
    'opppoooopp1p',
    'ooooooopp11p',
    'oooooop1121p',
    'pooooop12221',
    'qpoooop1221p',
    'pqpooopp11po',
    'ppqpoooppooo',
    'opppooooooop',
]
FK = {'o': N[1], 'p': N[2], 'q': N[3], '1': V[1], '2': V[2], '3': V[3]}

def star(im, cx, cy, size, bright=0):
    """4-point star, lit from the top-left: upper/left arms one step brighter. bright=1 lengthens the arms."""
    g = G
    pts = {(0, 0): 6}
    if size >= 1:
        pts.update({(-1, 0): 5, (0, -1): 5, (1, 0): 4, (0, 1): 4})
    if size >= 2:
        pts.update({(-2, 0): 3, (0, -2): 3, (2, 0): 2, (0, 2): 2})
        for d in ((-1, -1), (1, -1), (-1, 1), (1, 1)):   # violet halo between the arms
            pts[d] = 'h'
    if size >= 2 and bright:
        pts.update({(-3, 0): 2, (0, -3): 2, (3, 0): 1, (0, 3): 1, (-1, 0): 6, (0, -1): 6})
    for (dx, dy), i in pts.items():
        x, y = cx + dx, cy + dy
        if 0 <= x < 16 and 0 <= y < 16:
            im.putpixel((x, y), V[3] if i == 'h' else g[i])

def star_block(frame=0):
    im = Image.new('RGBA', (16, 16), T)
    for y in range(16):
        for x in range(16):
            ring = min(x, y, 15 - x, 15 - y)
            tl = (x <= y and x + y < 15) or (y < x and x + y < 15)  # placeholder
            if ring == 0:
                c = V[3] if (y == 0 or x == 0) and not (x == 15 or y == 15) else V[0]
                if (x, y) in ((15, 0), (0, 15)): c = V[1]
            elif ring == 1:
                lit = (y == 1 and x < 15) or (x == 1 and y < 15)
                c = V[5] if lit else V[1]
                if (x, y) in ((14, 1), (1, 14)): c = V[2]
                if (x, y) == (1, 1): c = V[6]
            else:
                c = FK[FIELD[y - 2][x - 2]]
            im.putpixel((x, y), c)
    # rim gems at the bevel corners would be noise; keep the rim clean. Stars:
    star(im, 9, 6, 2, bright=(frame == 2))
    star(im, 4, 10, 1)
    tw = {0: (G[5], G[3], V[4]), 1: (G[4], G[5], V[5]), 2: (G[3], G[4], V[4]), 3: (G[5], G[3], V[5])}[frame]
    im.putpixel((4, 4), tw[0])
    im.putpixel((12, 11), tw[1])
    im.putpixel((6, 13), tw[2])
    im.putpixel((12, 3), V[4])
    return im

def star_block_anim():
    frames = [star_block(i) for i in range(4)]
    strip = Image.new('RGBA', (16, 64), T)
    for i, f in enumerate(frames): strip.paste(f, (0, 16 * i))
    return strip, {"animation": {"frametime": 3, "interpolate": False,
                   "frames": [{"index": 0, "time": 60}, 1, 2, 1, {"index": 0, "time": 40}, 3, {"index": 3, "time": 4}, 0]}}

if __name__ == '__main__':
    import sys
    im = star_block(0)
    t = Image.new('RGBA', (48, 48))
    for i in range(3):
        for j in range(3): t.paste(im, (16 * i, 16 * j))
    t.resize((384, 384), Image.NEAREST).save(sys.argv[1])

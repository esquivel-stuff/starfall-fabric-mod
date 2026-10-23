"""Starfall item icons, drawn per minecraft-mod-design references/icon-design.md:
16x16, 1 px margin, coloured outline in each part's darkest step, light from the top-left,
1-3 px specular upper-left, 8-14 colours, no semi-transparent pixels, frame 0 a finished icon."""
from PIL import Image
from starfall_art import P, T

G, V, N, D, L = P['gold'], P['violet'], P['navy'], P['dough'], P['grip']

def blank():
    return Image.new('RGBA', (16, 16), T)

def inside_mask(im):
    return {(x, y) for y in range(16) for x in range(16) if im.getpixel((x, y))[3]}

def boundary(mask):
    out = set()
    for (x, y) in mask:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) not in mask:
                out.add((x, y)); break
    return out

def side(mask, p):
    """which outside directions a boundary pixel faces"""
    x, y = p
    return {d for d, (dx, dy) in {'r': (1, 0), 'l': (-1, 0), 'd': (0, 1), 'u': (0, -1)}.items() if (x + dx, y + dy) not in mask}

# ---------------------------------------------------------------- Star Shard
def _crystal(mask_rng, off=0):
    m = set()
    for y in range(16):
        for x in range(16):
            t, s = x - y, x + y - 15 - off
            r = mask_rng(t)
            if r and r[0] <= s <= r[1]: m.add((x, y))
    return m

def shard(glint=None):
    """A violet night-crystal with a fallen star's gold heart, plus a small sister crystal at its foot.
    Main axis x+y=15, tip top-right. t = x-y runs base -> tip; s = x+y-15 upper-left(-) -> lower-right(+)."""
    def main(t):
        if t < -10 or t > 11: return None
        if t <= -9: return (-1, 1)
        if t <= -7: return (-2, 2)
        if t <= 5:  return (-3, 3)
        if t <= 7:  return (-2, 2)
        if t <= 9:  return (-1, 1)
        return (0, 0)
    def sister(t):
        if t < -8 or t > -1: return None
        if t <= -3: return (-1, 1)
        return (0, 0) if t >= -1 else (-1, 0)
    im = blank()
    big = _crystal(main)
    small = set()
    mask = big | small
    for (x, y) in big:
        s = x + y - 15
        im.putpixel((x, y), V[4] if s <= -2 else V[5] if s == -1 else V[3] if s <= 1 else V[2])
    for (x, y) in small:
        s = x + y - 20
        im.putpixel((x, y), V[3] if s < 0 else V[2] if s == 0 else V[1])
    # gold heart: a little 4-point star caught inside the crystal
    cx, cy = 7, 7
    for (dx, dy, c) in ((0, 0, G[6]), (-1, 0, G[5]), (0, -1, G[5]), (1, 0, G[4]), (0, 1, G[4]),
                        (-2, 0, G[3]), (0, -2, G[3]), (2, 0, G[2]), (0, 2, G[2])):
        im.putpixel((cx + dx, cy + dy), c)
    edge = boundary(mask)
    for p in edge:
        d = side(mask, p); x, y = p; t = x - y
        if p in small:
            im.putpixel(p, V[0] if ('r' in d or 'd' in d) else V[1]); continue
        if ('u' in d or 'l' in d) and not ('r' in d or 'd' in d) and t > -5:
            im.putpixel(p, V[5] if t > 3 else V[4])   # selective outline: the lit edge breaks
        else:
            im.putpixel(p, V[0] if ('r' in d or 'd' in d) else V[1])
    for p in ((11, 3), (10, 4)):                      # specular, upper-left of the tip
        im.putpixel(p, V[6])
    # a loose spark beside it (stray pixels are allowed for sparkles)
    for (x, y, c) in ((3, 3, G[5]), (2, 3, G[3]), (4, 3, G[3]), (3, 2, G[3]), (3, 4, G[3])):
        im.putpixel((x, y), c)
    if glint is not None:                             # shine sweep: a band moving along t, only brightens
        for (x, y) in big - edge:
            if x - y in (glint, glint + 1):
                c = im.getpixel((x, y)); ramp = G if c in G else V
                im.putpixel((x, y), ramp[min(len(ramp) - 1, ramp.index(c) + 2)])
    return im

# ---------------------------------------------------------------- Star Cookie
def cookie():
    """Vanilla-cookie proportions (round, 12 px), dough ramp, with gold star flecks and two violet chips."""
    rows = [
        '................',
        '................',
        '.....EEEEE......',
        '...EEDDDDDEE....',
        '..EDDDDDDDDDC...',
        '..EDD*DDDDDDCB..',
        '.EDD*+*DDvDDCB..',
        '.EDDD*DDDDDDCB..',
        '.DDDDDDDDD*DCB..',
        '.DDDvDDDDDDCCB..',
        '.CDDDDDD*DCCB...',
        '..CCDDDDDCCB....',
        '...BCCCCCBB.....',
        '....ABBBBA......',
        '................',
        '................',
    ]
    pal = {'A': D[0], 'B': D[1], 'C': D[2], 'D': D[3], 'E': D[4], 'F': D[5],
           '*': G[4], '+': G[6], 'v': V[2]}
    im = blank()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.': im.putpixel((x, y), pal[ch])
    mask = inside_mask(im)
    for p in boundary(mask):
        d = side(mask, p)
        if im.getpixel(p) in (G[4], G[6], V[2]): continue
        if 'u' in d or ('l' in d and p[1] < 9): im.putpixel(p, D[4] if p[1] < 6 else D[3])
        else: im.putpixel(p, D[0] if ('d' in d or 'r' in d) else D[1])
    im.putpixel((5, 3), D[5]); im.putpixel((4, 4), D[5])  # top-left sheen
    im.putpixel((9, 6), V[1]); im.putpixel((10, 6), V[3]) # violet chip with a lit edge
    im.putpixel((4, 9), V[1]); im.putpixel((5, 9), V[3])
    return im

# ---------------------------------------------------------------- Blink Wand
def wand(state='ready', twinkle=0):
    """Diagonal navy-metal shaft, leather grip at the base, gold collar, and a 4-point star head
    top-right (all the identity lives in the head). state='spent' dims the star while on cooldown."""
    im = blank()
    # shaft: 2 px wide along x+y=17 -> from (2,14) up to (10,6)
    for i in range(9):
        x, y = 2 + i, 14 - i
        im.putpixel((x, y), N[4] if i > 3 else L[2])      # upper-left pixel: lit
        im.putpixel((x + 1, y), N[2] if i > 3 else L[1])  # lower-right pixel: shade
        if i > 3: im.putpixel((x + 1, y + 1), N[1]) if (x + 1, y + 1) not in inside_mask(im) else None
    for i in range(4):  # grip outline
        x, y = 2 + i, 14 - i
        im.putpixel((x + 1, y + 1), L[0])
    im.putpixel((1, 14), L[0]); im.putpixel((2, 15), L[0]); im.putpixel((1, 15), T)
    # pommel
    im.putpixel((1, 14), G[1]); im.putpixel((2, 14), G[3]); im.putpixel((2, 15), G[0])
    # gold collar at the head
    for (x, y, c) in ((9, 8, G[3]), (10, 8, G[2]), (9, 7, G[4]), (10, 9, G[1]), (11, 8, G[1]), (8, 8, G[2])):
        im.putpixel((x, y), c)
    # star head centred on (12,4)
    cx, cy = 12, 4
    S = G if state == 'ready' else [V[0], V[1], V[1], V[2], V[2], V[3], V[3]]
    star = {(0, 0): 6, (-1, 0): 5, (1, 0): 4, (0, -1): 5, (0, 1): 4,
            (-1, -1): 4, (1, -1): 3, (-1, 1): 3, (1, 1): 2,
            (-2, 0): 4, (2, 0): 2, (0, -2): 4, (0, 2): 2,
            (-3, 0): 1, (3, 0): 0, (0, -3): 1, (0, 3): 0}
    # outline the diamond core in the darkest gold so it sits on any background
    for (dx, dy) in ((-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)):
        star[(dx, dy)] = 0
    if twinkle == 1:
        star.update({(-3, 0): 3, (0, -3): 3, (3, 0): 1, (0, 3): 1})
    if twinkle == 2:
        star.update({(-3, 0): 5, (0, -3): 5, (-1, -1): 6})
    for (dx, dy), i in star.items():
        im.putpixel((cx + dx, cy + dy), S[i])
    if state == 'spent':  # cooled metal too: fewer gold steps keeps the icon inside the 14-colour budget
        swap = {G[0]: G[1], G[4]: G[3]}
        for y in range(16):
            for x in range(16):
                if (x, y) in ((cx + dx, cy + dy) for (dx, dy) in star):
                    continue
                c = im.getpixel((x, y))
                if c in swap: im.putpixel((x, y), swap[c])
    return im

if __name__ == '__main__':
    import sys
    out = sys.argv[1]
    s = Image.new('RGBA', (16 * 6, 16)); 
    for i, im in enumerate([shard(), cookie(), wand(), wand('spent'), shard(glint=0), wand(twinkle=2)]): s.paste(im, (16 * i, 0))
    bg = Image.new('RGBA', s.size, (139, 139, 139, 255)); bg.alpha_composite(s)
    bg.resize((s.width * 10, 160), Image.NEAREST).save(out)

"""Shared palette for Starfall art. Ramps built with minecraft-block-design palette.py, then tuned by hand
(lights pushed toward a warm white so the star reads hot). Dark -> light. Five named ramps for the whole mod."""
H = lambda s: tuple(int(s.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
T = (0, 0, 0, 0)

RAMPS = {
    # starlight gold: warm shift 18 deg -> 52 deg as it brightens
    'gold':   ['#6e2a0e', '#a8500f', '#d98417', '#efb43b', '#f8d868', '#fff0a6', '#fffbe2'],
    # dusk violet: the night the stars fall from; hue holds ~270-285
    'violet': ['#2a1454', '#46237f', '#6537ac', '#8a58d2', '#ae86e4', '#d3bef3', '#f0e7fc'],
    # night navy: wand metal and Star Block rim
    'navy':   ['#0d0d27', '#181a45', '#242862', '#323b7e', '#43579b', '#6479ad'],
    # cookie dough
    'dough':  ['#5a2412', '#87401d', '#a96229', '#c78236', '#dca560', '#ebc78c'],
    # wand grip leather
    'grip':   ['#2e1410', '#4d2318', '#6e3622'],
}
P = {k: [H(c) for c in v] for k, v in RAMPS.items()}

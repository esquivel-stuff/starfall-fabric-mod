"""Generates the mod's original 16x16 pixel-art textures (and a 128px icon).
Every texture is drawn from the character grids below - no external assets."""
import os
from PIL import Image

R = "src/main/resources/assets/starfall"

PAL = {
    ".": (0, 0, 0, 0),
    "k": (38, 20, 66, 255),     # outline / deep violet
    "d": (76, 41, 128, 255),    # dark purple
    "p": (128, 74, 196, 255),   # purple
    "l": (178, 132, 240, 255),  # light purple
    "w": (246, 238, 255, 255),  # highlight
    "y": (255, 214, 92, 255),   # star gold
    "o": (232, 156, 48, 255),   # dark gold
    "b": (110, 70, 38, 255),    # wood dark
    "B": (156, 104, 58, 255),   # wood light
    "c": (196, 140, 80, 255),   # cookie dark
    "C": (226, 178, 112, 255),  # cookie
    "h": (244, 208, 150, 255),  # cookie highlight
    "n": (52, 28, 88, 255),     # block base
    "m": (64, 36, 106, 255),    # block base 2
}

STAR_SHARD = """
................
..........kk....
.........kwlk...
........kwllpk..
.......kwllppk..
......kwllppdk..
.....kwllppdk...
....kwlyppdk....
...kwlyyypk.....
..kllpyppdk.....
..klppppdk......
..kdpppdk.......
...kddddk.......
....kkkk........
................
................
"""

STAR_BLOCK = """
kkkkkkkkkkkkkkkk
knmnnmnnnmnnmnnk
kmnnnnynnnnnnnmk
knnnnyyynnnnnnnk
knnyyywyyynnlnnk
knnnnyyynnnnnmnk
kmnnnyny.nnnnnnk
knnnnnnnnnnnnnnk
knnlnnnnnnnynnnk
knnnnnnnnnyyynmk
kmnnnnnnnnnynnnk
knnnnnynnnnnnnnk
knnnnyyynnnnlnnk
knmnnnynnnnnnnnk
knnnnnnnnmnnnmnk
kkkkkkkkkkkkkkkk
"""

STAR_COOKIE = """
................
.....cccccc.....
...cchhhhCCcc...
..chhCCCCCCCCc..
..chCClCCCyCCc..
.chCCCCCCCCCCCc.
.cCCyCCCCCCpCCc.
.cCCCCCCCCCCCCc.
.cCCCCCpCCCCCCc.
.cCCCCCCCCCyCCc.
.cCCplCCCCCCCcc.
..cCCCCCyCCCCc..
..ccCCCCCCCccc..
...cccCCCccc....
.....cccccc.....
................
"""

BLINK_WAND = """
............y...
.........y.kyk..
..........kywyk.
.........kywwwyk
..........kywyk.
...........kyk.y
..........bk....
.........bBb....
........bBb.....
.......bBb......
......bBb.......
.....bBb........
....bBb.........
...bBb..........
..bBb...........
..bb............
"""

def draw(grid):
    rows = [r for r in grid.strip("\n").split("\n")]
    assert len(rows) == 16 and all(len(r) == 16 for r in rows), [len(r) for r in rows]
    img = Image.new("RGBA", (16, 16))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            img.putpixel((x, y), PAL[ch])
    return img

def save(img, rel):
    path = os.path.join(R, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)

if __name__ == "__main__":
    # Star block uses '.' as a twinkle pixel - replace with base colour.
    save(draw(STAR_SHARD), "textures/item/star_shard.png")
    save(draw(STAR_BLOCK.replace(".", "n")), "textures/block/star_block.png")
    save(draw(STAR_COOKIE), "textures/item/star_cookie.png")
    save(draw(BLINK_WAND), "textures/item/blink_wand.png")

    icon = Image.new("RGBA", (128, 128), (52, 28, 88, 255))
    shard = draw(STAR_SHARD).resize((112, 112), Image.NEAREST)
    icon.alpha_composite(shard, (8, 8))
    save(icon, "icon.png")
    print("textures written")

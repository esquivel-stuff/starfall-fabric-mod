"""Generates the mod's JSON assets/data files. Run from the project root."""
import json, os

R = "src/main/resources"
NS = "starfall"

def w(path, obj):
    path = os.path.join(R, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")

w("fabric.mod.json", {
    "schemaVersion": 1,
    "id": NS,
    "version": "${version}",
    "name": "Starfall",
    "description": "A small Fabric mod about fallen stars: Star Shards, a glowing Star Block, Star Cookies and a Blink Wand that blinks you up to 8 blocks forward and always lands you on your feet.",
    "authors": ["esquivel-stuff"],
    "contact": {"sources": "https://github.com/esquivel-stuff/starfall-fabric-mod"},
    "license": "MIT",
    "icon": "assets/starfall/icon.png",
    "environment": "*",
    "entrypoints": {
        "main": ["dev.esquivel.starfall.Starfall"],
        "client": ["dev.esquivel.starfall.client.StarfallClient"],
    },
    "depends": {"fabricloader": ">=0.16.0", "minecraft": "~1.21.1", "java": ">=21", "fabric-api": "*"},
})

# Item models. The wand swaps to its dimmed "spent" texture while on cooldown (starfall:cooldown predicate).
for item in ["star_shard", "star_cookie"]:
    w(f"assets/{NS}/models/item/{item}.json",
      {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/{item}"}})
w(f"assets/{NS}/models/item/blink_wand.json", {
    "parent": "minecraft:item/handheld",
    "textures": {"layer0": f"{NS}:item/blink_wand"},
    "overrides": [{"predicate": {f"{NS}:cooldown": 0.01}, "model": f"{NS}:item/blink_wand_spent"}],
})
w(f"assets/{NS}/models/item/blink_wand_spent.json",
  {"parent": "minecraft:item/handheld", "textures": {"layer0": f"{NS}:item/blink_wand_spent"}})

w(f"assets/{NS}/blockstates/star_block.json", {"variants": {"": {"model": f"{NS}:block/star_block"}}})
w(f"assets/{NS}/models/block/star_block.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/star_block"}})
w(f"assets/{NS}/models/item/star_block.json", {"parent": f"{NS}:block/star_block"})

# Particles: grayscale sprites, tinted and aged in code (client/particle).
SPARK = [f"{NS}:star_spark_{i}" for i in range(4)]
for name, tex in {
    "star_spark": SPARK,
    "star_mote": SPARK[1:],
    "star_ember": [f"{NS}:star_ember_0", f"{NS}:star_ember_1"],
    "star_flash": [f"{NS}:star_flash"],
    "blink_ring": [f"{NS}:blink_ring"],
}.items():
    w(f"assets/{NS}/particles/{name}.json", {"textures": tex})

# Sounds: original synthesized .ogg files (scripts/gen_sounds.py), two variants per event, named by event.
def sound(event, files):
    return {"subtitle": f"subtitles.{NS}.{event}", "sounds": [f"{NS}:{f}" for f in files]}
w(f"assets/{NS}/sounds.json", {
    "item.blink_wand.depart": sound("item.blink_wand.depart", ["blink/depart1", "blink/depart2"]),
    "item.blink_wand.arrive": sound("item.blink_wand.arrive", ["blink/arrive1", "blink/arrive2"]),
    "item.blink_wand.fizzle": sound("item.blink_wand.fizzle", ["blink/fizzle1", "blink/fizzle2"]),
})

w(f"assets/{NS}/lang/en_us.json", {
    "itemGroup.starfall.main": "Starfall",
    "item.starfall.star_shard": "Star Shard",
    "item.starfall.star_shard.tooltip.0": "Crafts Star Blocks, Star Cookies and the Blink Wand",
    "item.starfall.star_shard.tooltip.1": "Still warm from the fall.",
    "item.starfall.star_cookie": "Star Cookie",
    "item.starfall.star_cookie.tooltip.0": "Night Vision for 30 seconds",
    "item.starfall.star_cookie.tooltip.1": "Baked under an open sky.",
    "item.starfall.blink_wand": "Blink Wand",
    "item.starfall.blink_wand.tooltip.0": "Use to blink up to %s blocks where you look",
    "item.starfall.blink_wand.tooltip.1": "Always lands on your feet. Recharge: %ss",
    "item.starfall.blink_wand.tooltip.2": "Leaves the stars a little out of place.",
    "block.starfall.star_block": "Star Block",
    "block.starfall.star_block.tooltip.0": "Light level 15. Sheds motes of starlight",
    "block.starfall.star_block.tooltip.1": "Nine shards, packed until they hum.",
    "subtitles.starfall.item.blink_wand.depart": "Wand blinks away",
    "subtitles.starfall.item.blink_wand.arrive": "Starlight lands",
    "subtitles.starfall.item.blink_wand.fizzle": "Wand fizzles",
})
w(f"assets/{NS}/lang/pt_br.json", {
    "itemGroup.starfall.main": "Starfall",
    "item.starfall.star_shard": "Fragmento Estelar",
    "item.starfall.star_shard.tooltip.0": "Usado em Blocos Estelares, Biscoitos Estelares e na Varinha de Salto",
    "item.starfall.star_shard.tooltip.1": "Ainda quente da queda.",
    "item.starfall.star_cookie": "Biscoito Estelar",
    "item.starfall.star_cookie.tooltip.0": "Visão Noturna por 30 segundos",
    "item.starfall.star_cookie.tooltip.1": "Assado sob o céu aberto.",
    "item.starfall.blink_wand": "Varinha de Salto",
    "item.starfall.blink_wand.tooltip.0": "Use para saltar até %s blocos para onde olha",
    "item.starfall.blink_wand.tooltip.1": "Sempre cai de pé. Recarga: %ss",
    "item.starfall.blink_wand.tooltip.2": "Deixa as estrelas um pouco fora do lugar.",
    "block.starfall.star_block": "Bloco Estelar",
    "block.starfall.star_block.tooltip.0": "Nível de luz 15. Solta partículas de luz estelar",
    "block.starfall.star_block.tooltip.1": "Nove fragmentos, compactados até zumbirem.",
    "subtitles.starfall.item.blink_wand.depart": "Varinha some",
    "subtitles.starfall.item.blink_wand.arrive": "Luz estelar pousa",
    "subtitles.starfall.item.blink_wand.fizzle": "Varinha falha",
})

# Recipes (1.21 uses the singular "recipe" folder and "id" in results)
w(f"data/{NS}/recipe/star_shard.json", {
    "type": "minecraft:crafting_shapeless", "category": "misc",
    "ingredients": [{"item": "minecraft:amethyst_shard"}, {"item": "minecraft:glowstone_dust"}],
    "result": {"id": f"{NS}:star_shard", "count": 2}})
w(f"data/{NS}/recipe/star_block.json", {
    "type": "minecraft:crafting_shaped", "category": "building",
    "pattern": ["###", "###", "###"], "key": {"#": {"item": f"{NS}:star_shard"}},
    "result": {"id": f"{NS}:star_block", "count": 1}})
w(f"data/{NS}/recipe/star_shard_from_block.json", {
    "type": "minecraft:crafting_shapeless", "category": "misc",
    "ingredients": [{"item": f"{NS}:star_block"}],
    "result": {"id": f"{NS}:star_shard", "count": 9}})
w(f"data/{NS}/recipe/star_cookie.json", {
    "type": "minecraft:crafting_shaped", "category": "misc",
    "pattern": ["W*W"], "key": {"W": {"item": "minecraft:wheat"}, "*": {"item": f"{NS}:star_shard"}},
    "result": {"id": f"{NS}:star_cookie", "count": 4}})
w(f"data/{NS}/recipe/blink_wand.json", {
    "type": "minecraft:crafting_shaped", "category": "equipment",
    "pattern": ["  E", " * ", "/  "],
    "key": {"E": {"item": "minecraft:ender_pearl"}, "*": {"item": f"{NS}:star_shard"}, "/": {"item": "minecraft:stick"}},
    "result": {"id": f"{NS}:blink_wand", "count": 1}})

w(f"data/{NS}/loot_table/blocks/star_block.json", {
    "type": "minecraft:block",
    "pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{NS}:star_block"}],
               "conditions": [{"condition": "minecraft:survives_explosion"}]}]})
w("data/minecraft/tags/block/mineable/pickaxe.json", {"replace": False, "values": [f"{NS}:star_block"]})
print("resources written")

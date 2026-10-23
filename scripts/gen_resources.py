"""Generates the mod's JSON assets/data files. Run from the project root."""
import json, os

R = "src/main/resources"
NS = "starfall"

def w(path, obj):
    path = os.path.join(R, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")

w("fabric.mod.json", {
    "schemaVersion": 1,
    "id": NS,
    "version": "${version}",
    "name": "Starfall (Demo)",
    "description": "A small demo mod: Star Shards, a glowing Star Block, Star Cookies and a Blink Wand that teleports you a few blocks forward.",
    "authors": ["esquivel-stuff"],
    "contact": {"sources": "https://github.com/esquivel-stuff/fabric-mod-demo"},
    "license": "MIT",
    "icon": "assets/starfall/icon.png",
    "environment": "*",
    "entrypoints": {"main": ["dev.esquivel.starfall.Starfall"]},
    "depends": {"fabricloader": ">=0.16.0", "minecraft": "~1.21.1", "java": ">=21", "fabric-api": "*"},
})

for item, parent in [("star_shard", "generated"), ("star_cookie", "generated"), ("blink_wand", "handheld")]:
    w(f"assets/{NS}/models/item/{item}.json",
      {"parent": f"minecraft:item/{parent}", "textures": {"layer0": f"{NS}:item/{item}"}})

w(f"assets/{NS}/blockstates/star_block.json", {"variants": {"": {"model": f"{NS}:block/star_block"}}})
w(f"assets/{NS}/models/block/star_block.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/star_block"}})
w(f"assets/{NS}/models/item/star_block.json", {"parent": f"{NS}:block/star_block"})

w(f"assets/{NS}/lang/en_us.json", {
    "itemGroup.starfall.main": "Starfall",
    "item.starfall.star_shard": "Star Shard",
    "item.starfall.star_cookie": "Star Cookie",
    "item.starfall.blink_wand": "Blink Wand",
    "block.starfall.star_block": "Star Block",
})
w(f"assets/{NS}/lang/pt_br.json", {
    "itemGroup.starfall.main": "Starfall",
    "item.starfall.star_shard": "Fragmento Estelar",
    "item.starfall.star_cookie": "Biscoito Estelar",
    "item.starfall.blink_wand": "Varinha de Salto",
    "block.starfall.star_block": "Bloco Estelar",
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

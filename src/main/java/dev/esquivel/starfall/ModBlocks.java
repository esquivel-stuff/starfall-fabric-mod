package dev.esquivel.starfall;

import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import dev.esquivel.starfall.block.StarBlock;
import dev.esquivel.starfall.item.LoreBlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;

public final class ModBlocks {
	static final int COUNT = 1;

	/**
	 * Nine Star Shards. Light 15 and emissive rendering (vanilla's magma flag), so its stars stay bright
	 * at night and in caves instead of being shaded like a normal block.
	 */
	public static final Block STAR_BLOCK = register("star_block", new StarBlock(
			BlockBehaviour.Properties.of()
					.mapColor(MapColor.COLOR_PURPLE)
					.strength(1.5f, 6.0f)
					.sound(SoundType.AMETHYST)
					.lightLevel(state -> 15)
					.emissiveRendering((state, level, pos) -> true)
					.requiresCorrectToolForDrops()), 2);

	private ModBlocks() {}

	private static Block register(String name, Block block, int loreLines) {
		ResourceLocation id = Starfall.id(name);
		Block registered = Registry.register(BuiltInRegistries.BLOCK, id, block);
		Registry.register(BuiltInRegistries.ITEM, id, new LoreBlockItem(registered, new Item.Properties(), loreLines));
		return registered;
	}

	static void register() {
		// Static initialiser does the work; this forces class loading at mod init.
	}
}

package dev.esquivel.starfall;

import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;

public final class ModBlocks {
	static final int COUNT = 1;

	/** A glowing decorative block made from nine Star Shards. Emits full light. */
	public static final Block STAR_BLOCK = register("star_block", new Block(
			BlockBehaviour.Properties.of()
					.mapColor(MapColor.COLOR_PURPLE)
					.strength(1.5f, 6.0f)
					.sound(SoundType.AMETHYST)
					.lightLevel(state -> 15)
					.requiresCorrectToolForDrops()));

	private ModBlocks() {}

	private static Block register(String name, Block block) {
		ResourceLocation id = ResourceLocation.fromNamespaceAndPath(Starfall.MOD_ID, name);
		Block registered = Registry.register(BuiltInRegistries.BLOCK, id, block);
		Registry.register(BuiltInRegistries.ITEM, id, new BlockItem(registered, new Item.Properties()));
		return registered;
	}

	static void register() {
		// Static initialiser does the work; this forces class loading at mod init.
	}
}

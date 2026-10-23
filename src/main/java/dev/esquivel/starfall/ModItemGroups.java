package dev.esquivel.starfall;

import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;

public final class ModItemGroups {
	public static final CreativeModeTab STARFALL_TAB = Registry.register(
			BuiltInRegistries.CREATIVE_MODE_TAB,
			ResourceLocation.fromNamespaceAndPath(Starfall.MOD_ID, "main"),
			FabricItemGroup.builder()
					.title(Component.translatable("itemGroup.starfall.main"))
					.icon(() -> new ItemStack(ModItems.STAR_SHARD))
					.displayItems((params, output) -> {
						output.accept(ModItems.STAR_SHARD);
						output.accept(ModBlocks.STAR_BLOCK);
						output.accept(ModItems.STAR_COOKIE);
						output.accept(ModItems.BLINK_WAND);
					})
					.build());

	private ModItemGroups() {}

	static void register() {
		// Forces static initialisation.
	}
}

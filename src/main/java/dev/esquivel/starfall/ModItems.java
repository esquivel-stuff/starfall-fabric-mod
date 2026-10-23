package dev.esquivel.starfall;

import dev.esquivel.starfall.item.BlinkWandItem;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;

public final class ModItems {
	static final int COUNT = 3;

	/** Crafting ingredient: amethyst + glowstone. */
	public static final Item STAR_SHARD = register("star_shard",
			new Item(new Item.Properties()));

	/** Food that grants 30 seconds of Night Vision. */
	public static final Item STAR_COOKIE = register("star_cookie",
			new Item(new Item.Properties().food(new FoodProperties.Builder()
					.nutrition(4)
					.saturationModifier(0.6f)
					.alwaysEdible()
					.effect(new MobEffectInstance(MobEffects.NIGHT_VISION, 20 * 30), 1.0f)
					.build())));

	/** Right-click to blink up to 8 blocks in the direction you are looking. */
	public static final Item BLINK_WAND = register("blink_wand",
			new BlinkWandItem(new Item.Properties().durability(64).rarity(Rarity.UNCOMMON)));

	private ModItems() {}

	private static Item register(String name, Item item) {
		return Registry.register(BuiltInRegistries.ITEM,
				ResourceLocation.fromNamespaceAndPath(Starfall.MOD_ID, name), item);
	}

	static void register() {
		// Forces static initialisation.
	}
}

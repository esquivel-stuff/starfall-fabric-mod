package dev.esquivel.starfall;

import dev.esquivel.starfall.network.BlinkFxPayload;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.minecraft.resources.ResourceLocation;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** Entry point for Starfall: a small mod about catching fallen stars. */
public class Starfall implements ModInitializer {
	public static final String MOD_ID = "starfall";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	public static ResourceLocation id(String path) {
		return ResourceLocation.fromNamespaceAndPath(MOD_ID, path);
	}

	@Override
	public void onInitialize() {
		ModSounds.register();
		ModParticles.register();
		ModBlocks.register();
		ModItems.register();
		ModItemGroups.register();
		// One small S2C packet per blink; clients expand it into the whole effect.
		PayloadTypeRegistry.playS2C().register(BlinkFxPayload.TYPE, BlinkFxPayload.CODEC);
		LOGGER.info("Starfall loaded: {} items, {} blocks, {} particles, {} sounds",
				ModItems.COUNT, ModBlocks.COUNT, ModParticles.COUNT, ModSounds.COUNT);
	}
}

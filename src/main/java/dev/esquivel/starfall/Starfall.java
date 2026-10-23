package dev.esquivel.starfall;

import net.fabricmc.api.ModInitializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** Entry point for the Starfall demo mod. */
public class Starfall implements ModInitializer {
	public static final String MOD_ID = "starfall";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	@Override
	public void onInitialize() {
		ModBlocks.register();
		ModItems.register();
		ModItemGroups.register();
		LOGGER.info("Starfall loaded: {} items, {} blocks", ModItems.COUNT, ModBlocks.COUNT);
	}
}

package dev.esquivel.starfall;

import net.fabricmc.fabric.api.particle.v1.FabricParticleTypes;
import net.minecraft.core.Registry;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.core.registries.BuiltInRegistries;

/** Particle types. Behaviour lives in the client particle classes; sprites are grayscale and tinted there. */
public final class ModParticles {
	static final int COUNT = 5;

	/** 4-point star that shrinks as it cools from white through gold to violet. */
	public static final SimpleParticleType STAR_SPARK = register("star_spark");
	/** Heavy spark that falls and bounces off the ground. */
	public static final SimpleParticleType STAR_EMBER = register("star_ember");
	/** Two-tick flash at the moment of arrival. */
	public static final SimpleParticleType STAR_FLASH = register("star_flash");
	/** Flat ring that runs out along the ground under your feet. */
	public static final SimpleParticleType BLINK_RING = register("blink_ring");
	/** Slow rising mote: the Star Block's idle shimmer and the blink's linger. */
	public static final SimpleParticleType STAR_MOTE = register("star_mote");

	private ModParticles() {}

	private static SimpleParticleType register(String name) {
		// alwaysShow=false: the player's particle setting still applies.
		return Registry.register(BuiltInRegistries.PARTICLE_TYPE, Starfall.id(name), FabricParticleTypes.simple(false));
	}

	static void register() {
		// Forces static initialisation.
	}
}

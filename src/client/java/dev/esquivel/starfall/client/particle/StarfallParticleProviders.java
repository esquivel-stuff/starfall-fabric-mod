package dev.esquivel.starfall.client.particle;

import dev.esquivel.starfall.ModParticles;
import net.fabricmc.fabric.api.client.particle.v1.ParticleFactoryRegistry;
import net.minecraft.client.particle.ParticleRenderType;

/** Registers a provider per particle type. Spawning code tunes motion and life on the returned particle. */
public final class StarfallParticleProviders {
	private StarfallParticleProviders() {}

	public static void register() {
		ParticleFactoryRegistry registry = ParticleFactoryRegistry.getInstance();
		registry.register(ModParticles.STAR_SPARK, sprites -> (type, level, x, y, z, xd, yd, zd) ->
				new StarfallParticle(level, x, y, z, sprites, ParticleRenderType.PARTICLE_SHEET_OPAQUE)
						.motion(xd, yd, zd).size(0.11f).life(8 + level.random.nextInt(6)));
		registry.register(ModParticles.STAR_EMBER, sprites -> (type, level, x, y, z, xd, yd, zd) ->
				new StarfallParticle(level, x, y, z, sprites, ParticleRenderType.PARTICLE_SHEET_OPAQUE)
						.motion(xd, yd, zd).size(0.06f).life(20 + level.random.nextInt(14))
						.drag(0.97f).falling(1.3f, 2, 0.6f + level.random.nextFloat() * 0.2f));
		registry.register(ModParticles.STAR_FLASH, sprites -> (type, level, x, y, z, xd, yd, zd) ->
				new FlashParticle(level, x, y, z, sprites));
		registry.register(ModParticles.BLINK_RING, sprites -> (type, level, x, y, z, xd, yd, zd) ->
				new RingParticle(level, x, y, z, sprites));
		registry.register(ModParticles.STAR_MOTE, sprites -> (type, level, x, y, z, xd, yd, zd) ->
				new StarfallParticle(level, x, y, z, sprites, ParticleRenderType.PARTICLE_SHEET_OPAQUE)
						.motion(xd, yd, zd).size(0.05f + level.random.nextFloat() * 0.03f)
						.life(24 + level.random.nextInt(20)).drag(0.98f).heat(0.25f));
	}
}

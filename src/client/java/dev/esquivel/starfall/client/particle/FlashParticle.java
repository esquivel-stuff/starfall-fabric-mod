package dev.esquivel.starfall.client.particle;

import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.particle.ParticleRenderType;
import net.minecraft.client.particle.SpriteSet;

/** The 2-3 tick flash on arrival: pops to full size, swells 30 % and fades out (no hold, no linger). */
public class FlashParticle extends StarfallParticle {
	FlashParticle(ClientLevel level, double x, double y, double z, SpriteSet sprites) {
		super(level, x, y, z, sprites, ParticleRenderType.PARTICLE_SHEET_TRANSLUCENT);
		this.lifetime = 2 + this.random.nextInt(2);
		this.fadeAlpha = true;
		this.friction = 0;
		size(0.75f);
	}

	@Override
	protected void applyCurves(float f) {
		this.setColor(1.0f, 0.96f, 0.80f);
		this.quadSize = startSize * (1 + 0.3f * f);
		this.setAlpha(1 - f);
	}
}

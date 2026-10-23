package dev.esquivel.starfall.client.particle;

import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.Camera;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.particle.ParticleRenderType;
import net.minecraft.client.particle.SpriteSet;
import net.minecraft.util.Mth;
import org.joml.Quaternionf;

/**
 * Ground blastwave: a flat ring under the caster's feet. Radius eases out (R * lerp(outQuad(f), 0.75, 1)) over
 * 8-10 ticks while alpha falls 1 - f, so the shock reads as fast-then-settling instead of linear.
 */
public class RingParticle extends StarfallParticle {
	private static final Quaternionf FACE_UP = new Quaternionf().rotationX((float) -Math.PI / 2);
	private static final Quaternionf FACE_DOWN = new Quaternionf().rotationX((float) Math.PI / 2);
	private final float radius;

	RingParticle(ClientLevel level, double x, double y, double z, SpriteSet sprites) {
		super(level, x, y, z, sprites, ParticleRenderType.PARTICLE_SHEET_TRANSLUCENT);
		this.lifetime = 8 + this.random.nextInt(3);
		this.friction = 0;
		this.radius = 1.6f;
		applyCurves(0);
	}

	@Override
	protected void applyCurves(float f) {
		float ease = 1 - (1 - f) * (1 - f);
		this.quadSize = radius * Mth.lerp(ease, 0.75f, 1.0f);
		this.setAlpha(1 - f);
		float heat = f * 0.6f;
		this.setColor(Mth.lerp(heat, 1.0f, 0.94f), Mth.lerp(heat, 0.96f, 0.71f), Mth.lerp(heat, 0.80f, 0.23f));
	}

	@Override
	public void render(VertexConsumer buffer, Camera camera, float partialTick) {
		// Two faces so the ring is visible from above and from below (particles have no backface pass).
		this.renderRotatedQuad(buffer, camera, FACE_UP, partialTick);
		this.renderRotatedQuad(buffer, camera, FACE_DOWN, partialTick);
	}

	@Override
	public float getQuadSize(float partialTick) {
		return this.quadSize;
	}
}

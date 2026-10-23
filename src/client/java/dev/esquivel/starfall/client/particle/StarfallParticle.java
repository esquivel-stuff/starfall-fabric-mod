package dev.esquivel.starfall.client.particle;

import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.particle.ParticleRenderType;
import net.minecraft.client.particle.SpriteSet;
import net.minecraft.client.particle.TextureSheetParticle;
import net.minecraft.client.renderer.LightTexture;
import net.minecraft.util.Mth;

/**
 * Shared behaviour for every Starfall particle (minecraft-spell-vfx rules):
 * full-bright, colour cools along a white -> pale gold -> gold -> violet ramp, size and alpha follow curves over
 * life, lifetimes are randomised per particle, optional gravity with bounce. Sprites are grayscale and tinted here.
 */
public class StarfallParticle extends TextureSheetParticle {
	/** The cooling ramp: hot white, pale gold, gold, dusk violet (same hues as the item and block ramps). */
	static final float[][] COOL = {
			{1.00f, 0.99f, 0.89f}, {1.00f, 0.94f, 0.65f}, {0.94f, 0.71f, 0.23f}, {0.54f, 0.35f, 0.82f}};

	protected final SpriteSet sprites;
	protected final ParticleRenderType renderType;
	protected float startSize;
	/** 0 = starts white-hot, 1 = starts already cooled to gold (departure is dimmer than arrival). */
	protected float heatOffset;
	protected boolean fadeAlpha;
	protected int bouncesLeft;
	protected float bounce = 0.7f;

	protected StarfallParticle(ClientLevel level, double x, double y, double z, SpriteSet sprites,
			ParticleRenderType renderType) {
		super(level, x, y, z);
		this.sprites = sprites;
		this.renderType = renderType;
		this.hasPhysics = false;
		this.gravity = 0;
		this.friction = 0.9f;
		this.startSize = this.quadSize;
		this.setSpriteFromAge(sprites);
		applyCurves(0);
	}

	public StarfallParticle motion(double xd, double yd, double zd) {
		this.xd = xd; this.yd = yd; this.zd = zd;
		return this;
	}

	public StarfallParticle life(int ticks) {
		this.lifetime = Math.max(1, ticks);
		return this;
	}

	public StarfallParticle size(float quadSize) {
		this.quadSize = quadSize;
		this.startSize = quadSize;
		return this;
	}

	public StarfallParticle drag(float friction) {
		this.friction = friction;
		return this;
	}

	public StarfallParticle heat(float offset) {
		this.heatOffset = offset;
		applyCurves(0);
		return this;
	}

	/** Falls with {@code gravity} (vanilla units) and bounces off the ground up to {@code bounces} times. */
	public StarfallParticle falling(float gravity, int bounces, float bounce) {
		this.gravity = gravity;
		this.hasPhysics = true;
		this.bouncesLeft = bounces;
		this.bounce = bounce;
		return this;
	}

	@Override
	public void tick() {
		double fallingSpeed = this.yd;
		super.tick();
		if (this.removed) return;
		if (this.hasPhysics && this.onGround && fallingSpeed < -0.02 && bouncesLeft > 0) {
			this.yd = -fallingSpeed * bounce;
			this.xd *= 0.8; this.zd *= 0.8;
			bouncesLeft--;
		}
		this.setSpriteFromAge(sprites);
		applyCurves((float) this.age / this.lifetime);
	}

	/** f = 0..1 over life. Subclasses override for flash and ring shapes. */
	protected void applyCurves(float f) {
		float heat = Mth.clamp(heatOffset + f * (1 - heatOffset), 0, 1) * (COOL.length - 1);
		int i = Math.min((int) heat, COOL.length - 2);
		float t = heat - i;
		this.setColor(Mth.lerp(t, COOL[i][0], COOL[i + 1][0]), Mth.lerp(t, COOL[i][1], COOL[i + 1][1]),
				Mth.lerp(t, COOL[i][2], COOL[i + 1][2]));
		this.quadSize = startSize * (1 - 0.55f * f * f); // hold, then shrink late
		if (fadeAlpha) this.setAlpha(1 - f * f);
	}

	@Override
	protected int getLightColor(float partialTick) {
		return LightTexture.FULL_BRIGHT;
	}

	@Override
	public ParticleRenderType getRenderType() {
		return renderType;
	}
}

package dev.esquivel.starfall.client;

import dev.esquivel.starfall.ModParticles;
import dev.esquivel.starfall.client.particle.StarfallParticle;
import dev.esquivel.starfall.network.BlinkFxPayload;
import net.minecraft.client.Minecraft;
import net.minecraft.client.ParticleStatus;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.particle.Particle;
import net.minecraft.client.particle.ParticleEngine;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.util.Mth;
import net.minecraft.util.RandomSource;
import net.minecraft.world.phys.Vec3;

/**
 * Client-side expansion of one {@link BlinkFxPayload} into the Blink effect (minecraft-spell-vfx archetype 5.9,
 * "blink"). Five beats:
 * <ol>
 *   <li>Depart: a brief flash, the body collapses inward (sparks with mirrored, inward velocity), a few motes
 *       are left behind, plus the depart sound (played by the server). Cooler colours than the arrival.</li>
 *   <li>Path: a sampled line of sparks along the jump whose lifetimes grow toward the end, so the trail
 *       burns out from where you left to where you land and reads as direction.</li>
 *   <li>Arrive: white flash (2-3 ticks), ground ring (ease-out), fast burst, slow burst, plus the arrive sound.</li>
 *   <li>Debris: heavy embers that fall and bounce.</li>
 *   <li>Linger: slow motes rising around your feet, then nothing.</li>
 * </ol>
 * Every count is scaled by the particle setting (All 1, Decreased 0.5, Minimal 0.2).
 */
public final class BlinkFx {
	private BlinkFx() {}

	public static void play(BlinkFxPayload fx) {
		Minecraft mc = Minecraft.getInstance();
		ClientLevel level = mc.level;
		if (level == null) return;
		float k = budget(mc.options.particles().get());
		RandomSource r = level.random;
		ParticleEngine engine = mc.particleEngine;
		Vec3 bodyFrom = fx.from().add(0, 0.9, 0);
		if (fx.fizzled()) {
			fizzle(engine, r, bodyFrom, k);
			return;
		}
		Vec3 bodyTo = fx.to().add(0, 0.9, 0);
		depart(engine, r, bodyFrom, k);
		path(engine, r, bodyFrom, bodyTo, k);
		arrive(engine, r, fx.to(), bodyTo, k);
	}

	static float budget(ParticleStatus status) {
		return switch (status) {
			case ALL -> 1.0f;
			case DECREASED -> 0.5f;
			case MINIMAL -> 0.2f;
		};
	}

	private static int n(int full, float k) {
		return Math.max(1, Math.round(full * k));
	}

	private static StarfallParticle spawn(ParticleEngine engine, SimpleParticleType type, Vec3 at) {
		Particle p = engine.createParticle(type, at.x, at.y, at.z, 0, 0, 0);
		return p instanceof StarfallParticle s ? s : null;
	}

	/** Beat 1: the body folds in on itself. Departure runs cooler (starts at pale gold) than the arrival. */
	private static void depart(ParticleEngine e, RandomSource r, Vec3 body, float k) {
		StarfallParticle flash = spawn(e, ModParticles.STAR_FLASH, body);
		if (flash != null) flash.size(0.6f);
		int count = n(32, k);
		for (int i = 0; i < count; i++) {
			// a point on the 0.8 x 1.4 body box, moving toward the centre: the cloud collapses
			Vec3 off = new Vec3((r.nextDouble() - 0.5) * 0.8, (r.nextDouble() - 0.5) * 1.4, (r.nextDouble() - 0.5) * 0.8);
			StarfallParticle s = spawn(e, ModParticles.STAR_SPARK, body.add(off));
			if (s == null) continue;
			int life = 5 + r.nextInt(4);
			Vec3 v = off.scale(-1.0 / life * 1.15);
			s.motion(v.x, v.y, v.z).life(life).drag(1.0f).heat(0.3f).size(0.08f + r.nextFloat() * 0.05f);
		}
		int motes = n(8, k);
		for (int i = 0; i < motes; i++) {
			// second type, mirrored velocity: drifts outward while the sparks rush in
			Vec3 dir = new Vec3(r.nextGaussian(), r.nextGaussian() * 0.5, r.nextGaussian()).normalize();
			StarfallParticle m = spawn(e, ModParticles.STAR_MOTE, body.add(dir.scale(0.2)));
			if (m != null) m.motion(dir.x * 0.03, dir.y * 0.03 + 0.01, dir.z * 0.03);
		}
	}

	/** Beat 2: the line you travelled along, sampled every half block (never just the end points). */
	private static void path(ParticleEngine e, RandomSource r, Vec3 a, Vec3 b, float k) {
		double length = a.distanceTo(b);
		int count = n(Math.min(16, Mth.ceil(length * 2)), k);
		for (int i = 0; i < count; i++) {
			double t = (i + r.nextDouble()) / count;
			Vec3 at = a.lerp(b, t).add(r.nextGaussian() * 0.06, r.nextGaussian() * 0.06, r.nextGaussian() * 0.06);
			StarfallParticle s = spawn(e, ModParticles.STAR_SPARK, at);
			if (s == null) continue;
			s.motion(r.nextGaussian() * 0.01, 0.005, r.nextGaussian() * 0.01)
					.life(4 + (int) (t * 10) + r.nextInt(3)).drag(0.9f).heat(0.15f).size(0.06f + 0.04f * (float) t);
		}
	}

	/** Beats 3-5: flash, ground ring, two-speed burst, bouncing embers, then a quiet linger. */
	private static void arrive(ParticleEngine e, RandomSource r, Vec3 feet, Vec3 body, float k) {
		spawn(e, ModParticles.STAR_FLASH, body);
		spawn(e, ModParticles.BLINK_RING, feet.add(0, 0.04, 0));
		int fast = n(20, k);
		for (int i = 0; i < fast; i++) {
			Vec3 dir = new Vec3(r.nextGaussian(), r.nextGaussian() * 0.45, r.nextGaussian()).normalize();
			double speed = 0.28 + r.nextDouble() * 0.14;
			StarfallParticle s = spawn(e, ModParticles.STAR_SPARK, body.add(dir.scale(0.15)));
			if (s != null) s.motion(dir.x * speed, dir.y * speed, dir.z * speed).drag(0.8f).life(8 + r.nextInt(5))
					.size(0.10f + r.nextFloat() * 0.04f);
		}
		int slow = n(12, k);
		for (int i = 0; i < slow; i++) {
			Vec3 dir = new Vec3(r.nextGaussian(), r.nextGaussian() * 0.6, r.nextGaussian()).normalize();
			double speed = 0.06 + r.nextDouble() * 0.06;
			StarfallParticle s = spawn(e, ModParticles.STAR_SPARK, body.add(dir.scale(0.3)));
			if (s != null) s.motion(dir.x * speed, dir.y * speed, dir.z * speed).drag(0.9f).life(14 + r.nextInt(9))
					.size(0.12f + r.nextFloat() * 0.05f);
		}
		int embers = n(10, k);
		for (int i = 0; i < embers; i++) {
			double angle = r.nextDouble() * Math.PI * 2;
			double out = 0.06 + r.nextDouble() * 0.1;
			StarfallParticle s = spawn(e, ModParticles.STAR_EMBER, body);
			if (s != null) s.motion(Math.cos(angle) * out, 0.2 + r.nextDouble() * 0.15, Math.sin(angle) * out);
		}
		int motes = n(6, k);
		for (int i = 0; i < motes; i++) {
			double angle = r.nextDouble() * Math.PI * 2;
			Vec3 at = feet.add(Math.cos(angle) * 0.7, 0.1 + r.nextDouble() * 0.3, Math.sin(angle) * 0.7);
			StarfallParticle m = spawn(e, ModParticles.STAR_MOTE, at);
			if (m != null) m.motion(0, 0.015 + r.nextDouble() * 0.01, 0);
		}
	}

	/** No room to land: a dim violet sputter at the wand, so the failure is readable but clearly not a blink. */
	private static void fizzle(ParticleEngine e, RandomSource r, Vec3 body, float k) {
		int count = n(16, k);
		for (int i = 0; i < count; i++) {
			Vec3 at = body.add(r.nextGaussian() * 0.25, 0.3 + r.nextGaussian() * 0.15, r.nextGaussian() * 0.2);
			StarfallParticle s = spawn(e, ModParticles.STAR_EMBER, at);
			if (s != null) s.motion(r.nextGaussian() * 0.04, 0.12 + r.nextDouble() * 0.1, r.nextGaussian() * 0.04).heat(0.55f).size(0.08f);
		}
		int puffs = n(8, k);
		for (int i = 0; i < puffs; i++) {
			StarfallParticle m = spawn(e, ModParticles.STAR_MOTE, body.add(r.nextGaussian() * 0.25, 0.2, r.nextGaussian() * 0.25));
			if (m != null) m.heat(0.8f).life(12 + r.nextInt(8));
		}
	}
}

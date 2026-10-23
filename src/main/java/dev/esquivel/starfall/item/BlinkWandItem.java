package dev.esquivel.starfall.item;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/**
 * The Blink Wand: right-click to teleport up to {@link #RANGE} blocks along your
 * line of sight. Stops just short of walls, resets fall damage, costs 1 durability
 * and has a short cooldown.
 */
public class BlinkWandItem extends Item {
	public static final double RANGE = 8.0;
	public static final int COOLDOWN_TICKS = 30;

	public BlinkWandItem(Properties properties) {
		super(properties);
	}

	@Override
	public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
		ItemStack stack = player.getItemInHand(hand);

		if (!level.isClientSide()) {
			Vec3 eye = player.getEyePosition();
			Vec3 look = player.getLookAngle();
			Vec3 end = eye.add(look.scale(RANGE));

			BlockHitResult hit = level.clip(new ClipContext(
					eye, end, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, player));

			// Back off half a block from whatever we hit so we don't land inside it.
			Vec3 targetEye = hit.getType() == HitResult.Type.MISS
					? end
					: hit.getLocation().subtract(look.scale(0.5));
			Vec3 targetFeet = targetEye.subtract(0, player.getEyeHeight(), 0);

			if (targetFeet.distanceToSqr(player.position()) < 1.0) {
				return InteractionResultHolder.fail(stack);
			}

			ServerLevel server = (ServerLevel) level;
			Vec3 from = player.position();
			server.sendParticles(ParticleTypes.PORTAL, from.x, from.y + 1, from.z, 40, 0.3, 0.6, 0.3, 0.2);

			player.teleportTo(targetFeet.x, targetFeet.y, targetFeet.z);
			player.resetFallDistance();

			server.sendParticles(ParticleTypes.END_ROD, targetFeet.x, targetFeet.y + 1, targetFeet.z, 20, 0.3, 0.6, 0.3, 0.05);
			level.playSound(null, targetFeet.x, targetFeet.y, targetFeet.z,
					SoundEvents.ENDERMAN_TELEPORT, SoundSource.PLAYERS, 0.8f, 1.4f);

			stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
		}

		player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
		return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
	}
}

package dev.esquivel.starfall.item;

import dev.esquivel.starfall.ModSounds;
import dev.esquivel.starfall.network.BlinkFxPayload;
import java.util.List;
import net.fabricmc.fabric.api.networking.v1.PlayerLookup;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/**
 * The Blink Wand: right-click to blink up to {@link #RANGE} blocks along your line of sight.
 *
 * <p>Landing is collision-checked: the wand walks back along the ray and, if needed, lifts you up to
 * {@link #MAX_LIFT} blocks so you land standing on a floor or ledge instead of inside it. If there is no
 * room it fizzles: no teleport, no durability cost, a shorter cooldown. The visuals are one
 * {@link BlinkFxPayload} that nearby clients expand into the full effect.
 */
public class BlinkWandItem extends Item {
	public static final double RANGE = 8.0;
	public static final int COOLDOWN_TICKS = 30;
	public static final int FIZZLE_COOLDOWN_TICKS = 10;
	static final double MIN_TRAVEL = 1.5;
	static final double MAX_LIFT = 2.0;
	static final double STEP = 0.25;
	static final double FX_RADIUS = 64.0;

	public BlinkWandItem(Properties properties) {
		super(properties);
	}

	@Override
	public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
		ItemStack stack = player.getItemInHand(hand);
		if (level.isClientSide()) {
			// The server decides where you land and syncs the cooldown; the client just swings the arm.
			return InteractionResultHolder.success(stack);
		}
		ServerLevel server = (ServerLevel) level;
		Vec3 from = player.position();
		Vec3 target = findLanding(server, player);

		if (target == null) {
			play(server, from, ModSounds.BLINK_FIZZLE, 0.6f, player);
			sendFx(server, new BlinkFxPayload(from, from, true));
			player.getCooldowns().addCooldown(this, FIZZLE_COOLDOWN_TICKS);
			return InteractionResultHolder.fail(stack);
		}

		play(server, from, ModSounds.BLINK_DEPART, 0.7f, player);
		player.teleportTo(target.x, target.y, target.z);
		player.resetFallDistance();
		player.setDeltaMovement(player.getDeltaMovement().multiply(1, 0, 1));
		play(server, target, ModSounds.BLINK_ARRIVE, 1.0f, player);
		sendFx(server, new BlinkFxPayload(from, target, false));

		stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
		player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
		return InteractionResultHolder.success(stack);
	}

	/** Returns safe feet coordinates at least {@link #MIN_TRAVEL} away, or null when there is no room. */
	static Vec3 findLanding(ServerLevel level, Player player) {
		Vec3 eye = player.getEyePosition();
		Vec3 look = player.getLookAngle();
		BlockHitResult hit = level.clip(new ClipContext(
				eye, eye.add(look.scale(RANGE)), ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, player));
		double reach = hit.getType() == HitResult.Type.MISS ? RANGE : hit.getLocation().distanceTo(eye) - 0.3;
		double eyeHeight = player.getEyeHeight();

		for (double d = reach; d >= MIN_TRAVEL; d -= STEP) {
			Vec3 feet = eye.add(look.scale(d)).subtract(0, eyeHeight, 0);
			for (double lift = 0; lift <= MAX_LIFT; lift += STEP) {
				Vec3 candidate = feet.add(0, lift, 0);
				if (candidate.distanceTo(player.position()) < MIN_TRAVEL) continue;
				AABB box = player.getDimensions(player.getPose()).makeBoundingBox(candidate);
				if (level.noCollision(player, box) && level.getWorldBorder().isWithinBounds(box)) {
					return candidate;
				}
			}
		}
		return null;
	}

	private static void play(ServerLevel level, Vec3 at, SoundEvent sound, float volume, Player player) {
		// Pitch varies 0.9-1.1 so repeated blinks never sound like a loop.
		float pitch = 0.9f + player.getRandom().nextFloat() * 0.2f;
		level.playSound(null, at.x, at.y, at.z, sound, SoundSource.PLAYERS, volume, pitch);
	}

	private static void sendFx(ServerLevel level, BlinkFxPayload payload) {
		Vec3 mid = payload.from().add(payload.to()).scale(0.5);
		for (ServerPlayer viewer : PlayerLookup.around(level, mid, FX_RADIUS)) {
			ServerPlayNetworking.send(viewer, payload);
		}
	}

	@Override
	public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
		tooltip.add(Component.translatable("item.starfall.blink_wand.tooltip.0", (int) RANGE)
				.withStyle(ChatFormatting.GRAY));
		tooltip.add(Component.translatable("item.starfall.blink_wand.tooltip.1",
				String.format(java.util.Locale.ROOT, "%.1f", COOLDOWN_TICKS / 20.0)).withStyle(ChatFormatting.GRAY));
		tooltip.add(Component.translatable("item.starfall.blink_wand.tooltip.2")
				.withStyle(ChatFormatting.DARK_PURPLE, ChatFormatting.ITALIC));
	}
}

package dev.esquivel.starfall.network;

import dev.esquivel.starfall.Starfall;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.world.phys.Vec3;

/**
 * One packet per blink: where the caster left from and where they landed (feet positions).
 * The client builds every particle locally, so the server never streams particles.
 */
public record BlinkFxPayload(Vec3 from, Vec3 to, boolean fizzled) implements CustomPacketPayload {
	public static final Type<BlinkFxPayload> TYPE = new Type<>(Starfall.id("blink_fx"));
	public static final StreamCodec<RegistryFriendlyByteBuf, BlinkFxPayload> CODEC =
			CustomPacketPayload.codec(BlinkFxPayload::write, BlinkFxPayload::read);

	private static BlinkFxPayload read(RegistryFriendlyByteBuf buf) {
		Vec3 from = new Vec3(buf.readDouble(), buf.readDouble(), buf.readDouble());
		Vec3 to = new Vec3(buf.readDouble(), buf.readDouble(), buf.readDouble());
		return new BlinkFxPayload(from, to, buf.readBoolean());
	}

	private void write(RegistryFriendlyByteBuf buf) {
		buf.writeDouble(from.x); buf.writeDouble(from.y); buf.writeDouble(from.z);
		buf.writeDouble(to.x); buf.writeDouble(to.y); buf.writeDouble(to.z);
		buf.writeBoolean(fizzled);
	}

	@Override
	public Type<? extends CustomPacketPayload> type() {
		return TYPE;
	}
}

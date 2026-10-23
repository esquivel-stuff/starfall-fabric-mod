package dev.esquivel.starfall.client;

import dev.esquivel.starfall.ModItems;
import dev.esquivel.starfall.Starfall;
import dev.esquivel.starfall.client.particle.StarfallParticleProviders;
import dev.esquivel.starfall.network.BlinkFxPayload;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.fabricmc.fabric.api.object.builder.v1.client.model.FabricModelPredicateProviderRegistry;
import net.minecraft.world.entity.player.Player;

/** Client entrypoint: particles, the blink FX packet, and the wand's cooldown model. */
public class StarfallClient implements ClientModInitializer {
	@Override
	public void onInitializeClient() {
		StarfallParticleProviders.register();
		ClientPlayNetworking.registerGlobalReceiver(BlinkFxPayload.TYPE,
				(payload, context) -> context.client().execute(() -> BlinkFx.play(payload)));
		// "starfall:cooldown" > 0 while the wand recharges: its model swaps to the dimmed violet star.
		FabricModelPredicateProviderRegistry.register(ModItems.BLINK_WAND, Starfall.id("cooldown"),
				(stack, level, entity, seed) -> entity instanceof Player player
						? player.getCooldowns().getCooldownPercent(stack.getItem(), 0f) : 0f);
	}
}

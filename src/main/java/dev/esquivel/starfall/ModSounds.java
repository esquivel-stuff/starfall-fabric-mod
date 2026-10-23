package dev.esquivel.starfall;

import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvent;

/** Sound events are named by what happens, each with subtitles and variants in sounds.json. */
public final class ModSounds {
	static final int COUNT = 3;

	/** The air you leave behind folds shut. */
	public static final SoundEvent BLINK_DEPART = register("item.blink_wand.depart");
	/** Starlight lands: a bright chime over a soft thump. */
	public static final SoundEvent BLINK_ARRIVE = register("item.blink_wand.arrive");
	/** No room to land: the wand sputters and you stay put. */
	public static final SoundEvent BLINK_FIZZLE = register("item.blink_wand.fizzle");

	private ModSounds() {}

	private static SoundEvent register(String name) {
		ResourceLocation id = Starfall.id(name);
		return Registry.register(BuiltInRegistries.SOUND_EVENT, id, SoundEvent.createVariableRangeEvent(id));
	}

	static void register() {
		// Forces static initialisation.
	}
}

package dev.esquivel.starfall.item;

import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

/** An item whose tooltip reads its lines from the lang file: {@code <key>.tooltip.0}, {@code .1}, ... */
public class LoreItem extends Item {
	private final int lines;

	public LoreItem(Properties properties, int lines) {
		super(properties);
		this.lines = lines;
	}

	@Override
	public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
		addLore(getDescriptionId(), lines, tooltip);
	}

	/** Line 0 is the gameplay fact (gray), the last line is flavour (violet, italic). */
	public static void addLore(String key, int lines, List<Component> tooltip) {
		for (int i = 0; i < lines; i++) {
			boolean flavour = i == lines - 1;
			tooltip.add(Component.translatable(key + ".tooltip." + i)
					.withStyle(flavour ? new ChatFormatting[] {ChatFormatting.DARK_PURPLE, ChatFormatting.ITALIC}
							: new ChatFormatting[] {ChatFormatting.GRAY}));
		}
	}
}

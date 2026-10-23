package dev.esquivel.starfall.item;

import java.util.List;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.block.Block;

/** BlockItem with lang-driven tooltip lines, see {@link LoreItem}. */
public class LoreBlockItem extends BlockItem {
	private final int lines;

	public LoreBlockItem(Block block, Properties properties, int lines) {
		super(block, properties);
		this.lines = lines;
	}

	@Override
	public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
		LoreItem.addLore(getDescriptionId(), lines, tooltip);
	}
}

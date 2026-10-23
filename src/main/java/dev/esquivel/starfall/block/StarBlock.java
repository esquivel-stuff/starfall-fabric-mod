package dev.esquivel.starfall.block;

import dev.esquivel.starfall.ModParticles;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;

/**
 * Nine Star Shards packed into a block. Light 15, rendered full-bright (emissive, the same flag vanilla magma uses),
 * with an animated twinkle texture and, now and then, a mote of starlight drifting off an open face.
 */
public class StarBlock extends Block {
	public StarBlock(Properties properties) {
		super(properties);
	}

	@Override
	public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
		if (random.nextInt(5) != 0) return; // about one mote every 5 ticks per block: a shimmer, not a fountain
		Direction face = Direction.getRandom(random);
		BlockPos side = pos.relative(face);
		if (level.getBlockState(side).isSolidRender(level, side)) return;
		double x = pos.getX() + 0.5 + face.getStepX() * 0.52 + (face.getStepX() == 0 ? random.nextDouble() - 0.5 : 0);
		double y = pos.getY() + 0.5 + face.getStepY() * 0.52 + (face.getStepY() == 0 ? random.nextDouble() - 0.5 : 0);
		double z = pos.getZ() + 0.5 + face.getStepZ() * 0.52 + (face.getStepZ() == 0 ? random.nextDouble() - 0.5 : 0);
		level.addParticle(ModParticles.STAR_MOTE, x, y, z, face.getStepX() * 0.01, 0.012, face.getStepZ() * 0.01);
	}
}

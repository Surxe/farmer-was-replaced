def is_checkered_pos(x, y):
	return x % 2 == 0 and y % 2 != 0
		
def cycle_wood_grid():
	for j in range(get_world_size()):
		for i in range(get_world_size()):
			if can_harvest():
				harvest()
			if is_checkered_pos(get_pos_x(), get_pos_y()):
				plant(Entities.Tree)
			move(East)
		move(North)
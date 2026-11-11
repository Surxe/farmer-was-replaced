from reset import move_to_origin

def is_checkered_pos(x, y):
	return (x % 2 == 0 and y % 2 == 1) or (x % 2 == 1 and y % 2 == 0)

def cycle_wood_grid():
	for j in range(get_world_size()):
		for i in range(get_world_size()):
			if can_harvest():
				harvest()
			if is_checkered_pos(get_pos_x(), get_pos_y()):
				plant(Entities.Tree)
			move(East)
		move(North)

if __name__ == '__main__':
	move_to_origin()
	cycle_wood_grid()

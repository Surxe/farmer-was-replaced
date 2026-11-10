def move_to_origin():
	# not shortest path yet
	if get_pos_x() > 0:
		move(West)
		move_to_origin()
	if get_pos_y() > 0:
		move(South)
		move_to_origin()
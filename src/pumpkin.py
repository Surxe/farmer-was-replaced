from till import *
from water import *
from utils import two_d_arr, one_d_arr, num_of_n_in_list
from reset import move_to_origin

def do_move(col_then_row):
	if col_then_row:
		move(East)
	else:
		move(North)

# Record the drone's current cell as `state` ('planted' or 'grown') and keep the
# per-row / per-col planted counts in sync. Only real transitions touch the counts,
# so re-marking a cell with the state it already has is a no-op.
# returns the change to the total planted count (-1, 0 or 1)
def set_cell_state(registry, planted_in_row, planted_in_col, state):
	x = get_pos_x()
	y = get_pos_y()
	prev = registry[x][y]
	if prev == state:
		return 0
	registry[x][y] = state
	delta = 0
	if state == 'planted':
		delta = 1
	elif prev == 'planted':
		delta = -1
	planted_in_row[y] += delta
	planted_in_col[x] += delta
	return delta

def cycle_pump_grid():
	pump_registry = two_d_arr()
	planted_in_row = one_d_arr(0) # indexed by y
	planted_in_col = one_d_arr(0) # indexed by x
	total_planted = 0
	iter = 1 # once its past the 1st iteration, pump registry is all planted
	# on iter=2, pump registry is some combination of planted and fully grown, as it will have replaced the planted->dead->back to planted
	# only after iter=2 will the # of dead spots be narrowed down to less than the full board. any spot thats not grown is treated as a possible
	# dead spot that it has to check
	# we dont need to check grown cells. This leads us to the pathing algorithm
	col_then_row = True
	while True:
		if iter>1:
			if total_planted == 0:
				# every cell is grown, so the grid is one merged pumpkin.
				# a full pass wraps back to the origin, which is part of it
				harvest()
				move_to_origin()
				return

			# snake cols->rows (East then North) and skip rows if theres more skippable rows than cols
			# else, snake rows->cols (North then East) and skip cols
			col_then_row = num_of_n_in_list(planted_in_row, 0) > num_of_n_in_list(planted_in_col, 0)

		for i in range(get_world_size()):
			if iter>1:
				# outer i is y when sweeping East, x when sweeping North
				if col_then_row:
					line_planted = planted_in_row[i]
				else:
					line_planted = planted_in_col[i]
				if line_planted == 0:
					do_move(not col_then_row)
					continue
			for j in range(get_world_size()):
				if can_harvest():
					if get_entity_type() != Entities.Pumpkin:
						# clear leftover crops so a pumpkin can go here
						harvest()
						do_till()
						plant(Entities.Pumpkin)
						total_planted += set_cell_state(pump_registry, planted_in_row, planted_in_col, 'planted')
					else:
						# this pump is ready to harvest but the whole grid isnt ready yet
						# mark it as fully grown
						total_planted += set_cell_state(pump_registry, planted_in_row, planted_in_col, 'grown')
				else:
					total_planted += set_cell_state(pump_registry, planted_in_row, planted_in_col, 'planted')
					do_till()
					water()
					plant(Entities.Pumpkin)

				do_move(col_then_row)
			do_move(not col_then_row)
		iter += 1

# pumpkins will be forced in the bottom left half of the grid,
# regardless of load balancing
# they will always be in a square of NxN size
# instead- load balancing will determine the size of N
def in_final_pump_spot(pump_size=None):
	if pump_size == None:
		pump_size = get_world_size()
	return get_pos_x() == pump_size-1 and get_pos_y() == pump_size-1
	# this is the last position thats checked for a pump.

if __name__ == "__main__":
	clear()
	cycle_pump_grid()

from till import *
from water import *
from utils import two_d_arr, one_d_arr

def get_skippable(r, dir):
	if dir not in [-1, 1]:
		return []
	skippables = one_d_arr(1)
	for i in range(len(r)):
		for j in range(len(r)):
			if (r[i][j] == 'planted' and dir == 1) or (r[j][i] == 'planted' and dir == -1):
				if dir == 1:
					v = i
				elif dir == -1:
					v = j
				skippables[v] = 0
	return skippables

def cycle_pump_grid():
	pump_registry = two_d_arr()
	iter = 1 # once its past the 1st iteration, pump registry is all planted
	# on iter=2, pump registry is some combination of planted and fully grown, as it will have replaced the planted->dead->back to planted
	# only after iter=2 will the # of dead spots be narrowed down to less than the full board. any spot thats not grown is treated as a possible
	# dead spot that it has to check
	# we dont need to check grown cells. This leads us to the pathing algorithm
	col_then_row = True
	skippable_rows = None
	skippable_cols = None
	while True:
		if iter>1:
			# compute if any rows are skippable or if any cols are skippable
			skippable_cols = get_skippable(pump_registry, -1)
			skippable_rows = get_skippable(pump_registry, 1)

			# snake cols->rows (East then North) and skip rows if theres more skippable rows than cols
			# else, snake rows->cols (North then East) and skip cols
			#if len(skippable_rows) > len(skippable_cols):
			col_then_row = len(skippable_rows) > len(skippable_cols)
			print(col_then_row)
			do_a_flip()
			print(skippable_rows)
			do_a_flip()
			print(skippable_cols)

		for i in range(get_world_size()):
			if iter>1 and not col_then_row and skippable_cols[i]:
				continue
			for j in range(get_world_size()):
				if iter>1 and col_then_row and skippable_rows[j]:
					continue
				if can_harvest():
					if get_entity_type() != Entities.Pumpkin:
						# clear leftover crops so a pumpkin can go here
						harvest()
						do_till()
						plant(Entities.Pumpkin)
						pump_registry[get_pos_x()][get_pos_y()] = 'planted'
					elif in_final_pump_spot():
						# last cell is ripe: harvest the merged pumpkin,
						# step back to the origin (wraps), and hand control back
						harvest()
						move(East)
						move(North)
						return
					else:
						# this pump is ready to harvest but the whole grid isnt ready yet
						# mark it as fully grown
						pump_registry[get_pos_x()][get_pos_y()] = 'grown'
				else:
					pump_registry[get_pos_x()][get_pos_y()] = 'planted'
					plant(Entities.Pumpkin)
				do_till()
				water()

				if col_then_row:
					move(East)
				else:
					move(North)
			if col_then_row:
				move(North)
			else:
				move(East)
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

from till import *
from water import *
from utils import two_d_arr

def cycle_pump_grid():
	pump_registry = two_d_arr()
	iter = 1 # once its past the 1st iteration, pump registry is all planted
	# on iter=2, pump registry is some combination of planted and fully grown, as it will have replaced the planted->dead->back to planted
	# only after iter=2 will the # of dead spots be narrowed down to less than the full board. any spot thats not grown is treated as a possible
	# dead spot that it has to check
	# we dont need to check grown cells. This leads us to the pathing algorithm
	while True:
		for _ in range(get_world_size()):
			for _ in range(get_world_size()):
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
				move(East)
			move(North)
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
	cycle_pump_grid()

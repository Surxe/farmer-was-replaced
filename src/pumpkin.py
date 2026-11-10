from till import *
from water import *

def cycle_pump_grid():
    while True:
		for j in range(get_world_size()):
			for i in range(get_world_size()):
				if can_harvest():
					if in_final_pump_spot() or get_entity_type() != Entities.Pumpkin:
						if get_entity_type() == Entities.Pumpkin:
							harvest()
							move(East)
							move(North)
							return
						harvest()
				do_till()
				water()
				plant(Entities.Pumpkin)
				move(East)
			move(North)

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
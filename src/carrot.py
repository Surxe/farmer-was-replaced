from water import *
from till import *

def cycle_carrot_grid():
	for j in range(get_world_size()):
		for i in range(get_world_size()):
			if can_harvest():
				harvest()
			do_till()
			water()
			plant(Entities.Carrot)
			move(East)
		move(North)
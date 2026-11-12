from water import *
from till import *
from utils import two_d_arr
from reset import move_to_origin



def cycle_poly_grid(default_entity=Entities.Carrot):
	preference_registry = two_d_arr()

	def register_pref():
		comp = get_companion()
		print(comp)
		comp_entity = comp[0]
		comp_location = comp[1]
		preference_registry[comp_location[0]][comp_location[1]] = comp_entity

	for j in range(get_world_size()):
		for i in range(get_world_size()):
			if can_harvest():
				harvest()
			do_till()
			water()
			preferred_entity = preference_registry[i][j]
			if preferred_entity == None: # if theres no preferred plant at this spot
				plant(default_entity)
				register_pref()
			else:
				plant(preferred_entity)
				register_pref()
			move(East)
		move(North)

if __name__ == '__main__':
	clear()
	move_to_origin()
	cycle_poly_grid()

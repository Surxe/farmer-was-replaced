from water import *
from till import *
from utils import two_d_arr
from reset import move_to_origin
from constants import item_to_entity, poly_culture_supported_entities
from sunflower import *

power_needed_for_cycle = 80

def item_is_supported_by_poly_culture(item):
	if item not in item_to_entity:
		return None, False
	entity = item_to_entity[item]
	is_supported = poly_culture_supported_entities[entity]
	return entity, is_supported

def cycle_poly_grid(default_entity=Entities.Carrot):
	preference_registry = two_d_arr()

	def register_pref():
		comp = get_companion()
		comp_entity = comp[0]
		comp_location = comp[1]
		preference_registry[comp_location[0]][comp_location[1]] = comp_entity

	global power_needed_for_cycle
	print(power_needed_for_cycle)
	cycle_sunflower(power_needed_for_cycle)

	starting_power = num_items(Items.Power)
	for j in range(get_world_size()):
		for i in range(get_world_size()):
			if is_sunflower_designated_tile():
				process_sunflower_tile()
			else:
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
	power_cycle_cost = starting_power - num_items(Items.Power)
	power_needed_for_cycle = power_cycle_cost * 1.15 # padding

if __name__ == '__main__':
	clear()
	do_a_flip()
	move_to_origin()
	while True:
		cycle_poly_grid()

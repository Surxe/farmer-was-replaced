from water import *
from reset import move_to_origin
from load_balancing import get_item_needed_most
from pumpkin import cycle_pump_grid
from poly_culture import *
from sunflower import init_registries

percent_grid_tilled = 0
num_carrots_more_than_wood = num_items(Items.Carrot) - num_items(Items.Wood)
num_pumps_more_than_carrots = num_items(Items.Pumpkin) - num_items(Items.Carrot)
water_thresh = 0.5
item_to_grid_cycler = {
	Items.Pumpkin: cycle_pump_grid,
}
# entity_to_item = {
# 	Entities.Grass: Items.Hay,
# 	Entities.Tree: Items.Wood,
# 	Entities.Carrot: Items.Carrot,
# }

#clear()
change_hat(Hats.Sunflower_Hat)
move_to_origin()
do_a_flip()
while(True):
	cycle_had_dead_pumps = False
	item_needed_most = get_item_needed_most()

	# If the item thats needed most is supported by poly culture
	# then perform a poly_culture cycle, with the item's entity thats needed most as the default entity
	entity_needed_most, is_supported = item_is_supported_by_poly_culture(item_needed_most)
	if is_supported:
		cycle_poly_grid(entity_needed_most)
	else:
		init_registries() #reset sunflower reg
		# If the item thats needed most is not supported by poly culture,
		# call its dedicated cycle function
		item_grid_cycler = item_to_grid_cycler[get_item_needed_most()]
		item_grid_cycler()

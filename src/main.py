from water import *
from plant import *
from harvest import *
from reset import move_to_origin
from load_balancing import get_item_needed_most
from hay import cycle_hay_grid
from wood import cycle_wood_grid
from carrot import cycle_carrot_grid
from pumpkin import cycle_pump_grid

percent_grid_tilled = 0
num_carrots_more_than_wood = num_items(Items.Carrot) - num_items(Items.Wood)
num_pumps_more_than_carrots = num_items(Items.Pumpkin) - num_items(Items.Carrot)
water_thresh = 0.5

item_to_grid_cycler = {
	Items.Hay: cycle_hay_grid,
	Items.Carrot: cycle_carrot_grid,
	Items.Wood: cycle_wood_grid,
	Items.Pumpkin: cycle_pump_grid,
}

#clear()
move_to_origin()
do_a_flip()
while(True):	
	cycle_had_dead_pumps = False
	item_needed_most = get_item_needed_most()
	item_grid_cycler = item_to_grid_cycler[get_item_needed_most()]
	item_grid_cycler()

	for j in range(get_world_size()):
		for i in range(get_world_size()):
			
					
			move(East)
		move(North)
	
	
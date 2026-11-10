from water import *
from plant import *

percent_grid_tilled = 0
starting_water = num_items(Items.Water)
num_carrots_more_than_wood = num_items(Items.Carrot) - num_items(Items.Wood)
clear()
do_a_flip()
while(True):	
	for j in range(get_world_size()):
		for i in range(get_world_size()):
			if can_harvest():
				harvest()
				
			plant_least(percent_grid_tilled, num_carrots_more_than_wood)
					
			move(East)
		move(North)
	
	
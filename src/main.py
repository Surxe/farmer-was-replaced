from water import *
from plant import *
from harvest import *
from reset import move_to_origin

percent_grid_tilled = 0
num_carrots_more_than_wood = num_items(Items.Carrot) - num_items(Items.Wood)
num_pumps_more_than_carrots = num_items(Items.Pumpkin) - num_items(Items.Carrot)
water_thresh = 0.5

#clear()
move_to_origin()
do_a_flip()
while(True):	
	#print(water_thresh)
	cycle_had_dead_pumps = False
	for j in range(get_world_size()):
		for i in range(get_world_size()):
			had_dead_pump = do_harvest(cycle_had_dead_pumps)
			if not cycle_had_dead_pumps and had_dead_pump:
				cycle_had_dead_pumps = True
				
			water_thresh = do_plant(num_carrots_more_than_wood, water_thresh)
					
			move(East)
		move(North)
	
	
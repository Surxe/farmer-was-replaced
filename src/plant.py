from water import *
from pumpkin import *
from load_balancing import *
from till import *

def plant_carrot(water_thresh):
	do_till()
	plant(Entities.Carrot)
	return water(water_thresh)

def do_plant(num_carrots_more_than_wood, water_thresh):
	# Plant what you have the least of
	water_thresh = plant_pumpkin(water_thresh)
		
	if get_item_least_supply() == Items.Carrot:
		water_thresh = plant_carrot(water_thresh)
	elif get_item_least_supply() == Items.Hay:
		plant(Entities.Grass)
	elif get_item_least_supply() == Items.Wood:
		# low on wood, prioritize trees
		if get_pos_x()%2==0 and get_pos_y()%2==0:
			plant(Entities.Tree)
		# if trees are nearby, instead plant the next most needed item
		else:
			# if its not a tree spot, but we now have even less wood 
			# than carrots than the last cycle, plant a bush
			if num_items(Items.Carrot) - num_items(Items.Wood) > num_carrots_more_than_wood and num_carrots_more_than_wood>0:
				plant(Entities.Bush)
			# we're at least gaining on carrots, so we can plant carrots
			# since the diff is only computed per cycle, this may just make the wood/cycle diff alternate each cycle
			# but at least theyll stay near in supply
			elif num_items(Items.Carrot) < num_items(Items.Hay):
				water_thresh = plant_carrot(water_thresh)
			else:
				plant(Entities.Grass)

	return water_thresh
			
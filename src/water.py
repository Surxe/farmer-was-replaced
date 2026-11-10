STARTING_WATER = num_items(Items.Water)

# Only spend water if we're not at a not loss
def profitted_water_this_run():
	return num_items(Items.Water) - STARTING_WATER
	

def water(water_thresh):
	# assumes were on tilled land already
	# only till if we profitted water this cycle
	# and if the current cell has < 35% water
	# returns whether or not it planted water
	if profitted_water_this_run() > 0:
		water_thresh += (1-water_thresh) * .1 # and accelerate
		if get_water() < water_thresh:
			use_item(Items.Water)
			return water_thresh
	else:
		# deccelerate
		water_thresh *= .93
		
	return water_thresh
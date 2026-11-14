STARTING_WATER = num_items(Items.Water)
REFILL_WATER_IF_BELOW_THRESH = .75
WATER_THRESH_CHANGE_PER_UPDATE = .01

# Only spend water if we're not at a net loss
def profitted_water_this_run():
	return num_items(Items.Water) - STARTING_WATER

def water(actually_water=False):
	if not actually_water:
		return
	# assumes were on tilled land already
	# only till if we profitted water this cycle
	# and if the current cell has < 35% water
	# returns whether or not it planted water
	if profitted_water_this_run() > 0:
		while get_water() < REFILL_WATER_IF_BELOW_THRESH:
			use_item(Items.Water)
	return REFILL_WATER_IF_BELOW_THRESH

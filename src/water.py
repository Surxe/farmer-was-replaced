STARTING_WATER = num_items(Items.Water)
REFILL_WATER_IF_BELOW_THRESH = .6
WATER_THRESH_CHANGE_PER_UPDATE = .01

# Only spend water if we're not at a not loss
def profitted_water_this_run():
	return num_items(Items.Water) - STARTING_WATER

def update_water_thresh(magnitude):
	if magnitude not in [-1, 1]:
		return None

	global REFILL_WATER_IF_BELOW_THRESH
	REFILL_WATER_IF_BELOW_THRESH = max(0, min(1, REFILL_WATER_IF_BELOW_THRESH + WATER_THRESH_CHANGE_PER_UPDATE * magnitude))

def water():
	# assumes were on tilled land already
	# only till if we profitted water this cycle
	# and if the current cell has < 35% water
	# returns whether or not it planted water
	if profitted_water_this_run() > 0:
		if get_water() < REFILL_WATER_IF_BELOW_THRESH:
			update_water_thresh(1)
			use_item(Items.Water)
		else:
			# dont use water, but do decrease the thresh
			update_water_thresh(-1)
	return REFILL_WATER_IF_BELOW_THRESH

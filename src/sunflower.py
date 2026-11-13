from utils import two_d_arr
from water import *
from till import do_till
from reset import move_to_origin

sunflower_registry = two_d_arr()
petal_registry = {} # {num_petals: num_sunflowers with that # of petals}
peak_petal_count = 0

# Poly culture farming is also capable of spending 10 slots on sunflowers
def is_sunflower_designated_tile(x=None, y=None, n=10):
	if x == None:
		x = get_pos_x()
	if y == None:
		y = get_pos_y()
	# n is the number of tiles remaining that are available to be designated as sunflower tiles
	# the first n slots in reading order (left to right, top row down) are designated.
	# y=0 is the bottom row, so the top row is y=size-1.
	size = get_world_size()
	index = (size - 1 - y) * size + x
	return index < n

def get_peak_petal_count():
	# Returns the number of petals on the sunflower that has the most petals
	# Filters the petal_registry to those that have num_sunflowers > 0
	most_petals = -100000
	for num_petals in petal_registry:
		num_sunflowers = petal_registry[num_petals]
		if num_sunflowers > 0:
			most_petals = max(most_petals, num_petals)
	return most_petals

def register_petals(num_petals, magnitude):
	if magnitude not in [-1, 1]:
		print('magnitude must be -1 or 1')
		return
	if num_petals not in petal_registry:
		petal_registry[num_petals] = 0
	petal_registry[num_petals] += magnitude
	num_sunflowers = petal_registry[num_petals] # with this # of petals
	global peak_petal_count
	if num_sunflowers == 0: # then we need to recompute by iterating the keys
		peak_petal_count = get_peak_petal_count() # we just harvested the last
		# sunflower with this # of petals
	else:
		peak_petal_count = max(num_petals, peak_petal_count) # we just planted a
		# sunflower, check if it has more petals than the current peak

def plant_sunflower():
	plant(Entities.Sunflower)
	num_petals = measure()
	sunflower_registry[get_pos_x()][get_pos_y()] = num_petals
	register_petals(num_petals, 1)

def harvest_sunflower():
	harvest()
	num_petals = sunflower_registry[get_pos_x()][get_pos_y()]
	register_petals(num_petals, -1)

def process_sunflower_tile():
	# Assuming this tile is meant for sunflower, it processes it, meaning it either:
	# * Harvests it if its giving 8x yield
	# * Harvests it if its not yet a sunflower
	# * Ignores it if its a sunflower thats not giving 8x yield
	if can_harvest() or get_entity_type() == None: #or its blank
		do_till()
		water()
		if get_entity_type() == Entities.Sunflower:
			# Only harvest sunflower if it has the same # of petals as the
			# most petals (even if this cell is the one that has the most)
			num_petals = sunflower_registry[get_pos_x()][get_pos_y()]
			if num_petals == peak_petal_count:
				harvest_sunflower()
				plant_sunflower()
		else:
			harvest()
			plant_sunflower()

def cycle_sunflower_grid():
	global peak_petal_count
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			process_sunflower_tile()
			move(East)
		move(North)

if __name__ == '__main__':
	clear()
	move_to_origin()
	do_a_flip()
	do_a_flip()
	while True:
		cycle_sunflower_grid()

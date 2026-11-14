from utils import two_d_arr
from water import *
from till import do_till
from reset import move_to_origin

sunflower_registry = two_d_arr()
petal_registry = {} # {num_petals: num_sunflowers with that # of petals}
peak_petal_count = 0
num_sunflowers = get_world_size() # the min # of sunflowers to reserve

def init_registries():
	global sunflower_registry
	sunflower_registry = two_d_arr()
	global petal_registry
	petal_registry = {}
	global peak_petal_count
	peak_petal_count = 0

# Sunflower tiles are the first n tiles going left to right, bottom row up.
# y=0 is the bottom row, so this matches the drone's East-then-North sweep from the origin.
def tile_index(x=None, y=None):
	if x == None:
		x = get_pos_x()
	if y == None:
		y = get_pos_y()
	return y * get_world_size() + x

# Poly culture farming is also capable of spending n slots on sunflowers
def is_sunflower_designated_tile(x=None, y=None, n=num_sunflowers):
	return tile_index(x, y) < n

# Whether this is the final sunflower tile the sweep reaches
def is_last_sunflower_tile(x=None, y=None, n=num_sunflowers):
	return tile_index(x, y) == n - 1

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
	do_till() # sunflowers only grow on soil
	if not plant(Entities.Sunflower):
		return # nothing planted, so nothing to measure or register
	num_petals = measure()
	sunflower_registry[get_pos_x()][get_pos_y()] = num_petals
	register_petals(num_petals, 1)

def harvest_sunflower():
	harvest()
	num_petals = sunflower_registry[get_pos_x()][get_pos_y()]
	register_petals(num_petals, -1)

def adopt_unregistered_sunflower():
	# A sunflower the registries dont know about (e.g. planted before main was
	# restarted) gets measured and registered. Returns whether it adopted one.
	if get_entity_type() != Entities.Sunflower:
		return False
	if sunflower_registry[get_pos_x()][get_pos_y()] != None:
		return False
	num_petals = measure()
	sunflower_registry[get_pos_x()][get_pos_y()] = num_petals
	register_petals(num_petals, 1)
	return True

def process_sunflower_tile():
	# Assuming this tile is meant for sunflower, it processes it, meaning it either:
	# * Harvests it if its giving 8x yield
	# * Harvests it if its not yet a sunflower
	# * Ignores it if its a sunflower thats not giving 8x yield
	if adopt_unregistered_sunflower():
		# dont harvest on the visit that adopts it: the peak isnt trustworthy
		# until every existing sunflower has been registered (one full pass)
		return
	if can_harvest() or get_entity_type() in [None, Entities.Dead_Pumpkin]: #or its blank
		water(True)
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

def cycle_sunflower(till_power=80):
	# Sunflower left and right till done
	dir = East
	while(num_items(Items.Power) < till_power):
		if num_sunflowers > get_world_size():
			print("Expand world size or decrease num_sunflowers")
			return
		process_sunflower_tile()
		if is_last_sunflower_tile():
			dir = West
		if get_pos_x() == 0:
			dir = East
		move(dir)

if __name__ == '__main__':
	clear()
	move_to_origin()
	do_a_flip()
	do_a_flip()
	while True:
		cycle_sunflower()

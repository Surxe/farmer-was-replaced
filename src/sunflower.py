from utils import two_d_arr
from water import *
from till import do_till
from reset import move_to_origin

sunflower_registry = two_d_arr()
petal_registry = {} # {num_petals: num_sunflowers with that # of petals}
peak_petal_count = 0

def log():
	print('peak_petal_count: ', peak_petal_count)
	do_a_flip()
	do_a_flip()
	print('petal_registry: ', petal_registry)
	do_a_flip()
	do_a_flip()
	print('sunflower_registry: ', sunflower_registry)
	do_a_flip()
	do_a_flip()

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

def cycle_sunflower_grid():
	global peak_petal_count
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if can_harvest():
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
			move(East)
		move(North)

if __name__ == '__main__':
	clear()
	move_to_origin()
	do_a_flip()
	do_a_flip()
	while True:
		cycle_sunflower_grid()

sunflowers = [] #list of tuples(x, y, num_petals)
# make it a dict keyed by x+y later


def plant_sunflower():
	plant(Entities.Sunflower)
	
	sunflower = (get_pos_x, get_pox_y, measure())
	sunflowers.append(sunflower)
	
def harvest_sunflower():
	
	# ensure >= 10 sunflowers on field
	# check that the current one has the most petals
	
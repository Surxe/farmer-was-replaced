from till import do_till
from water import *

STARTING_FERTILIZER = num_items(Items.Fertilizer)

# Only spend fertilizer if we're not at a net loss
def profitted_fertilizer_this_run():
	profitted_fertilizer = num_items(Items.Fertilizer) - STARTING_FERTILIZER
	if profitted_fertilizer < 0:
		pass #print("FERTILIZER PRODUCTION NOT SUFFICIENT, LOST FERTILIZER")
	return profitted_fertilizer

def fertilize_till_is_entity(entity):
	# Fertilize spams a cell till its grown as the desired entity
	# When the entity that's planted can grow into something that isn't
	# the desired entity, it harvests and iterates (pumpkins)
	while not (get_entity_type() == entity and can_harvest()):
		if get_entity_type() != entity:
			harvest()
			do_till()
			water()
			plant(entity)
		use_item(Items.Fertilizer)

if __name__ == '__main__':
    pass

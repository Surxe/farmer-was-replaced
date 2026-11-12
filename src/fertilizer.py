from till import do_till
from water import *

def fertilize_till_is_entity(entity):
	# Fertilize spams a cell till its grown as the desired entity
	# When the entity that's planted can grow into something that isn't
	# the desired entity, it harvests and iterates (pumpkins)
	while get_entity_type() != entity:
		harvest()
		do_till()
		water()
		plant(entity)
		use_item(Items.Fertilizer)

if __name__ == '__main__':
    pass

from pumpkin import in_final_pump_spot
from load_balancing import scale_pump_size

def do_harvest(cycle_had_dead_pumps, pump_size):
	# returns (if it had a dead pumpkin, pump_size)
	ent_type = get_entity_type()
	if ent_type == Entities.Dead_Pumpkin:
		return True, pump_size # had a dead pumpkin
	elif can_harvest():
		if ent_type == Entities.Pumpkin:
			if in_final_pump_spot(pump_size) and not cycle_had_dead_pumps:
				harvest()
				pump_size = scale_pump_size()
		else:
			harvest()
	return False, pump_size
		
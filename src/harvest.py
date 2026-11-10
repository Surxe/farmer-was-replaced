from pumpkin import in_final_pump_spot

def do_harvest(cycle_had_dead_pumps):
	# returns (if it had a dead pumpkin)
	ent_type = get_entity_type()
	if ent_type == Entities.Dead_Pumpkin:
		return True # had a dead pumpkin
	elif can_harvest():
		if ent_type == Entities.Pumpkin:
			if in_final_pump_spot() and not cycle_had_dead_pumps:
				harvest()
		else:
			harvest()
	return False
		
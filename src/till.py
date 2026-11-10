def do_till():
	if get_ground_type() != Grounds.Soil:
		till()
		return True
	return False
items = [Items.Hay, Items.Wood, Items.Carrot, Items.Pumpkin]
def scale_pump_size():
	if need_pump_most():
	# we have more pumps than carrots and its still outpacing carrots
		pump_size = 6
	else:
		pump_size = 0
	return pump_size
print()
def get_item_least_supply(exclude=Items.Pumpkin):
	least_item_supply = 10000000
	least_item_obj = -1
	for item in items:
		if item == exclude:
			continue
		item_supply = num_items(item)
		if item_supply < least_item_supply:
			least_item_obj = item
			least_item_supply = item_supply
	return least_item_obj
	
def need_hay_most():
	return get_item_least_supply() == Items.Hay
	
def need_wood_most():
	return get_item_least_supply() == Items.Wood
	
def need_carrot_most():
	return get_item_least_supply() == Items.Carrot
	
def need_pump_most():
	return get_item_least_supply(None) == Items.Pumpkin


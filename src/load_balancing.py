items = [Items.Hay, Items.Wood, Items.Carrot, Items.Pumpkin]
def get_item_needed_most():
	least_item_supply = 10000000
	least_item_obj = -1
	for item in items:
		item_supply = num_items(item)
		if item_supply < least_item_supply:
			least_item_obj = item
			least_item_supply = item_supply
	return least_item_obj
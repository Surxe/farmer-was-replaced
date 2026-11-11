def two_d_arr():
	cols = []
	for i in range(get_world_size()):
		row = []
		for j in range(get_world_size()):
			row.append(None)
		cols.append(row)
	return cols

def one_d_arr(v=None):
	arr = []
	for i in range(get_world_size()):
		arr.append(v)
	return arr

if __name__ == '__main__':
	my_arr = two_d_arr()
	print(my_arr)

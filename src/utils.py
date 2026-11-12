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

def num_of_n_in_list(list, n):
	num = 0
	for elem in list:
		if elem == n:
			num += 1
	return num

def rev_dict(dict):
	# For a given dict, reverses the dict
	# Input: {
	# 	a: 1
	# 	b: 1
	# 	c: 2
	# }
	# Output: {
	# 	1: [a, b]
	# 	2: [c]
	# }

	output = {}
	for key in dict:
		value = dict[key]
		if value not in output:
			output[value] = []
		output[value].append(key)
	return output

def rev_lookup_is_in(dict, key, lookup_value):
	# In a non-nested dict, returns whether the value is a element in the key's value
	# Inputs:
	# dict: {
	#  	1: [a, b],
	# 	2: [c]
	# }
	# key: 1
	# value: b

	# Outputs: True, because dict[1] is [a, b], and b is in [a, b]
	return lookup_value in dict[key]

if __name__ == '__main__':
	my_arr = two_d_arr()

	input = {
		"a": 1,
		"b": 1,
		"c": 2
	}
	reversed_dict = rev_dict(input)
	print(reversed_dict)

	do_a_flip()
	input_dict = reversed_dict
	print(rev_lookup_is_in(input_dict, 1, "b"))

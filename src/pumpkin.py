from till import *
from water import *
from utils import two_d_arr, one_d_arr, num_of_n_in_list
from reset import move_to_origin
from fertilizer import fertilize_till_is_entity, profitted_fertilizer_this_run
from sunflower import *

PLANTED = 'planted' # pumpkin may still grow or die, keep visiting it
GROWN = 'grown' # pumpkin is fully grown, it never needs another visit
power_needed_for_cycle = 150

# ---- tracker: which cells still need visiting ----

# The tracker records each cell as PLANTED or GROWN and keeps per-row / per-col
# PLANTED counts so whole lines with nothing left to check can be skipped.
def new_tracker():
	return {
		'registry': two_d_arr(),
		'planted_in_row': one_d_arr(0), # indexed by y
		'planted_in_col': one_d_arr(0), # indexed by x
		'total_planted': 0,
	}

# Mark the drone's current cell as `state`. Only real transitions touch the counts,
# so re-marking a cell with the state it already has is a no-op.
def mark_cell(tracker, state):
	x = get_pos_x()
	y = get_pos_y()
	prev = tracker['registry'][x][y]
	if prev == state:
		return
	tracker['registry'][x][y] = state
	delta = 0
	if state == PLANTED:
		delta = 1
	elif prev == PLANTED:
		delta = -1
	tracker['planted_in_row'][y] += delta
	tracker['planted_in_col'][x] += delta
	tracker['total_planted'] += delta

def all_grown(tracker):
	return tracker['total_planted'] == 0

# ---- movement ----

def do_move(col_then_row):
	if col_then_row:
		move(East)
	else:
		move(North)

# snake cols->rows (East then North) and skip rows if theres more skippable rows than cols
# else, snake rows->cols (North then East) and skip cols
def choose_col_then_row(tracker):
	empty_rows = num_of_n_in_list(tracker['planted_in_row'], 0)
	empty_cols = num_of_n_in_list(tracker['planted_in_col'], 0)
	return empty_rows > empty_cols

# line i is a row (y) when sweeping East, a col (x) when sweeping North
def line_has_planted(tracker, i, col_then_row):
	if col_then_row:
		return tracker['planted_in_row'][i] > 0
	return tracker['planted_in_col'][i] > 0

# ---- per-cell actions ----

def plant_pumpkin():
	if get_entity_type() != None:
		harvest() # clears leftover crops and dead pumpkins
	do_till()
	water()
	plant(Entities.Pumpkin)

# After the # of dead pumpkins is low enough (its immediately low enough after 1st iter)
# it becomes more efficient to stay at this position and spam fertilizer till its no longer a dead one.
# One might think its advantageous to set a threshold for the # of dead pumps before applying this, except that for this
# first have to confirm the # of dead pumps, which takes a full 2nd iteration. So with a threshold of 1 or more confirmed pumps,
# it wouldnt be able to apply till iter3. Applying immediately on the 2nd iter is faster every time, at least at n=6 with the current dead pumpkin odds.
def try_fertilize_dead_pumpkin():
	if get_entity_type() == Entities.Dead_Pumpkin: # and profitted_fertilizer_this_run() > 0:
		fertilize_till_is_entity(Entities.Pumpkin) # leaves a fully grown pumpkin

def process_pump_cell(tracker):
	try_fertilize_dead_pumpkin()
	entity = get_entity_type()
	if entity == Entities.Pumpkin:
		if can_harvest():
			# ready to harvest, but the whole grid isnt ready yet
			mark_cell(tracker, GROWN)
		else:
			# still growing, it may yet die so keep checking it
			mark_cell(tracker, PLANTED)
	else:
		# empty, dead pumpkin, or a leftover crop (grown or not)
		plant_pumpkin()
		mark_cell(tracker, PLANTED)

# ---- sweeps ----

# One pass over the grid. On a full pass every line is visited; otherwise lines
# with no PLANTED cells are skipped. Either way the drone wraps back to where it started.
def sweep(tracker, col_then_row, full_pass):
	for i in range(get_world_size()):
		if not full_pass and not line_has_planted(tracker, i, col_then_row):
			do_move(not col_then_row)
			continue
		for j in range(get_world_size()):
			process_pump_cell(tracker)
			do_move(col_then_row)
		do_move(not col_then_row)

# once its past the 1st pass, every cell is either PLANTED or GROWN.
# from then on any cell thats not grown is treated as a possible dead spot that it has to check,
# and grown cells never need checking again. This leads us to the pathing algorithm
def cycle_pump_grid():
	# Check if we need power for the cycle first
	global power_needed_for_cycle
	print('power_needed_for_cycle: ', power_needed_for_cycle)
	cycle_sunflower(power_needed_for_cycle)
	move_to_origin()

	# We got enough, lets track power we use this run and then perform
	num_pump_items_cycle_start = num_items(Items.Pumpkin)
	time_cycle_start = get_time()
	power_cycle_start = num_items(Items.Power)
	tracker = new_tracker()

	sweep(tracker, True, True)
	while not all_grown(tracker):
		sweep(tracker, choose_col_then_row(tracker), False)

	# every cell is grown, so the grid is one merged pumpkin.
	# a full pass wraps back to the origin, which is part of it
	harvest()
	move_to_origin()
	profit = num_items(Items.Pumpkin) - num_pump_items_cycle_start
	time_taken = get_time() - time_cycle_start
	power_needed_for_cycle = (power_cycle_start - num_items(Items.Power)) * 1.1
	return profit, time_taken

# pumpkins will be forced in the bottom left half of the grid,
# regardless of load balancing
# they will always be in a square of NxN size
# instead- load balancing will determine the size of N
def in_final_pump_spot(pump_size=None):
	if pump_size == None:
		pump_size = get_world_size()
	return get_pos_x() == pump_size-1 and get_pos_y() == pump_size-1
	# this is the last position thats checked for a pump.

if __name__ == "__main__":
	clear()
	sum_profit = 0
	sum_time = 0
	while True:
		profit, time = cycle_pump_grid()
		# Analytics
		sum_profit += profit
		sum_time += time
		this_profit_rate = profit / time #pumpkins / second
		avg_profit_rate = sum_profit / sum_time
		print('this_profit_rate: ', this_profit_rate)

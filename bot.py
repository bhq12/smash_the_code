import copy
import math
import random
import sys


GRID_HEIGHT = 12
GRID_WIDTH = 6
FUTURE_BLOCK_ARRAY_SIZE = 8
SKULL_BLOCK_CHAR = '0'
EMPTY_CELL_CHAR = '.'
MINIMUM_ADJACENT = 4

#('.' = empty, '0' = skull block, '1' to '5' = colored block)

class Block:
	def __init__(self, x, y, colour = EMPTY_CELL_CHAR):
		self.x = x
		self.y = y
		self.colour = colour
	def __str__(self):
		return "x: " + str(self.x) + " y: " + str(self.y) + " c: " + self.colour
	def __repr__(self):
		return "x: " + str(self.x) + " y: " + str(self.y) + " c: " + self.colour
	
def read_inputs():
	for i in range(FUTURE_BLOCK_ARRAY_SIZE):
		future_colours[i] = [int(j) for j in input().split()][0]
	score = int(input())
	
	for i in range(GRID_HEIGHT):
		row = input()
		grid[i] = [None] * GRID_WIDTH
		for j in range(len(row)):
			grid[i][j] = Block(j,GRID_HEIGHT - 1 - i,row[j])
			
	opponent_score = int(input())
	
	for i in range(GRID_HEIGHT):
		row = input()
		opponent_grid[i] = [None] * GRID_WIDTH
		for j in range(len(row)):
			opponent_grid[i][j] = Block(j,GRID_HEIGHT - 1 - i,row[j])
	
	for row in range(len(grid)):
		for i in range(len(grid[row])):
			block = grid[row][i]
			if(block.colour != EMPTY_CELL_CHAR):
				top_row[i] = block.colour
				top_row_height[i] = row
	#my mental model prefers higher rows -> higher grid index
	grid.reverse()
	opponent_grid.reverse()

def simulate_placement(grid, colour, column):
	block1 = Block(column, 0, colour)
	block2 = Block(column, 0, colour)
	
	drop_block_into_grid(block1, grid)
	drop_block_into_grid(block1, grid)
	
def drop_block_into_grid(block, grid):
	height = GRID_HEIGHT - 1
	row = block.x
	
	while height > 0:
		if grid[height][row].colour != EMPTY_CELL_CHAR:
			grid[height + 1][row] = block
			block.y = height + 1
		height -= 1

def drop_block_within_grid(block, grid):
	height = block.y
	row = block.x
	grid[block.y][block.x] = Block(block.x, block.y, EMPTY_CELL_CHAR)
	
	while height > 0:
		if grid[height][row].colour != EMPTY_CELL_CHAR:
			block.y = height + 1
		height -= 1

def erase_block(block, grid):
	block.colour = EMPTY_CELL_CHAR
	if(block.y < GRID_HEIGHT - 1):
		above_block = grid[block.y + 1][block.x]
		drop_block_within_grid(above_block)

def check_turn(grid):
	visited = set()
	scoring_blocks = set()
	for y in range(GRID_HEIGHT):
		for x in range(GRID_WIDTH):
			block = grid[y][x]
			if block.colour != EMPTY_CELL_CHAR and block.colour != SKULL_BLOCK_CHAR:
				same_neighbours = find_identical_adjacent_blocks(block, grid)
				if len(same_neighbours) >= MINIMUM_ADJACENT:
					scoring_blocks = scoring_blocks.union(same_neighbours)
	return scoring_blocks

def find_identical_adjacent_blocks(block, grid):
	visited, same_neighbours = find_same_neighbours(block, grid, set(), {block})
	return same_neighbours
	
def find_same_neighbours(block, grid, visited, same_neighbours):
	visited.add(block)
	neighbours = get_all_neighbours(block, grid)
	same_colour_neighbours = [n for n in neighbours if n.colour == block.colour and n not in visited]
	
	for neighbour in same_colour_neighbours:
		same_neighbours.add(neighbour)
		visited, same_neighbours = find_same_neighbours(neighbour, grid, visited, same_neighbours)
	
	return visited, same_neighbours
		
def get_all_neighbours(block, grid):
	neighbours = []
	if(block.x > 0):
		neighbours.append(grid[block.y][block.x - 1])#left
	if(block.x < GRID_WIDTH - 1):
		neighbours.append(grid[block.y][block.x + 1])#right
	if(block.y > 0):
		neighbours.append(grid[block.y - 1][block.x])#down
	if(block.y < GRID_HEIGHT - 1):
		neighbours.append(grid[block.y + 1][block.x])#up
	return neighbours



def plan_turn(grid, future_colours):
	highest_score = 0
	highest_score_column = random.randint(0,GRID_WIDTH - 1)
	for i in range(GRID_WIDTH):
		column_full = grid[GRID_HEIGHT - 1][i] != EMPTY_CELL_CHAR
		
		if(column_full):
			scoring_blocks = set()
			grid_copy = copy.deepcopy(grid)
		else:
			grid_copy = copy.deepcopy(grid)
			simulate_placement(grid_copy, future_colours[0], i)
			scoring_blocks = check_turn(grid_copy)
			for block in scoring_blocks:
				erase_block(grid_copy, block)
			
		for j in range(GRID_WIDTH):
			column_full = grid_copy[GRID_HEIGHT - 1][i] != EMPTY_CELL_CHAR
			if column_full != True:
				grid_copy_copy = copy.deepcopy(grid_copy)
				score = len(scoring_blocks)
				simulate_placement(grid_copy_copy, future_colours[1], j)
				score_2 = len(check_turn(grid_copy_copy))
				if(score + score_2 > highest_score):
					highest_score = score + score_2
					highest_score_column = i
	if highest_score == 0:
		while grid[GRID_HEIGHT - 1][i] == EMPTY_CELL_CHAR:
			highest_score_column = (highest_score_column + 1)%GRID_WIDTH
	return highest_score_column

def find_shortest_neighbour(place):
	left = top_row[(place - 1)%GRID_WIDTH]
	middle = top_row[(place)%GRID_WIDTH]
	right = top_row[(place + 1)%GRID_WIDTH]
	
	if(min(left,middle,right) == left):
		return (place - 1)%GRID_WIDTH
	elif(min(left,middle,right) == middle):
		return place%GRID_WIDTH
	else:
		return (place+1)%GRID_WIDTH
	
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop
future_colours = [None] * FUTURE_BLOCK_ARRAY_SIZE
grid = [None] * GRID_HEIGHT
opponent_grid = [None] * GRID_HEIGHT
score = 0
opponent_score = 0

top_row = ['7'] * GRID_WIDTH
top_row_height = [0] * GRID_WIDTH

place = 0

while True:
	read_inputs()

	# Write an action using print
	# To debug: print("Debug messages...", file=sys.stderr)
	# "x": the column in which to drop your blocks
	print(plan_turn(grid, future_colours))
	
	
	

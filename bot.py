import sys
import math

GRID_HEIGHT = 12
GRID_WIDTH = 6
FUTURE_BLOCK_ARRAY_SIZE = 8
SKULL_BLOCK_CHAR = '0'
EMPTY_CELL_CHAR = '.'

#('.' = empty, '0' = skull block, '1' to '5' = colored block)
class Block:
	def __init__(self, x, y, colour = EMPTY_CELL_CHAR):
		self.x = x
		self.y = y
		self.colour = colour
	
def read_inputs():
	for i in range(FUTURE_BLOCK_ARRAY_SIZE):
		future_colours[i] = [int(j) for j in input().split()][0]
	score = int(input())
	for i in range(GRID_HEIGHT):
		row = input()
		grid[i] = [None] * GRID_WIDTH
		for j in range(len(row)):
			grid[i][j] = Block(i,j,row[j])
	opponent_score = int(input())
	for i in range(GRID_HEIGHT):
		row = input()
		opponent_grid[i] = [None] * GRID_WIDTH
		for j in range(len(row)):
			opponent_grid[i][j] = Block(i,j,row[j])
	
	for row in range(len(grid)):
		for i in range(len(grid[row])):
			block = grid[row][i]
			if(block.colour != EMPTY_CELL_CHAR):
				top_row[i] = block.colour
				top_row_height[i] = row



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
	print("top_row:" + str(top_row), file=sys.stderr)
	print("top_row_height:" + str(top_row_height), file=sys.stderr)
	# "x": the column in which to drop your blocks
	
	
	position = find_shortest_neighbour(place)
	
	for i in range(len(top_row)):
		if(int(top_row[i]) == future_colours[0]):
			position = i
	
	print(position)
	place = place + 1
	
	

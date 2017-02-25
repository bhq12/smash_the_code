import sys
import math

    
def read_inputs():
    for i in range(8):
        future_colours[i] = [int(j) for j in input().split()][0]
    score = int(input())
    for i in range(12):
        grid[i] = input()
    opponent_score = int(input())
    for i in range(12):
        opponent_grid[i] = input()  # One line of the map ('.' = empty, '0' = skull block, '1' to '5' = colored block)
    
    for row in range(len(grid)):
        for i in range(len(grid[row])):
            point = grid[row][i]
            if(point != '.' and point != '0'):
                top_row[i] = point
                top_row_height[i] = row



def find_shortest_neighbour(place):
    left = top_row[(place - 1)%6]
    middle = top_row[(place)%6]
    right = top_row[(place + 1)%6]
    
    if(min(left,middle,right) == left):
        return (place - 1)%6
    elif(min(left,middle,right) == middle):
        return place%6
    else:
        return (place+1)%6
    
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop
future_colours = [None] * 8
grid = [None] * 12
opponent_grid = [None] * 12
score = 0
opponent_score = 0

top_row = ['7'] * 6
top_row_height = [0] * 6

place = 0

while True:
    read_inputs()

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # "x": the column in which to drop your blocks
    
    
    position = find_shortest_neighbour(place)
    
    for i in range(len(top_row)):
        if(int(top_row[i]) == future_colours[0]):
            position = i
    
    print(position)
    place = place + 1
    
    

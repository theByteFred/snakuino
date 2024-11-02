import serial
from time import sleep
from random import choice
from itertools import product


print("connecting")
try:
	ard = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
except:
	from serial.tools import list_ports
	print("error: port not available")
	print("available ports:")
	for p in list_ports.comports(): 
		print(p)
	exit()



print("initialize game")
board_width = 17
board_height = 7
board = set(product(range(board_width),range(board_height))) 
snake = 3*[(board_width//2,board_height//2)] # store snake as list
dx,dy = 1,0

def new_random_food():
	return choice(list(board-set(snake)))
food = new_random_food()


def visualize_board():
	plot = {(x,y):'.' for (x,y) in board}
	# visualize snake with "+" and
	# head as ">,<,^,v" depending on direction
	for (x,y) in snake: plot[x,y] = '+' 
	if (dx,dy) == (0,-1): plot[snake[-1]] = '^'
	if (dx,dy) == (-1,0): plot[snake[-1]] = '<' 
	if (dx,dy) == (+1,0): plot[snake[-1]] = '>'
	if (dx,dy) == (0,+1): plot[snake[-1]] = 'v'
	# visualize food as "O"
	plot[food] = 'O' 

	print()
	for y in range(board_height):
		for x in range(board_width):
			print(plot[x,y],end="")
		print()



print("start event loop")
delay = 0.5 # in seconds
threshold = 500
while True:	
	visualize_board()
	sleep(delay)
	ard.flushInput()
	line = ard.readline()
	try:
		vec = [int(x) for x in line.decode("utf-8").strip("\r\n").split()]
		print("input vector",vec)
		if vec[0] > threshold and (dx,dy) != (0,+1): 
			(dx,dy) = (0,-1) # up    (input pin A0)
		if vec[1] > threshold and (dx,dy) != (+1,0): 
			(dx,dy) = (-1,0) # left  (input pin A1)
		if vec[2] > threshold and (dx,dy) != (-1,0): 
			(dx,dy) = (+1,0) # right (input pin A2)
		if vec[3] > threshold and (dx,dy) != (0,-1): 
			(dx,dy) = (0,+1) # down  (input pin A3)
	except:
		print("skipping invalid input")


	# snake moves forward
	x,y = snake[-1] # current head position
	head = (x+dx,y+dy) # new head position
	is_alive = (head in board) and (head not in snake) 
	# snake dies if it moves out of the board or bites itself
	snake.append(head) # add new head
	snake.pop(0) # remove old tail 
	if not is_alive:
		visualize_board()
		print("GAME OVER!")
		break


	# check if food is consumed
	if snake[-1] == food:
		snake.insert(0,snake[0]) # snake eats and grows longer
		food = new_random_food() # place new food

	print("snake",snake)
	print("direction",dx,dy)
	print("food",food)

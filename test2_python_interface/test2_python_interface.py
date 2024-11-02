import serial
from time import sleep

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

print("start loop")
delay = 0.2 # in seconds
threshold = 500
while 1:	
	sleep(delay)
	ard.flushInput()
	line = ard.readline()
	try:
		vec = [int(x) for x in line.decode("utf-8").strip("\r\n").split()]
		print(vec)
		if vec[0] > threshold: print("up")
		if vec[1] > threshold: print("left")
		if vec[2] > threshold: print("right")
		if vec[3] > threshold: print("down")
	except:
		print("skip")
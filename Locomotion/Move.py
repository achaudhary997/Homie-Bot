import time
import curses
import RPi.GPIO as GPIO


def findDistance():
	
	GPIO.setmode(GPIO.BOARD)

	TRIG = 16
	ECHO = 18
	print ("[+] Distance Measurement in Progress")

	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)

	GPIO.output(TRIG, False)
	print ("[+] Waiting for sensor to settle")
	time.sleep(0.5)

	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO)==0:
		pulse_start = time.time()

	while GPIO.input(ECHO)==1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150

	ditance = round(distance, 2)

	print ("Distance:", distance, "cm") # The final distance
	GPIO.cleanup()
	return distance




# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

try:
	while True:   
		curDistance = findDistance()
		print curDistance
		char = screen.getch()
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(7,GPIO.OUT)	
		GPIO.setup(11,GPIO.OUT)
		GPIO.setup(13,GPIO.OUT)
		GPIO.setup(15,GPIO.OUT)

		if char == ord('q'):
			break
		elif char == ord('s'):
			GPIO.output(7,False)
			GPIO.output(11,False)
			GPIO.output(13,False)
			GPIO.output(15,False)
		elif curDistance > 20:
			if char == curses.KEY_RIGHT:
				GPIO.output(7,False)
				GPIO.output(11,True)
				GPIO.output(13,False)
				GPIO.output(15,True)
			elif char == curses.KEY_LEFT:
				GPIO.output(7,True)
				GPIO.output(11,False)
				GPIO.output(13,True)
				GPIO.output(15,False)
			elif char == curses.KEY_UP:
				GPIO.output(7,True)
				GPIO.output(11,False)
				GPIO.output(13,False)
				GPIO.output(15,True)
			elif char == curses.KEY_DOWN:
				GPIO.output(7,False)
				GPIO.output(11,True)
				GPIO.output(13,True)
				GPIO.output(15,False)
		else:
			GPIO.output(7,False)
			GPIO.output(11,False)
			GPIO.output(13,False)
			GPIO.output(15,False)
			
		 
finally:
	#Close down curses properly, inc turn echo back on!
	curses.nocbreak(); screen.keypad(0); curses.echo()
	curses.endwin()
	GPIO.cleanup()

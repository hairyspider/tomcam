import RPi.GPIO as GPIO
import sys

state = "OFF"

if len(sys.argv)==2:
	state = sys.argv[1]

print("Setting the state of Socket 1 to ", state)

pin=26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pin, GPIO.OUT)

if state=="ON":
	GPIO.output(pin, 0)
else:
	GPIO.output(pin, 1)

###GPIO.cleanup()

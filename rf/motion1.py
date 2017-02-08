# The code continuously checks the input pin and will print the given line of text if the input goes high.
import RPi.GPIO as GPIO
import time

# set GPIO pin numbering.
GPIO.setmode(GPIO.BCM)

#input pin
PIR_PIN = 11

# defining PIR_PIN as an input.
GPIO.setup(PIR_PIN, GPIO.IN)

try:
	print "PIR Module Test"
	print "Preparing the sensor"
	time.sleep(2)
	print "Ready!"

# Checking the input status of the input pin
	while True:
		if GPIO.input(PIR_PIN):
			print "Motion Detected!"
		time.sleep(1)
except KeyboardInterrupt:
	print "Quit!"

GPIO.cleanup()

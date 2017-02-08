from gpiozero import MotionSensor
#
# PIR    an Pin  4 GPIO_04
#
pir = MotionSensor(18)
#
# Start einer Dauerschleife
# Abbruch mit Ctrl+C
# Bei Bewegungserkennung Textausgabe
# am Bildschirm.
#

while True:
    if pir.motion_detected:
        print("Motion detected!")

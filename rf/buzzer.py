from gpiozero import Button, LED, Buzzer
#
# Button an Pin  2
# LED    an Pin  6 GPIO_17
# Buzzer an Pin 25 GPIO_15
#
button = Button(2)
led = LED(17)
buzzer = Buzzer(15)
#
# Start einer Dauerschleife
# Abbruch mit Ctrl+C
# Während Taste gedrückt, LED un Buzzer an
#
#while True:
#    button.wait_for_press()
#    led.on()
#    buzzer.beep()
#    button.wait_for_release()
#    led.off()
#    buzzer.off()
buzzer.beep()

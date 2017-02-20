#!/usr/bin/env python
#
import RPi.GPIO as GPIO
from signal import pause
from datetime import datetime
from time import sleep
#
# -------------------------------------------------------------------
# Die General Purpose Input Output Kanäle GPIO werden über die Broad-
# com Kanalnummer angesprochen, nicht über die Bordeigene.
# -------------------------------------------------------------------
#
GPIO.setmode(GPIO.BCM)
#
PIR_SIG = 15    # PIR     an GPIO_15 und +5V und GND
ADC_CLK = 18    # ADC_CLK an GPIO_18
ADC_CS  = 17    # ADC_CS  an GPIO_17
ADC_DIO = 12    # ADC_DIO an GPIO_12
LED_PWR = 23    # LED     an GPIO_23
BUZ_PWR = 24    # Buzzer  an GPIO_24
BUTTON  = 27    # Button  an GPIO_27 und +3,3V
#
# -------------------------------------------------------------------
# Setup der Kanalrichtung (Lesen=IN, schreiben=OUT)
# Achtung: ADC_DIO ändert sich innerhalb der Logik, Init in der function 
# -------------------------------------------------------------------
#
# ADC und Fotowiderstand
GPIO.setup(ADC_CLK, GPIO.OUT)
GPIO.setup(ADC_CS, GPIO.OUT)
# PIR Input
GPIO.setup(PIR_SIG, GPIO.IN)
# Button
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# LED
GPIO.setup(LED_PWR, GPIO.OUT)
GPIO.output(LED_PWR, GPIO.LOW)
# Buzzer
GPIO.setup(BUZ_PWR, GPIO.OUT)
GPIO.output(BUZ_PWR, GPIO.LOW)
#
# -------------------------------------------------------------------
# Callback Functions:
# -------------------------------------------------------------------
#
# -------------------------------------------------------------------
# LED und Buzzer an und ausschalten
# -------------------------------------------------------------------
#
def LEDonoff(channel):
    nun = datetime.now()
    sleep(0.1)
    if GPIO.input(LED_PWR):
        zeile = str(nun)+" --> Button is released -> No signal!\n"
        logfile.write(zeile)
        print("--> Button released!")
        GPIO.output(LED_PWR, GPIO.LOW)
        GPIO.output(BUZ_PWR, GPIO.LOW)
    else:
        zeile = str(nun)+" --> Button is pressed -> Signal!\n"
        logfile.write(zeile)
        print("--> Button is pressed!")
        GPIO.output(LED_PWR, GPIO.HIGH)
        GPIO.output(BUZ_PWR, GPIO.HIGH)
#
# -------------------------------------------------------------------
# PIR Motion detector
# -------------------------------------------------------------------
#
def PIRmotion(channel):
    nun = datetime.now()
    if GPIO.input(PIR_SIG):
        zeile = str(nun)+" --> Yea! PIR Motion detected!\n"
        logfile.write(zeile)
        print("Motion detected Time: %s" % nun)
#
#    Da nur die Bewegung als Ereignis zählt, wird das Zurückfallen
#    in den Ruhezustand (PIR_SIG = LOW, abfallende Flanke, FALLING)
#    nicht geloggt.
#
#    else:
#        zeile = str(nun)+" --> PIR No Signal!\n"
#        logfile.write(zeile)
#        print("No signal       Time: %s" % nun)
#
# -------------------------------------------------------------------
# Fotowiderstand und ADC
# -------------------------------------------------------------------
#
def getADC(channel=0):
    GPIO.setup(ADC_DIO, GPIO.OUT)
    GPIO.output(ADC_CS, GPIO.LOW)

    GPIO.output(ADC_CLK, GPIO.LOW)
    GPIO.output(ADC_DIO, GPIO.HIGH); sleep(0.000002)
    GPIO.output(ADC_CLK, GPIO.HIGH); sleep(0.000002)
    GPIO.output(ADC_CLK, GPIO.LOW)

    GPIO.output(ADC_DIO, GPIO.HIGH); sleep(0.000002)
    GPIO.output(ADC_CLK, GPIO.HIGH); sleep(0.000002)
    GPIO.output(ADC_CLK, GPIO.LOW)

    GPIO.output(ADC_DIO, channel); sleep(0.000002)

    GPIO.output(ADC_CLK, GPIO.HIGH)
    GPIO.output(ADC_DIO, GPIO.HIGH); sleep(0.000002)
    GPIO.output(ADC_CLK, GPIO.LOW)
    GPIO.output(ADC_DIO, GPIO.HIGH); sleep(0.000002)

    dat1 = 0
    for i in range(0, 8):
        GPIO.output(ADC_CLK, GPIO.HIGH); sleep(0.000002)
        GPIO.output(ADC_CLK, GPIO.LOW); sleep(0.000002)
        GPIO.setup(ADC_DIO, GPIO.IN)
        dat1 = dat1 << 1 | GPIO.input(ADC_DIO)

    dat2 = 0
    for i in range(0, 8):
        dat2 = dat2 | GPIO.input(ADC_DIO) << i
        GPIO.output(ADC_CLK, GPIO.HIGH); sleep(0.000002)
        GPIO.output(ADC_CLK, GPIO.LOW); sleep(0.000002)
    
    GPIO.output(ADC_CS, GPIO.HIGH)
    GPIO.setup(ADC_DIO, GPIO.OUT)

    if dat1 == dat2:
        return dat1
    else:
        return 0
#
# -------------------------------------------------------------------
#
#
#sleep(1.0)
#
# -------------------------------------------------------------------
# Start ereignisgesteuerter Listener
# -------------------------------------------------------------------
# PIR Sensor
# GPIO.add_event_detect(PIR_SIG, GPIO.BOTH, callback=PIRmotion, bouncetime=100)
GPIO.add_event_detect(PIR_SIG, GPIO.RISING, callback=PIRmotion, bouncetime=100)
#
# Button
GPIO.add_event_detect(BUTTON, GPIO.BOTH, callback=LEDonoff, bouncetime=200)
#
# -------------------------------------------------------------------
# Main program:
# -------------------------------------------------------------------
#
try:
    # Logfile öffnen
    logfile = open("/home/pi/ECG_Event.log", "a")
    # Start einer Dauerschleife
    # Abbruch mit Ctrl+C
    # Bei Tastendruck LED und Buzzer an.
    while True:
        nun = datetime.now()
        ADCvalue = getADC(0)
        if (ADCvalue <= 50):
            print("The ADC Value of fotoresistor is: %d" % ADCvalue)
            zeile = str(nun) + " The ADC Value of fotoresistor is: " + str(ADCvalue) + "\n"
            logfile.write(zeile)
        sleep(1.0)
#
except KeyboardInterrupt:
    logfile.write("5_Fotoresistor_ADC_2.py: I'm in except now\n")
    print("#")
    print("# Programmabbruch durch Ctrl-c")
#
except:
    logfile.write("5_Fotoresistor_ADC_2.py: Processing except: routine\n")
    print("! Programmabbruch durch anderen Fehler")
#    
finally:
    logfile.write("5_Fotoresistor_ADC_2.py: Processing finally routine\n")
    print("Finally close logfile and ")
    logfile.close()
    print("cleanup GPIO with GPIO.cleanup()")
    GPIO.cleanup()

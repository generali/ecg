#!/bin/bash

THIS_SYSTEM=`hostname`
THIS_SERIAL=`cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2`

while true
do
        ONLINE=1


	URL=`cat /home/pi/circonus/rpi_ecg1_url.txt`

        curl -s -o /dev/null -X PUT --insecure "$URL" --data '{
            "'$THIS_SYSTEM.$THIS_SERIAL.RPI.online'": "'$ONLINE'"
          }'
        sleep 30
done


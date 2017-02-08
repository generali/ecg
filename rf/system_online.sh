#!/bin/bash

THIS_SYSTEM=`hostname`
THIS_SERIAL=`cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2`

SENSOR_TYPE="system.online"
SLEEP_LOOP=30

DISPLAY=0
ONLINE=1

# ################################################################################

while [[ $# -gt 0 ]]
do
	key="$1"

	case $key in
  	-display)
  	  DISPLAY=1
  	;;
   -fast)
		SLEEP_LOOP=10
	;;
   *)
      # unknown option
   ;;
	esac
	shift # past argument or value
done

if [ $DISPLAY -eq 1 ]; then
   echo "System Online-Sensor"
   echo "######################################################"
fi

while true
do
	HOSTNAME=`cat /home/pi/ecg/hostname.secret | cut -d\" -f2 | cut -d= -f2`
	URL=`cat /home/pi/ecg/json_push.secret | cut -d\" -f2 | cut -d= -f2`


	if [ $DISPLAY -eq 1 ]; then
		echo "Reporting online status to  URL: $URL  as  $THIS_SYSTEM.system.online"
      # -o /dev/null -X PUT --insecure
        	curl -s "$URL" --data '{
            		"'$THIS_SYSTEM.$SENSOR_TYPE'": "'$ONLINE'"
          	}'
		else
         curl -s -o /dev/null "$URL" --data '{
            		"'$THIS_SYSTEM.$SENSOR_TYPE'": "'$ONLINE'"
          	}'
      fi
      sleep $SLEEP_LOOP
done

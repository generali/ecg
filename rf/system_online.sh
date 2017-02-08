#!/bin/bash

THIS_SYSTEM=`hostname`
THIS_SERIAL=`cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2`


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
    	*)
            # unknown option
    	;;
	esac
	shift # past argument or value
done

echo "System Online-Sensor"
echo "######################################################"

while true
do
	URL=`cat /home/pi/ecg/json_push.secret | cut -d\" -f2 | cut -d= -f2`

	if [ $DISPLAY -eq 1 ]; then
		echo "Reporting online status to  URL: $URL  as  $THIS_SYSTEM.system.online"
        fi
	curl -s -o /dev/null -X PUT --insecure "$URL" --data '{
            "'$THIS_SYSTEM.system.online'": "'$ONLINE'"
          }'
        sleep 30
done


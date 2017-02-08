#!/bin/bash

# Waittime to redo messurement
SLEEP_LOOP=30

# #################################################

THIS_SYSTEM=`hostname`
THIS_SERIAL=`cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2`
URL=`cat /home/pi/ecg/json_push.secret | cut -d\" -f2 | cut -d= -f2`

# #################################################

DISPLAY_ECHO=0
for key in "$@"
	do
	#key="$1"

	case $key in
	-display)
		DISPLAY_ECHO=1
	;;
	*)
	;;
	esac
done

while true
do
        CPU=`top -d 0.5 -b -n2 | grep "Cpu(s)"|tail -n 1 | awk '{print $2 + $4}'`
        [[ $DISPLAY_ECHO == 1 ]] && echo "cpu: $CPU"
	# Freier Speicher
        MEM_FREE=`free -m | grep "Mem:" | awk '{print $4}'`
	[[ $DISPLAY_ECHO == 1 ]] && echo "mem free: $MEM_FREE"
	# netload eth0 in
	ETH0_IN=`ifstat -i eth0 -q 1 1 | sed -n '3p' | cut -d' ' -f 5`
	[[ $DISPLAY_ECHO == 1 ]] && echo "eth0 in: $ETH0_IN"
	# netload eth0 outt
	ETH0_OUT=`ifstat -i eth0 -q 1 1 | sed -n '3p' | cut -d' ' -f 11`
	[[ $DISPLAY_ECHO == 1 ]] && echo "eth0 out: $ETH0_OUT"
	# netload wlan in
	WLAN0_IN=`ifstat -i wlan0 -q 1 1 | sed -n '3p' | cut -d' ' -f 5`
	[[ $DISPLAY_ECHO == 1 ]] && echo "wlan in: $WLAN0_IN"
	# netload wlan out
	WLAN0_OUT=`ifstat -i wlan0 -q 1 1 | sed -n '3p' | cut -d' ' -f 5`
	[[ $DISPLAY_ECHO == 1 ]] && echo "wlan0 out: $WLAN0_OUT"
	# rpi voltage
	RPI_VOLTAGE=`vcgencmd measure_volts core | cut -d'=' -f 2 | cut -d'V' -f 1`
	[[ $DISPLAY_ECHO == 1 ]] && echo "voltage: $RPI_VOLTAGE"
	# sdcard_free (%)
	SDCARD_FREE=`df -h | grep mmcb | awk '{print $5}' | cut -d'%' -f 1`
	[[ $DISPLAY_ECHO == 1 ]] && echo "sd free: $SDCARD_FREE"

        curl -s -o /dev/null -X PUT --insecure "$URL" --data '{
            "'$THIS_SYSTEM.system.cpu'": "'$CPU'",
            "'$THIS_SYSTEM.system.mem_free'": "'$MEM_FREE'",
	    "'$THIS_SYSTEM.system.eth0_in'": "'$ETH0_IN'",
	    "'$THIS_SYSTEM.system.eth0_out'": "'$ETH0_OUT'",
	    "'$THIS_SYSTEM.system.wlan0_in'": "'$WLAN0_IN'",
	    "'$THIS_SYSTEM.system.wlan0_out'": "'$WLAN0_OUT'",
	    "'$THIS_SYSTEM.system.sdcard_free'": "'$SDCARD_FREE'",
	    "'$THIS_SYSTEM.system.voltage'": "'$RPI_VOLTAGE'"
         }'

#        curl -X PUT --insecure "$URL" --data '{
#            "'$THIS_SYSTEM'"."'$THIS_SERIAL.RPI.cpu'": "'$CPU'",
#            "'$THIS_SYSTEM'"."'$THIS_SERIAL.RPI.mem_free'": "'$MEM_FREE'",
#	    "'$THIS_SYSTEM'"."'$THIS_SERIAL.RPI.eth0_in'": "'$ETH0_IN'",
#	    "'$THIS_SYSTEM'"."'$THIS_SERIAL.RPI.eth0_out'": "'$ETH0_OUT'",
#	    "'$THIS_SYSTEM'"."'$THIS_SERIAL.RPI.wlan0_in'": "'$WLAN0_IN'",
#	    "'$THIS_SYSTEM'"."'$THIS_SERIAL.RPI.wlan0_out'": "'$WLAN0_OUT'",
#	    "'$THIS_SYSTEM'"."'$THIS_SERIAL.RPI.sdcard_free'": "'$SDCARD_FREE'",
#	    "'$THIS_SYSTEM'"."'$THIS_SERIAL.RPI.voltage'": "'$RPI_VOLTAGE'"
 #        }'


        sleep $SLEEP_LOOP
done

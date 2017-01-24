#!/bin/bash

WATCHDOG_FILE=/home/pi/ecg1/watchdog.list
THISSCRIPT=$(readlink -f $0)

echo "Watchdog"
echo "================================="
echo "To install, edit 'sudo nano /etc/crontab' and add '* * * * * root $THISSCRIPT'"
echo ""
echo "Arguments:"
echo "$THISSCRIPT <-file:listfile> <-display>"
echo ""


while read WATCHDOG_PROCESS; do
	if [[ "$WATCHDOG_PROCESS" != "#"* ]];then
		# String no comment

		if [[ $WATCHDOG_PROCESS == -* ]]; then
			WATCHDOG_KILL=`echo -n "$WATCHDOG_PROCESS" | tail -c +2 | sed -e 's/^[[:space:]]*//'`
			echo -n "Beende Prozess '$WATCHDOG_KILL'..."
			sudo pkill -f $WATCHDOG_KILL
			echo "OK"
		else
			if [[ !  -z  $WATCHDOG_PROCESS  ]]; then
			    	echo -n "Prüfe Prozess '$WATCHDOG_PROCESS'..."
				COUNT=`ps -ef | grep "$WATCHDOG_PROCESS" | grep -v "grep" | wc -l`
				if [ $COUNT -eq 0 ]; then
					echo "nicht gefunden!"
					$($WATCHDOG_PROCESS) &
				else
					echo "gefunden. OK"
				fi
			fi
		fi
	fi
done < $WATCHDOG_FILE

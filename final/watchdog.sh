#!/bin/bash

WATCHDOG_FILE=/home/pi/ecg1/watchdog.list
THISSCRIPT=$(readlink -f $0)

echo "Watchdog"
echo "================================="
echo "To install, edit 'sudo nano /etc/crontab' and add '* * * * * root $THISSCRIPT <arguments>'"
echo ""
echo "Arguments:"
echo "$THISSCRIPT <-file=listfile> <-display>"
echo ""
echo "-file=   : different list file (default: watchdog.list)"
echo "-display : echo output to console"
echo ""

DISPLAY_ECHO=0
#while [[ $# -gt 1 ]]
for key in "$@"
	do
	key="$1"

	case $key in
	-display)
		DISPLAY_ECHO=1
	;;
	-edit)
		sudo nano /etc/crontab
		exit 0
	;;
	-file=*)
		WATCHDOG_FILE="${key#*=}"
		echo "Use non-default watchdog file '$WATCHDOG_FILE'"
	;;
	-log=*)
		LOG_FILE="${key#*=}"
		echo "Use log file '$LOG_FILE'"
	;;
	*)
		# unknown option
	;;
	esac
	shift
done

while read WATCHDOG_PROCESS; do
	if [[ "$WATCHDOG_PROCESS" != "#"* ]];then
		# String no comment

		if [[ $WATCHDOG_PROCESS == -* ]]; then
			WATCHDOG_KILL=`echo -n "$WATCHDOG_PROCESS" | tail -c +2 | sed -e 's/^[[:space:]]*//'`
			[[ $DISPLAY_ECHO == 1 ]] && echo -n "Terminate Process '$WATCHDOG_KILL'..."
			sudo pkill -f $WATCHDOG_KILL
			[[ $DISPLAY_ECHO == 1 ]] && echo "OK"
		else
			if [[ !  -z  $WATCHDOG_PROCESS  ]]; then
			    	[[ $DISPLAY_ECHO == 1 ]] && echo -n "Check running process '$WATCHDOG_PROCESS'..."
				COUNT=`ps -ef | grep "$WATCHDOG_PROCESS" | grep -v "grep" | wc -l`
				if [ $COUNT -eq 0 ]; then
					[[ $DISPLAY_ECHO == 1 ]] && echo "not found!"
					# run process in background
					$($WATCHDOG_PROCESS) &
				else
					[[ $DISPLAY_ECHO == 1 ]] && echo "found. OK"
				fi
			fi
		fi
	fi
done < $WATCHDOG_FILE

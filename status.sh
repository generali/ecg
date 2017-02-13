#!/bin/bash

PROCESS_LIST = "webserver\.py|bt\.py|motion\.py|system\.sh|system_online\.sh"

# ################
HOSTNAME=`hostname`

# ################


echo "HOSTNAME"
echo "===================================================================="
echo $HOSTNAME
echo ""
echo "ECG PROZESSE"
echo "===================================================================="
ps -ef | grep -v grep | grep ecg | grep --color -E "webserver\.py|bt\.py|motion\.py|system\.sh|system_online\.sh|watchdog\.sh"

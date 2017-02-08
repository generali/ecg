#!/bin/bash

# ################
HOSTNAME=`hostname`

# ################


echo "HOSTNAME"
echo "===================================================================="
echo $HOSTNAME
echo ""
echo "ECG PROZESSE"
echo "===================================================================="
ps -ef | grep -v grep | grep ecg | grep -E "\.py|\.sh"

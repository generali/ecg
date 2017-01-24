#!/bin/bash
THISHOST=`hostname`

#cd ~/$THISHOST
git add * .
git commit -m "auto commit by $THISHOST"
git push

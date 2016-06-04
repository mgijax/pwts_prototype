#!/bin/sh

ERROR_LOG=startserver.sh.error
rm -f $ERROR_LOG
nohup python prodserver.py --port=$SERVER_PORT  &

sleep 1

if [[ -s $ERROR_LOG ]] ; then
        cat $ERROR_LOG
fi ;

echo "stderr log = $ERROR_LOG"


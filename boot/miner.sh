#!/bin/bash

function usage()
{
	printf "Miner Control\n\n"
	printf "Usage: miner [OPTION]\n\n"
	printf "start: Start Miner Service\n"
	printf "stop: Stop Miner Service\n"
	printf "restart: Restart Miner Service\n"

}

function start()
{

	SCREEN=$(screen -ls lsminer | grep lsminer | wc -l)
	[ "$SCREEN" -gt 1 ] && echo "Miner already running..." && exit

	echo "Miner Starting..."
	screen -dmS lsminer -t lsminer python3 /home/lsminer/lsminer/update.py
}


function stop()
{
	screens=`screen -ls lsminer | grep -E "[0-9]+\.lsminer" | cut -d. -f1 | awk '{print $1}'`

	if [[ -z $screens ]]; then
		echo "No miner screens found"
	else
		for pid in $screens; do
			echo "Stopping screen session: $pid.lsminer"
			screen -S $pid -X quit
		done
	fi
}



case $1 in
	start)
		start
	;;
	stop)
		stop
	;;
	restart)

		echo "Restarting miner"
		stop
		sleep 1
		start
	;;
	*)
		usage
	;;
esac

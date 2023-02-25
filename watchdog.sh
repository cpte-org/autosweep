#!/bin/bash

# Set the path to the Python script
PYTHON_SCRIPT=/home/Zcash/main.py

# Set the log file path
LOG_FILE=/home/Zcash/sweeper.log

# Set the maximum idle time in seconds
MAX_IDLE_TIME=300

# Define a function to check if the Python script is running and producing output
function check_python_script {
    if ! pgrep -f "$PYTHON_SCRIPT" > /dev/null ; then
        echo "Python script is not running. Restarting..."
        echo "---------------------------" >> $LOG_FILE
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Python script is not running. Restarting..." >> $LOG_FILE
        # Start the Python script in the background
        nohup python $PYTHON_SCRIPT >> $LOG_FILE &
        return
    fi

    # Get the modification time of the log file
    LOG_MOD_TIME=$(stat -c %Y $LOG_FILE)

    # Get the current time
    CURRENT_TIME=$(date +%s)

    # Calculate the idle time
    IDLE_TIME=$(($CURRENT_TIME - $LOG_MOD_TIME))

    # Check if the idle time is greater than the maximum allowed
    if [ $IDLE_TIME -gt $MAX_IDLE_TIME ]; then
        echo "Python script is not producing output. Restarting..."
        echo "---------------------------" >> $LOG_FILE
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Python script is not producing output. Restarting..." >> $LOG_FILE
        # Kill the existing Python script process and start a new one in the background
        pkill -f "$PYTHON_SCRIPT"
        nohup python $PYTHON_SCRIPT >> $LOG_FILE &
    fi
}

# Run the function in a loop
while true; do
    check_python_script
    sleep 30 # check every 30 seconds
done
